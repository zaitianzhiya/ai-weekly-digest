#!/usr/bin/env python3
"""AI Weekly Digest — 报告生成辅助工具

此脚本不直接调用 LLM API（由 CI workflow 中的 Claude 调用完成），
而是提供生成报告所需的结构化上下文信息，包括:
1. 上期报告的参考回顾
2. 当前周信息
3. Prompt 模板加载
4. 数据库状态检查
"""

import json
import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "db" / "ai_weekly_digest.db"
PROMPTS_DIR = ROOT / "prompts"
OUTPUT_DIR = ROOT / "output"


def get_previous_week(conn: sqlite3.Connection):
    """获取上期周报信息"""
    row = conn.execute("""
        SELECT week_number, week_range, report_date, total_events, key_numbers
        FROM weekly_reports ORDER BY week_number DESC LIMIT 1
    """).fetchone()
    if not row:
        return None

    prev = dict(row)

    # 获取上期 Top 5 事件作为上下文
    report_id = conn.execute(
        "SELECT id FROM weekly_reports WHERE week_number = ?", (prev['week_number'],)
    ).fetchone()[0]
    top5 = conn.execute("""
        SELECT rank, weight, title, one_liner FROM events
        WHERE report_id = ? ORDER BY rank LIMIT 5
    """, (report_id,)).fetchall()
    prev['top5'] = [dict(r) for r in top5]

    # 获取上期趋势
    trends = conn.execute("""
        SELECT title, description FROM trend_insights
        WHERE report_id = ? ORDER BY trend_number
    """, (report_id,)).fetchall()
    prev['trends'] = [dict(t) for t in trends]

    return prev


def compute_current_week():
    """计算当前周的元数据"""
    today = datetime.now()
    # ISO 周号
    iso_year, iso_week, _ = today.isocalendar()
    week_number = f"{iso_year}-W{iso_week:02d}"

    # 本周一
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)

    week_range = f"{monday.strftime('%Y.%m.%d')} - {sunday.strftime('%Y.%m.%d')}"
    report_date = today.strftime("%Y-%m-%d")

    return {
        "week_number": week_number,
        "week_range": week_range,
        "report_date": report_date,
        "monday": monday.strftime("%Y-%m-%d"),
        "sunday": sunday.strftime("%Y-%m-%d"),
    }


def load_prompt(prompt_name: str) -> str:
    """加载 Prompt 模板"""
    prompt_path = PROMPTS_DIR / f"{prompt_name}.md"
    if prompt_path.exists():
        return prompt_path.read_text(encoding="utf-8")
    return ""


def build_generation_context():
    """构建传递给 LLM 的生成上下文"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row

    current = compute_current_week()
    previous = get_previous_week(conn)
    conn.close()

    deep_prompt = load_prompt("weekly-deep")
    taxonomy = load_prompt("taxonomy")
    feedback_rules = load_prompt("feedback-rules")

    context = {
        "current_week": current,
        "methodology": {
            "scoring": "六维影响力加权: 行业颠覆性(30%) + 技术突破度(25%) + 生态影响力(20%) + 时间敏感性(15%) + 公众关注度(10%)",
            "pipeline": "多源检索 → 交叉验证 → 影响力加权 → 人工排序 → 深度分析",
        },
        "previous_week": previous,
        "prompts": {
            "deep_analysis": deep_prompt[:500] + "..." if len(deep_prompt) > 500 else deep_prompt,
            "taxonomy": taxonomy[:500] + "..." if len(taxonomy) > 500 else taxonomy,
        },
        "categories": [
            "基础模型", "AI Agent", "开源生态", "政策监管",
            "硬件算力", "AI 安全", "企业动态", "应用落地",
        ],
        "info_sources": {
            "tier1": ["OpenAI 官方", "Anthropic 官方", "Google DeepMind 官方",
                       "Meta AI 官方", "xAI 官方", "Microsoft AI 官方",
                       "Apple 官方", "arXiv", "各国政府公告"],
            "tier2": ["EdgeN", "VentureBeat", "BBC", "36氪", "Economic Times",
                       "Crunchbase", "东方财富", "GitHub Trending", "Hugging Face"],
        },
        "output_format_note": (
            "每个事件输出结构: 事件概述 → 关键数据(3-5条) → 来源渠道 → 未来应用前景 → 对AI发展的影响\n"
            "每个事件前增加信息块: | 时间 | 地点 | 涉及方 |\n"
            "TOP20 后附汇总一览表\n"
            "最后附 3-6 条跨事件趋势洞察"
        ),
    }

    return context


def main():
    import argparse
    parser = argparse.ArgumentParser(description="AI Weekly Digest 报告上下文构建")
    parser.add_argument("--context", action="store_true", help="输出 LLM 生成上下文 JSON")
    parser.add_argument("--week-info", action="store_true", help="仅输出当前周信息")
    parser.add_argument("--check", action="store_true", help="检查数据库状态")
    args = parser.parse_args()

    if args.check:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.execute("SELECT COUNT(*) FROM weekly_reports")
        n = cursor.fetchone()[0]
        print(f"数据库可用 | 已有 {n} 份周报")
        conn.close()

    if args.week_info:
        current = compute_current_week()
        print(json.dumps(current, ensure_ascii=False, indent=2))

    if args.context:
        ctx = build_generation_context()
        print(json.dumps(ctx, ensure_ascii=False, indent=2))

    if not any([args.check, args.week_info, args.context]):
        # 默认: 输出简化的生成任务说明
        ctx = build_generation_context()
        cw = ctx["current_week"]
        print(f"## AI Weekly Digest 生成任务")
        print(f"  周次: {cw['week_number']}")
        print(f"  范围: {cw['week_range']}")
        print(f"  日期: {cw['report_date']}")
        if ctx["previous_week"]:
            pw = ctx["previous_week"]
            print(f"\n  上期: {pw['week_number']} ({pw['week_range']})")
            print(f"  上期 Top 1: {pw['top5'][0]['title']} (⭐{pw['top5'][0]['weight']})")
        print(f"\n  方法: {ctx['methodology']['pipeline']}")
        print(f"  输出: {OUTPUT_DIR}/{cw['week_number']}.md")


if __name__ == "__main__":
    main()
