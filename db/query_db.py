#!/usr/bin/env python3
"""AI Weekly Digest — 数据查询与导出工具

用法:
    python query_db.py --stats           # 统计概览
    python query_db.py --week 2026-W28   # 某周完整报告
    python query_db.py --top 5           # 按权重 Top N 事件
    python query_db.py --category 基础模型  # 按分类查询
    python query_db.py --export-json      # 导出 JSON
    python query_db.py --export-csv       # 导出 CSV
"""

import argparse
import csv
import json
import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "ai_weekly_digest.db"


def get_conn():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def show_stats(conn):
    """数据库统计概览"""
    queries = {
        "周报总数": "SELECT COUNT(*) FROM weekly_reports",
        "事件总数": "SELECT COUNT(*) FROM events",
        "涉及方总数": "SELECT COUNT(*) FROM involved_parties",
        "来源总数": "SELECT COUNT(*) FROM source_channels",
        "趋势洞察总数": "SELECT COUNT(*) FROM trend_insights",
        "平均权重": "SELECT ROUND(AVG(weight), 1) FROM events",
    }
    print("\n=== 数据库统计 ===")
    for label, sql in queries.items():
        val = conn.execute(sql).fetchone()[0]
        print(f"  {label}: {val}")

    print("\n=== 事件分类分布 ===")
    rows = conn.execute("""
        SELECT category, COUNT(*) as cnt FROM events
        GROUP BY category ORDER BY cnt DESC
    """).fetchall()
    for r in rows:
        print(f"  {r['category']}: {r['cnt']}")

    print("\n=== 每周事件数 ===")
    rows = conn.execute("""
        SELECT wr.week_number, wr.week_range, COUNT(e.id) as cnt
        FROM weekly_reports wr
        LEFT JOIN events e ON wr.id = e.report_id
        GROUP BY wr.id ORDER BY wr.week_number DESC
    """).fetchall()
    for r in rows:
        print(f"  {r['week_number']} ({r['week_range']}): {r['cnt']} 事件")


def show_week(conn, week_number):
    """展示某周完整报告"""
    report = conn.execute("""
        SELECT * FROM weekly_reports WHERE week_number = ?
    """, (week_number,)).fetchone()
    if not report:
        print(f"未找到周报: {week_number}")
        return

    print(f"\n{'='*70}")
    print(f"  AI 每周发展摘要 | {report['week_number']} ({report['week_range']})")
    print(f"{'='*70}")
    print(f"  生成日期: {report['report_date']}")
    print(f"  关键数字: {report['key_numbers']}")
    print(f"{'='*70}")

    events = conn.execute("""
        SELECT * FROM events WHERE report_id = ? ORDER BY rank
    """, (report['id'],)).fetchall()

    for ev in events:
        print(f"\n{'─'*70}")
        print(f"  #{ev['rank']} ⭐{ev['weight']}  {ev['title']}")
        print(f"  分类: {ev['category']} | 时间: {ev['event_date_start']} ~ {ev['event_date_end'] or '持续中'}")
        print(f"  地点: {ev['location']}")
        print(f"  📌 {ev['one_liner']}")

        # 涉及方
        parties = conn.execute("""
            SELECT * FROM involved_parties WHERE event_id = ? ORDER BY is_primary DESC
        """, (ev['id'],)).fetchall()
        primary = [p for p in parties if p['is_primary']]
        secondary = [p for p in parties if not p['is_primary']]
        print(f"  涉及: {', '.join(p['party_name'] for p in primary)}")
        if secondary:
            print(f"  相关: {', '.join(p['party_name'] for p in secondary)}")

        print(f"\n  {ev['summary']}")

        # 关键数据
        kd = json.loads(ev['key_data'])
        for item in kd[:3]:
            print(f"    • {item}")

        print(f"\n  应用前景: {ev['application_prospect'][:120]}...")
        print(f"  行业影响: {ev['development_impact'][:120]}...")

    # 趋势洞察
    trends = conn.execute("""
        SELECT * FROM trend_insights WHERE report_id = ? ORDER BY trend_number
    """, (report['id'],)).fetchall()
    if trends:
        print(f"\n{'='*70}")
        print(f"  本周趋势洞察")
        print(f"{'='*70}")
        for t in trends:
            print(f"\n  {t['trend_number']}. {t['title']}")
            print(f"     {t['description'][:200]}...")


def show_top(conn, n=10):
    """按权重 Top N"""
    rows = conn.execute("""
        SELECT wr.week_number, e.rank, e.weight, e.title, e.category, e.one_liner
        FROM events e
        JOIN weekly_reports wr ON e.report_id = wr.id
        ORDER BY e.weight DESC
        LIMIT ?
    """, (n,)).fetchall()
    print(f"\n=== 历史 Top {n} 事件（按权重）===")
    for r in rows:
        print(f"  ⭐{r['weight']} [{r['week_number']}] {r['title']} — {r['one_liner']}")


def show_by_category(conn, category):
    """按分类查询"""
    rows = conn.execute("""
        SELECT wr.week_number, e.rank, e.weight, e.title, e.one_liner
        FROM events e
        JOIN weekly_reports wr ON e.report_id = wr.id
        WHERE e.category = ? OR e.subcategory = ?
        ORDER BY e.weight DESC
    """, (category, category)).fetchall()
    print(f"\n=== 分类: {category} ({len(rows)} 条) ===")
    for r in rows:
        print(f"  ⭐{r['weight']} [{r['week_number']}] #{r['rank']} {r['title']}")


def export_json(conn):
    """导出全部数据为 JSON"""
    output = []
    reports = conn.execute("SELECT * FROM weekly_reports ORDER BY week_number DESC").fetchall()
    for report in reports:
        r = dict(report)
        events = conn.execute("""
            SELECT * FROM events WHERE report_id = ? ORDER BY rank
        """, (report['id'],)).fetchall()
        r['events'] = []
        for ev in events:
            e = dict(ev)
            e['key_data'] = json.loads(e['key_data'])
            e['sources'] = json.loads(e['sources'])

            parties = conn.execute("""
                SELECT * FROM involved_parties WHERE event_id = ? ORDER BY is_primary DESC
            """, (ev['id'],)).fetchall()
            e['parties'] = [dict(p) for p in parties]

            impact = conn.execute("""
                SELECT * FROM impact_scores WHERE event_id = ?
            """, (ev['id'],)).fetchone()
            if impact:
                e['impact'] = dict(impact)

            r['events'].append(e)

        trends = conn.execute("""
            SELECT * FROM trend_insights WHERE report_id = ? ORDER BY trend_number
        """, (report['id'],)).fetchall()
        r['trends'] = []
        for t in trends:
            td = dict(t)
            td['supporting_events'] = json.loads(td['supporting_events'])
            r['trends'].append(td)

        output.append(r)

    out_path = Path(__file__).resolve().parent / "export.json"
    out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[✓] 已导出到: {out_path} ({len(output)} 份周报)")


def export_csv(conn):
    """导出事件为 CSV"""
    out_path = Path(__file__).resolve().parent / "events.csv"
    rows = conn.execute("""
        SELECT wr.week_number, e.rank, e.weight, e.title, e.category, e.one_liner,
               e.event_date_start, e.location, e.summary
        FROM events e
        JOIN weekly_reports wr ON e.report_id = wr.id
        ORDER BY wr.week_number DESC, e.rank ASC
    """).fetchall()

    with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["周次", "排名", "权重", "标题", "分类", "一句话", "开始日期", "地点", "概述"])
        for r in rows:
            writer.writerow([r["week_number"], r["rank"], r["weight"], r["title"],
                           r["category"], r["one_liner"], r["event_date_start"],
                           r["location"], r["summary"]])
    print(f"[✓] 已导出到: {out_path} ({len(rows)} 条)")


def main():
    parser = argparse.ArgumentParser(description="AI Weekly Digest 数据查询")
    parser.add_argument("--stats", action="store_true", help="统计概览")
    parser.add_argument("--week", type=str, help="指定周号 (如 2026-W28)")
    parser.add_argument("--top", type=int, help="按权重 Top N")
    parser.add_argument("--category", type=str, help="按分类查询")
    parser.add_argument("--export-json", action="store_true", help="导出 JSON")
    parser.add_argument("--export-csv", action="store_true", help="导出 CSV")
    args = parser.parse_args()

    conn = get_conn()
    try:
        if args.stats:
            show_stats(conn)
        if args.week:
            show_week(conn, args.week)
        if args.top:
            show_top(conn, args.top)
        if args.category:
            show_by_category(conn, args.category)
        if args.export_json:
            export_json(conn)
        if args.export_csv:
            export_csv(conn)
        if not any([args.stats, args.week, args.top, args.category, args.export_json, args.export_csv]):
            show_stats(conn)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
