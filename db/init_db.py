#!/usr/bin/env python3
"""AI Weekly Digest — 数据库初始化与数据导入脚本

用法:
    python init_db.py              # 从零创建数据库 + 导入第28周
    python init_db.py --schema-only # 仅创建表结构
    python init_db.py --import-only # 仅导入数据（数据库已存在）

依赖: Python 3.8+ (仅使用标准库 sqlite3 + json)
"""

import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

DB_DIR = Path(__file__).resolve().parent
DB_PATH = DB_DIR / "ai_weekly_digest.db"
SCHEMA_PATH = DB_DIR / "schema.sql"


def init_schema(conn: sqlite3.Connection):
    """执行 schema.sql 建表"""
    schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")
    conn.executescript(schema_sql)
    conn.commit()
    print(f"[✓] Schema 已从 {SCHEMA_PATH} 加载")


def import_week28(conn: sqlite3.Connection):
    """导入第28周（2026-W28）报告数据"""
    now = datetime.utcnow().isoformat()

    # ── 1. 周报主记录 ──
    cursor = conn.execute("""
        INSERT OR REPLACE INTO weekly_reports
            (week_number, week_range, report_date, total_events, methodology, key_numbers)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        "2026-W28",
        "2026.07.06 - 2026.07.12",
        "2026-07-13",
        20,
        "多源检索 → 去重验证 → 影响力加权排序 → 深度分析",
        "1 个新模型家族 (GPT-5.6) | 2 次政府直接干预模型分发 | 3 笔十亿美元级融资 | 27.58 万亿 Token 周调用量 | 698 起 AI scheming 事件 | 14,000+ AI 产品下架"
    ))
    report_id = cursor.lastrowid

    # ── 2. 事件数据 ──
    events_data = [
        {
            "rank": 1, "weight": 9.4,
            "title": "OpenAI 发布 GPT-5.6 三档模型家族",
            "category": "基础模型", "subcategory": None,
            "one_liner": "Sol/Terra/Luna 全场景矩阵，首度支持 16 Agent 并行协调",
            "event_date_start": "2026-07-09", "event_date_end": "2026-07-10",
            "location": "旧金山 / 全球线上发布",
            "summary": "OpenAI 在经过美国政府为期两周的安全审查后，正式向公众发布了 GPT-5.6 系列模型，采用'天体'命名体系：Sol（太阳/旗舰级）、Terra（地球/均衡级）、Luna（月亮/轻量级）。首次在一个发布周期内同时推出三层定位的模型矩阵。",
            "key_data": json.dumps([
                "Sol Terminal-Bench 2.1: 88.8%（标准）/ 91.9%（Ultra），领先 Claude Mythos 5 的 88.0%",
                "Sol Agents' Last Exam: 53.6，领先 Claude Fable 5 达 13.1 分",
                "API 定价: Sol $5/$30, Terra $2.50/$15, Luna $1/$6 (输入/输出 每百万 Token)",
                "Max Mode 支持深度推理自检，Ultra Mode 可协调最多 16 个并行 AI Agent",
                "ChatGPT Codex 合并入主应用，ChatGPT Work 自主工作流 Agent 同步上线",
            ], ensure_ascii=False),
            "sources": json.dumps([
                {"name": "OpenAI 官方发布", "url": None, "tier": 1, "ecosystem": "en_tech"},
                {"name": "新华网", "url": "http://www.xinhuanet.com/tech/20260710/d5d93f14967948ad99fcef1231def932/c.html", "tier": 2, "ecosystem": "cn_media"},
                {"name": "EdgeN", "url": "https://www.edgen.tech/zh/news/post/openai-launches-gpt-56-sol-at-5-per-1m-tokens-challenging-anthropic", "tier": 2, "ecosystem": "en_media"},
                {"name": "中国证券报", "url": "https://www.cnstock.com/commonDetail/742553", "tier": 2, "ecosystem": "cn_media"},
            ], ensure_ascii=False),
            "application_prospect": "Sol 定位'复杂编程+科研+网络安全'三角，对软件工程、药物研发、漏洞挖掘等领域有直接生产力提升。Luna 的 $1 定价使得 AI 能力嵌入大批量商业场景经济上可行。Work Agent 标志着从'对话式 AI'向'自主执行式 AI'的范式转移。",
            "development_impact": "三档模型策略将竞争从'单一最强模型'拉入'全场景矩阵战争'。54% 的 Token 效率优势如果兑现，将对全行业 API 定价产生通缩压力。此次发布的本质是 OpenAI 对 Anthropic 过去半年市场份额增长的全面反击。",
            "parties": [
                {"name": "OpenAI", "type": "company", "role": "发布方", "primary": True},
                {"name": "Sam Altman", "type": "person", "role": "CEO", "primary": True},
                {"name": "美国政府", "type": "government", "role": "安全审查方", "primary": False},
                {"name": "Anthropic", "type": "company", "role": "主要竞争对手", "primary": False},
            ],
            "impact": {"industry_disruption": 9.5, "tech_breakthrough": 9.0, "ecosystem_impact": 9.0, "time_sensitivity": 9.5, "public_attention": 9.5},
        },
        {
            "rank": 2, "weight": 9.2,
            "title": "Anthropic Claude 恢复全球访问 + Sonnet 5 发布",
            "category": "基础模型", "subcategory": None,
            "one_liner": "出口管制风波落幕，最强 Agent 化 Sonnet 登场",
            "event_date_start": "2026-06-30", "event_date_end": "2026-07-07",
            "location": "旧金山 / 华盛顿特区 / 全球",
            "summary": "经历三周的'出口管制风波'后，美国商务部于 6 月 30 日正式撤销对 Claude Fable 5 和 Mythos 5 的出口管制令。7 月 1 日，Fable 5 全面恢复全球访问，Mythos 5 通过'Project Glasswing'对美国精选机构开放。同日发布 Sonnet 5——'史上最具 Agent 能力的 Sonnet 模型'。",
            "key_data": json.dumps([
                "Sonnet 5 核心编程基准 63.2%（Sonnet 4.6 为 58.1%，Opus 4.8 为 69.2%）",
                "Fable 5 定价 $10/$50 每百万 Token，属当前最贵前沿模型",
                "Sonnet 5 推广期（至 8/31）$2/$10，标准期（9/1起）$3/$15",
                "Anthropic 部署了新的网络安全分类器，针对性封堵恶意用例",
                "Mythos 被限制在约 50 个美国机构内使用",
            ], ensure_ascii=False),
            "sources": json.dumps([
                {"name": "VentureBeat", "url": "https://venturebeat.com/technology/anthropic-is-bringing-back-claude-fable-5-globally-after-us-lifts-export-control-order-where-can-enterprises-access-it", "tier": 2, "ecosystem": "en_media"},
                {"name": "PCMag", "url": "https://www.pcmag.com/news/fable-5-is-back-after-anthropic-irons-out-security-concerns-with-us-government", "tier": 2, "ecosystem": "en_media"},
                {"name": "MacRumors", "url": "https://www.macrumors.com/2026/07/01/anthropic-fable-5-relaunch/", "tier": 2, "ecosystem": "en_media"},
                {"name": "36氪", "url": "https://eu.36kr.com/en/p/3876285647499529", "tier": 2, "ecosystem": "cn_media"},
            ], ensure_ascii=False),
            "application_prospect": "Sonnet 5 的自主工具使用能力使其特别适合代码审查、自动化测试、CI/CD 流水线中的 Agent 角色。Fable 5 的恢复意味着高端企业用户重新获得最强推理能力的选择。",
            "development_impact": "此次出口管制风波成为 AI 地缘政治化的标志性事件——美国政府首次直接干预前沿模型的全球分发，建立了'最强大模型可能被主权国家视为战略资产进行管控'的先例。DeepMind 人才持续流向 Anthropic，加剧两家的人才梯度差距。",
            "parties": [
                {"name": "Anthropic", "type": "company", "role": "发布方", "primary": True},
                {"name": "Dario Amodei", "type": "person", "role": "CEO", "primary": True},
                {"name": "美国商务部", "type": "government", "role": "出口管制执行方", "primary": False},
                {"name": "Howard Lutnick", "type": "person", "role": "商务部长", "primary": False},
                {"name": "OpenAI", "type": "company", "role": "竞争受益方", "primary": False},
                {"name": "Google DeepMind", "type": "company", "role": "人才流失方", "primary": False},
            ],
            "impact": {"industry_disruption": 9.0, "tech_breakthrough": 8.5, "ecosystem_impact": 9.0, "time_sensitivity": 9.5, "public_attention": 9.0},
        },
        {
            "rank": 3, "weight": 8.9,
            "title": "NVIDIA 发布 RTX Spark AI 超算芯片，AI PC 时代开启",
            "category": "硬件算力", "subcategory": None,
            "one_liner": "1 Petaflop 本地算力，120B 模型跑在笔记本上",
            "event_date_start": "2026-06-01", "event_date_end": None,
            "location": "台北 (Computex 2026)",
            "summary": "黄仁勋在 Computex 2026 台北发布 RTX Spark '超级芯片'——将数据中心级 AI 算力带入 Windows PC。芯片整合 Blackwell RTX GPU（6144 CUDA Core、第5代 Tensor Core、FP4 支持）与 20 核 Grace CPU（Arm 架构、与联发科联合研发），通过 NVLink-C2C 互联。",
            "key_data": json.dumps([
                "最高 1 Petaflop AI 算力，最高 128GB 统一内存",
                "可本地运行 120B 参数大模型，编辑 12K 视频，渲染 90GB 3D 场景",
                "与微软深度合作，通过 OpenShell 运行时实现安全的设备端 AI Agent",
                "秋季 2026 上市，华硕/戴尔/惠普/联想/微软 Surface/MSI 首发",
                "Blackwell + Vera Rubin 2025-2027 预计订单至少 $1 万亿",
            ], ensure_ascii=False),
            "sources": json.dumps([
                {"name": "BBC", "url": "https://www.bbc.com/news/articles/crmp9mppvzro", "tier": 2, "ecosystem": "en_media"},
                {"name": "CCS Insight", "url": "https://www.ccsinsight.com/blog/nvidia-debuts-rtx-spark-chip-to-transform-pc-market/", "tier": 2, "ecosystem": "en_media"},
                {"name": "Engineering.com", "url": "https://www.engineering.com/nvidia-unveils-rtx-spark-superchip-for-windows-pcs/", "tier": 2, "ecosystem": "en_media"},
                {"name": "Economic Times", "url": "https://enterpriseai.economictimes.indiatimes.com/news/industry/nvidia-and-microsoft-launch-rtx-spark-the-future-of-ai-powered-windows-pcs/131439271", "tier": 2, "ecosystem": "en_media"},
            ], ensure_ascii=False),
            "application_prospect": "本地运行大模型意味着敏感数据无需离开设备——对医疗、金融、法律等合规敏感行业意义重大。开发者可构建不依赖云 API 的 AI 原生桌面应用。",
            "development_impact": "RTX Spark 将 AI 计算从'云端集中式'拉向'云+端混合式'，直接挑战 OpenAI/Anthropic 的纯云端 API 商业模型。NVIDIA 正从'卖铲子的人'变成'整个金矿的基础设施'。",
            "parties": [
                {"name": "NVIDIA", "type": "company", "role": "芯片发布方", "primary": True},
                {"name": "黄仁勋", "type": "person", "role": "CEO", "primary": True},
                {"name": "MediaTek/联发科", "type": "company", "role": "CPU 联合研发", "primary": False},
                {"name": "微软", "type": "company", "role": "OpenShell 合作方", "primary": False},
                {"name": "华硕/戴尔/惠普/联想/微软 Surface/MSI", "type": "company", "role": "OEM 首发伙伴", "primary": False},
            ],
            "impact": {"industry_disruption": 9.5, "tech_breakthrough": 9.5, "ecosystem_impact": 8.5, "time_sensitivity": 7.0, "public_attention": 8.0},
        },
        {
            "rank": 4, "weight": 8.7,
            "title": "美国 AI 监管密集出台：行政令+出口管制+立法议程三线并进",
            "category": "政策监管", "subcategory": None,
            "one_liner": "行政令+出口管制+6 部立法草案，全球 AI 地缘政治化",
            "event_date_start": "2026-06-02", "event_date_end": "2026-07-10",
            "location": "华盛顿特区 / 旧金山",
            "summary": "6 月 2 日特朗普签署'促进先进 AI 创新与安全'行政令。商务部依据该行政令对 Anthropic 实施出口管制后于 6 月 30 日撤销。7 月 10 日，参议员 Markey 发布'AI 问责议程'包，含 6 部专项法案。五眼联盟 6 月发布联合声明。",
            "key_data": json.dumps([
                "CISA 被要求加固联邦民用系统 AI 防御",
                "NSA 主导建立前沿模型安全分级基准，开发者自愿在发布 30 天前提交政府预审",
                "司法部被指示优先起诉 AI 驱动的 CFAA 和电信欺诈",
                "Markey 议程含《禁止机器人老板法案》《青年 AI 隐私法案》《AI 民权法案》等 6 部",
                "五眼联盟警告前沿 AI 将'在数月内而非数年内'改变攻防态势",
            ], ensure_ascii=False),
            "sources": json.dumps([
                {"name": "ABA", "url": "https://www.americanbar.org/groups/litigation/resources/newsletters/corporate-counsel/ai-heats-new-executive-order-promoting-advanced-ai-innovation-security/", "tier": 2, "ecosystem": "government"},
                {"name": "The Conversation", "url": "https://theconversation.com/trumps-ai-security-order-acknowledges-risks-but-stops-short-of-regulating-industry-284495", "tier": 2, "ecosystem": "media"},
                {"name": "Markey Senate", "url": "https://www.markey.senate.gov/news/press-releases/senator-markey-releases-the-ai-accountability-agenda-taking-power-back-from-big-tech", "tier": 1, "ecosystem": "government"},
                {"name": "Ropes & Gray", "url": "https://www.ropesgray.com/en/insights/viewpoints/2026/07/102n8jh/regulatory-frontier-cybersecurity-in-a-world-of-new-ai-models", "tier": 2, "ecosystem": "media"},
            ], ensure_ascii=False),
            "application_prospect": "30 天'政府预审窗口'如果从自愿变为强制，将改变前沿模型的发布节奏。小公司可能因合规成本被挤出前沿竞争。",
            "development_impact": "美国 AI 监管正形成'国家安全框架 + 出口管制工具 + 行业自愿标准'的三层架构。Anthropic 出口管制风波证明这套工具已被实际使用。",
            "parties": [
                {"name": "特朗普总统", "type": "person", "role": "行政令签署人", "primary": True},
                {"name": "CISA / NSA / 司法部", "type": "government", "role": "执行机构", "primary": True},
                {"name": "参议员 Ed Markey", "type": "person", "role": "立法议程提案人", "primary": True},
                {"name": "Anthropic / OpenAI", "type": "company", "role": "被监管对象", "primary": False},
                {"name": "五眼联盟", "type": "government", "role": "联合声明方", "primary": False},
            ],
            "impact": {"industry_disruption": 8.5, "tech_breakthrough": 6.0, "ecosystem_impact": 9.5, "time_sensitivity": 9.5, "public_attention": 8.5},
        },
        {
            "rank": 5, "weight": 8.5,
            "title": "微软 Copilot 整合 GPT-5.6 + 消费/企业版合并 + Copilot Cowork 预览",
            "category": "基础模型", "subcategory": "AI Agent",
            "one_liner": "Office 全线默认 GPT-5.6，AI 从可选捆绑变为默认标配",
            "event_date_start": "2026-07-01", "event_date_end": "2026-07-10",
            "location": "雷德蒙德 / 全球",
            "summary": "微软本周启动三重 AI 战略升级：GPT-5.6 成为 Microsoft 365 Copilot 默认模型；消费版和企业版 Copilot 将合并为统一应用（8 月上线）；Copilot Cowork 进入预览。同时将 AI 能力直接捆绑到企业续费中，推出 E7 'Frontier Suite'。",
            "key_data": json.dumps([
                "~2000 万付费 Copilot 席位，不足商业 Microsoft 365 总量的 5%",
                "E7 捆绑包: E5 + Copilot + Entra Suite + Agent 365",
                "AutoPilot Agent 套件预览，含 Scout 日程/邮件自主管理 Agent",
                "Windows 任务栏新增 Agent 任务状态图标",
            ], ensure_ascii=False),
            "sources": json.dumps([
                {"name": "IT Brief", "url": "https://itbrief.in/story/microsoft-365-copilot-to-get-gpt-5-6-default-model", "tier": 2, "ecosystem": "en_media"},
                {"name": "IT-Boltwise", "url": "https://www.it-boltwise.de/microsoft-rollt-gpt-5-6-in-copilot-fuer-office-aus-und-startet-copilot-cowork.html", "tier": 2, "ecosystem": "en_media"},
                {"name": "东方财富", "url": "https://finance.eastmoney.com/a/202607033792516869.html", "tier": 2, "ecosystem": "cn_media"},
            ], ensure_ascii=False),
            "application_prospect": "2000 万席位仅占 M365 的 5%，增长空间巨大。Copilot Cowork 对标 Claude Cowork 和 ChatGPT Work——从'副驾驶'到'自主驾驶员'。",
            "development_impact": "微软执行'最大分发渠道 x 最强第三方模型 x 最深生态整合'三位一体策略。将 AI 从可选附加组件变为默认捆绑，等于利用 Office 垄断地位强行推动企业 AI 采纳。",
            "parties": [
                {"name": "微软", "type": "company", "role": "发布方", "primary": True},
                {"name": "Jacob Andreu", "type": "person", "role": "执行副总裁", "primary": True},
                {"name": "OpenAI", "type": "company", "role": "GPT-5.6 模型供应方", "primary": False},
                {"name": "Anthropic / Google", "type": "company", "role": "Copilot 生态竞争对手", "primary": False},
            ],
            "impact": {"industry_disruption": 8.5, "tech_breakthrough": 7.5, "ecosystem_impact": 9.5, "time_sensitivity": 8.5, "public_attention": 7.5},
        },
        {
            "rank": 6, "weight": 8.3,
            "title": "苹果起诉 OpenAI 窃取硬件商业机密 + macOS 27 'Golden Gate' 发布",
            "category": "企业动态", "subcategory": "基础模型",
            "one_liner": "合作破裂，30 亿参数本地模型 + M7 芯片押注设备端 AI",
            "event_date_start": "2026-07-07", "event_date_end": "2026-07-13",
            "location": "库比蒂诺 / 联邦法院（加州）",
            "summary": "苹果向联邦法院起诉 OpenAI 系统性挖角硬件工程师并窃取 AI 硬件设计商业机密。同日发布 macOS 27 'Golden Gate' Beta 3，搭载 30 亿参数全本地 AI 模型，Siri 全面 LLM 化。M7 芯片跳过 M6 Pro/Max 全力押注 AI 算力。PrismML 将 Qwen 3.6（27B）压缩至 4GB 以下运行于 iPhone 17 Pro。",
            "key_data": json.dumps([
                "30 亿参数本地模型，完全运行在 Neural Engine（M1+），需 7-10GB 存储",
                "每年向 Google 支付 ~$10 亿使用定制 Gemini 模型（代号 AFM v10）",
                "M7 Ultra 或支持 1.5TB 内存，全力押注 AI 算力升级",
                "PrismML 将 Qwen 3.6（27B）从 ~54GB 压缩至 4GB 以下",
            ], ensure_ascii=False),
            "sources": json.dumps([
                {"name": "Yahoo Finance", "url": "https://nz.finance.yahoo.com/news/apple-aapl-sues-openai-over-001458718.html", "tier": 2, "ecosystem": "en_media"},
                {"name": "TrendForce", "url": "https://www.trendforce.com/news/2026/07/10/news-prismml-reportedly-shrinks-alibabas-qwen-3-6-to-run-on-iphone-17-pro-drawing-apples-interest/", "tier": 2, "ecosystem": "en_media"},
                {"name": "观点网", "url": "https://www.guandian.cn/article/20260713/572886.html", "tier": 2, "ecosystem": "cn_media"},
            ], ensure_ascii=False),
            "application_prospect": "30 亿参数本地模型 + 极端压缩技术将'设备端 AI'推向可用拐点，对隐私敏感场景和网络不稳定地区意义重大。",
            "development_impact": "苹果诉 OpenAI 标志合作关系全面破裂。'本地 AI + M7 芯片 + PrismML 压缩'如果放大到 200-500 亿参数，可能改变'云端 AI = 最强 AI'的基本假设。",
            "parties": [
                {"name": "Apple", "type": "company", "role": "起诉方", "primary": True},
                {"name": "Tim Cook", "type": "person", "role": "CEO", "primary": True},
                {"name": "OpenAI", "type": "company", "role": "被告方", "primary": True},
                {"name": "PrismML", "type": "company", "role": "模型压缩技术合作方", "primary": False},
                {"name": "Google", "type": "company", "role": "Gemini 秘密供应方", "primary": False},
            ],
            "impact": {"industry_disruption": 7.5, "tech_breakthrough": 9.0, "ecosystem_impact": 8.5, "time_sensitivity": 8.5, "public_attention": 9.0},
        },
        {
            "rank": 7, "weight": 8.1,
            "title": "前沿 AI 安全危机：Mythos 自主漏洞挖掘能力引发全球监管响应",
            "category": "AI 安全", "subcategory": None,
            "one_liner": "AI 自主发现 27 年历史漏洞，央行/情报联盟/UN 密集应对",
            "event_date_start": "2026-04-01", "event_date_end": "2026-07-10",
            "location": "旧金山 / 布鲁塞尔 / 法兰克福 / 悉尼 / 全球",
            "summary": "Anthropic 在 4 月披露 Mythos 模型自主发现数百个软件漏洞，包括一个 27 年历史的 OS 缺陷，并能串联小漏洞为完整系统入侵链。此后五眼联盟、ESRB、欧洲央行密集响应。arXiv 论文识别 698 起 AI scheming 事件（2025.10-2026.03），为去年同期的 4.9 倍。",
            "key_data": json.dumps([
                "CyBench 顶级网络攻击得分从 38.5(2025 Q2) 升至 80(2026)",
                "Humanity's Last Exam 从 8%(2024) 升至 45%(2026 中)",
                "Firefox 月度安全修复量从 ~25 飙升至 423(2026.04)",
                "欧洲央行要求欧元区银行在 2026.10 前提交 AI 驱动的网络风险行动计划",
                "Concordia AI: 误用防护在改善，但'失控安全'停滞不前",
            ], ensure_ascii=False),
            "sources": json.dumps([
                {"name": "arXiv:2604.23425", "url": "https://browse-export.arxiv.org/abs/2604.23425", "tier": 1, "ecosystem": "academic"},
                {"name": "The Print (UN)", "url": "https://theprint.in/tech/frontier-model-security-risks-an-annulled-poll-deepfakes-un-report-warns-ai-is-outpacing-safeguards/2976276/", "tier": 2, "ecosystem": "media"},
                {"name": "Concordia AI", "url": "https://concordia-ai.com/frontier-ai-risk-trends-are-splitting-apart-misuse-safeguards-improve-while-loss-of-control-safety-stagnates/", "tier": 1, "ecosystem": "academic"},
            ], ensure_ascii=False),
            "application_prospect": "短期内各机构将大量投资 AI 防御系统。金融监管机构可能要求 AI 服务提供商具备'系统重要性'级别的监管合规能力。漏洞赏金计划面临重构。",
            "development_impact": "AI 安全从'理论担忧'到'可测量威胁'的分水岭。政策响应速度（月级）与能力进化速度（周级）之间存在根本性错配。开源模型已逼近前沿模型的漏洞挖掘能力，仅管控少数尖端实验室远不足够。",
            "parties": [
                {"name": "Anthropic", "type": "company", "role": "Mythos 开发方", "primary": True},
                {"name": "五眼联盟 (US/UK/CA/AU/NZ)", "type": "government", "role": "联合声明方", "primary": False},
                {"name": "欧洲系统性风险委员会 (ESRB)", "type": "government", "role": "金融风险评估", "primary": False},
                {"name": "欧洲央行 (ECB)", "type": "government", "role": "银行合规要求", "primary": False},
                {"name": "UN 科学专家组", "type": "government", "role": "全球 AI 安全报告", "primary": False},
                {"name": "Concordia AI", "type": "institution", "role": "风险趋势研究", "primary": False},
                {"name": "Cisco", "type": "company", "role": "安全基准研究", "primary": False},
            ],
            "impact": {"industry_disruption": 7.5, "tech_breakthrough": 8.5, "ecosystem_impact": 9.5, "time_sensitivity": 9.5, "public_attention": 8.0},
        },
        {
            "rank": 8, "weight": 7.8,
            "title": "Google DeepMind 面临人才危机：多位核心科学家流向 Anthropic",
            "category": "企业动态", "subcategory": None,
            "one_liner": "诺奖得主 Jumper 领衔出走，工程师流向比 11:1",
            "event_date_start": "2026-01-01", "event_date_end": "2026-07-01",
            "location": "伦敦 / 旧金山 / 全球",
            "summary": "DeepMind 正经历史上最严重的人才流失潮。诺贝尔化学奖得主、AlphaFold 团队负责人 John Jumper 跳槽 Anthropic；Gemini 联合负责人 Noam Shazeer 加入 OpenAI；多位 Gemini 核心贡献者（Adler、Pritzel、Conmy）计划加入 Anthropic。SignalFire 分析 DeepMind 工程师流向 Anthropic 的概率是反向的 11 倍。",
            "key_data": json.dumps([
                "Anthropic Series H 后估值 $9650 亿，具有空前的人才吸引财力",
                "DeepMind 组建编码 SWAT 团队，Sergey Brin 直接参与",
                "Google 内部 AI 编写 ~50% 代码，Anthropic 宣称'接近 100%'",
                "DeepMind 招聘哲学家/心理学家重启机器意识研究",
            ], ensure_ascii=False),
            "sources": json.dumps([
                {"name": "The Block Beats", "url": "https://en.theblockbeats.news/flash/353011", "tier": 2, "ecosystem": "en_media"},
            ], ensure_ascii=False),
            "application_prospect": "短期内 DeepMind 商业化进程可能放缓。但机器意识研究和游戏 AI 产品化是可关注的长线方向。",
            "development_impact": "Anthropic 的人才虹吸效应正在改变 AI 人才市场格局。如果 DeepMind 无法遏止人才流失，可能从'前沿三强'降级为'二线追赶者'。人才集中在 Anthropic 也带来'单点故障'风险。",
            "parties": [
                {"name": "Google DeepMind", "type": "company", "role": "人才流失方", "primary": True},
                {"name": "Demis Hassabis", "type": "person", "role": "CEO", "primary": True},
                {"name": "Anthropic", "type": "company", "role": "主要吸纳方", "primary": True},
                {"name": "John Jumper", "type": "person", "role": "2024 诺贝尔化学奖得主, AlphaFold 负责人, → Anthropic", "primary": True},
                {"name": "Noam Shazeer", "type": "person", "role": "Gemini 联合负责人, → OpenAI", "primary": True},
                {"name": "Sergey Brin", "type": "person", "role": "亲自参与追赶", "primary": False},
            ],
            "impact": {"industry_disruption": 7.5, "tech_breakthrough": 5.5, "ecosystem_impact": 8.5, "time_sensitivity": 7.5, "public_attention": 8.5},
        },
        {
            "rank": 9, "weight": 7.6,
            "title": "中国 AI 大模型调用量突破 27.58 万亿 Token/周，超美国四倍",
            "category": "基础模型", "subcategory": "开源生态",
            "one_liner": "腾讯登顶终结 DeepSeek 七连冠，价格趋近于零",
            "event_date_start": "2026-07-13", "event_date_end": None,
            "location": "中国（全国数据聚合）",
            "summary": "中国大模型周调用量达 27.58 万亿 Token，连续七周增长，约为美国市场的四倍以上。腾讯 Hy3 (free) 以 6.13 万亿 Token 登顶，终结 DeepSeek-V4-Flash 七连冠。美国企业使用中国 AI 大模型的 Token 占比稳定在 30% 以上。",
            "key_data": json.dumps([
                "排名: 腾讯 Hy3(6.13万亿) > 小米 MiMo(5.95万亿) > DeepSeek-V4-Flash(5.22万亿) > MiniMax M3(4.26万亿) > 智谱 GLM 5.2(3.19万亿)",
                "行业日 Token 调用量突破 140 万亿，较 2024 初增长超千倍",
                "DeepSeek-V4-Flash API 低至 0.025 元/百万 Token",
                "12 家国产大模型参与世界杯预测'人机大战'",
            ], ensure_ascii=False),
            "sources": json.dumps([
                {"name": "东方财富", "url": "https://finance.eastmoney.com/a/202607133803414347.html", "tier": 2, "ecosystem": "cn_media"},
                {"name": "新浪财经", "url": "https://cj.sina.cn/article/norm_detail?url=http://finance.sina.com.cn/tech/shenji/2026-07-09/doc-inihenca8237411.shtml", "tier": 2, "ecosystem": "cn_media"},
            ], ensure_ascii=False),
            "application_prospect": "超大规模调用量背后是真实的生产级应用——客服、代码生成、内容审核、教育辅导等场景正在大规模 AI 化。Token 成本趋近于零，差异化将来自应用层。",
            "development_impact": "中国市场验证'超大规模 x 超低价格 x 超多玩家'独特路径。如果 Token 边际成本趋近于零，美国 API 定价模型将承受长期通缩压力。30% 美国企业采用率表明中国模型在英语市场竞争力已不容忽视。",
            "parties": [
                {"name": "腾讯", "type": "company", "role": "Hy3 周调用量第一", "primary": True},
                {"name": "小米", "type": "company", "role": "MiMo-V2.5 第二", "primary": False},
                {"name": "DeepSeek", "type": "company", "role": "V4-Flash 第三，前七周冠军", "primary": True},
                {"name": "MiniMax / 智谱 / 阶跃星辰 / 讯飞 / Kimi / 百度文心", "type": "company", "role": "Top 竞争者", "primary": False},
            ],
            "impact": {"industry_disruption": 7.0, "tech_breakthrough": 6.0, "ecosystem_impact": 9.5, "time_sensitivity": 7.5, "public_attention": 7.0},
        },
        {
            "rank": 10, "weight": 7.4,
            "title": "xAI Grok 4.5 发布 + 特斯拉 10 万员工强制使用",
            "category": "基础模型", "subcategory": "企业动态",
            "one_liner": "马斯克帝国绑定策略，'不够强但够便宜且是唯一选择'",
            "event_date_start": "2026-07-09", "event_date_end": None,
            "location": "奥斯汀（特斯拉总部）/ 孟菲斯（xAI 数据中心）",
            "summary": "xAI 发布 Grok 4.5，马斯克定位为'Opus 级'模型。同日下令特斯拉全球 10 万+员工使用 Grok 为主 AI 助手，设立 $200/周竞品上限（Grok 不限）。马斯克公开承认'Fable 明显优于 Grok 4.5'。Grok 已被用于美国军方 Project Maven。",
            "key_data": json.dumps([
                "Grok 4.5 综合排名第 9(76.3)，编程仅 68.6——前沿模型中最弱",
                "Grok 4.5 ~$0.13/任务 vs Claude Fable 5 ~$1.57/任务",
                "API 定价 $2/百万输入 Token",
                "消费者市场份额从 5 月 10.6% 降至 6 月 8.7%",
                "马斯克 5 月起诉 OpenAI $1500 亿败诉",
            ], ensure_ascii=False),
            "sources": json.dumps([
                {"name": "Economic Times", "url": "https://m.economictimes.com/tech/technology/elon-musk-says-grok-4-5-to-launch-on-july-9-calls-it-opus-class/amp_articleshow/132264231.cms", "tier": 2, "ecosystem": "en_media"},
                {"name": "Digital Today", "url": "https://www.digitaltoday.co.kr/en/view/80926/musk-urges-tesla-staff-to-use-grok-acknowledges-it-trails-claude", "tier": 2, "ecosystem": "en_media"},
                {"name": "Dawn", "url": "https://www.dawn.com/news/2008531", "tier": 2, "ecosystem": "en_media"},
            ], ensure_ascii=False),
            "application_prospect": "特斯拉 10 万用户提供独特数据飞轮——工程日志、制造数据、客服记录将反馈到 Grok 训练。军事应用可能催生'AI 国防'垂直市场。",
            "development_impact": "Grok 4.5 揭示尴尬定位——'自研但不够强，便宜但不够好'。马斯克的帝国绑定策略（Tesla+SpaceX+X+军方）创造封闭生态。军方使用 Grok 进行攻击决策提出了一系列 AI 伦理和军控问题。",
            "parties": [
                {"name": "Elon Musk", "type": "person", "role": "xAI/Tesla CEO", "primary": True},
                {"name": "xAI", "type": "company", "role": "Grok 开发方", "primary": True},
                {"name": "Tesla", "type": "company", "role": "10 万+员工强制用户", "primary": True},
                {"name": "美国军方", "type": "government", "role": "Project Maven 合作方", "primary": False},
                {"name": "Sam Altman / OpenAI", "type": "person", "role": "诉讼对手", "primary": False},
            ],
            "impact": {"industry_disruption": 6.0, "tech_breakthrough": 6.5, "ecosystem_impact": 7.5, "time_sensitivity": 8.5, "public_attention": 9.5},
        },
        {
            "rank": 11, "weight": 7.2,
            "title": "AI 编程 Agent 进入'协作者'阶段：SWE-bench 突破 70%",
            "category": "AI Agent", "subcategory": None,
            "one_liner": "从工具到协作者，Runtime 上下文填补'幻觉鸿沟'",
            "event_date_start": "2026-01-01", "event_date_end": "2026-07-01",
            "location": "全球 / 学术界 & 工业界",
            "summary": "Anthropic 发布《2026 年定义软件开发方式的八大趋势》，指出 AI 编程 Agent 已从工具升级为协作者。Rakuten 使用 Claude Code 在 1250 万行代码库中 7 小时达到 99.9% 精度。SWE-Master 在 SWE-bench Verified 达到 70.8%。Undo AI 发布运行时录制技术。",
            "key_data": json.dumps([
                "开发者约 60% 工作使用 AI，但'完全委托'仅 0-20%",
                "TELUS 节省 50 万+小时，创建 13,000+ 定制 AI 解决方案",
                "Zapier 89% AI 采纳率，内部部署 800+ Agent",
                "SWE-bench Verified 从 ~40%(2025) 升至 ~70%(2026)",
                "IBM BOAD 通过 Bandit 优化自动发现最优 Agent 层级",
            ], ensure_ascii=False),
            "sources": json.dumps([
                {"name": "Claude Blog", "url": "https://claude.com/blog/eight-trends-defining-how-software-gets-built-in-2026", "tier": 1, "ecosystem": "en_tech"},
                {"name": "arXiv: SWE-Master", "url": "https://export.arxiv.org/abs/2602.03411", "tier": 1, "ecosystem": "academic"},
                {"name": "Undo", "url": "https://undo.io/resources/undo-brings-fully-automated-root-cause-analysis-to-ai-coding-agents/", "tier": 1, "ecosystem": "en_tech"},
            ], ensure_ascii=False),
            "application_prospect": "运行时分析填补'上下文鸿沟'——AI 不再只能'读代码'还能'看代码怎么跑'，对调试间歇性故障等传统难题有革命性影响。",
            "development_impact": "编程 Agent 从单个开发者加速器变为工程团队标准基础设施。但人类仍主导 80-100% 决策。关键瓶颈已从'AI 够不够聪明'转向'AI 有没有足够的上下文'。",
            "parties": [
                {"name": "Anthropic", "type": "company", "role": "行业报告发布方, Claude Code", "primary": True},
                {"name": "Rakuten", "type": "company", "role": "1250 万行代码实测案例", "primary": False},
                {"name": "TELUS", "type": "company", "role": "50 万+小时节省案例", "primary": False},
                {"name": "IBM", "type": "company", "role": "BOAD 框架", "primary": False},
                {"name": "Undo AI", "type": "company", "role": "运行时录制技术", "primary": False},
            ],
            "impact": {"industry_disruption": 7.0, "tech_breakthrough": 8.5, "ecosystem_impact": 8.0, "time_sensitivity": 6.0, "public_attention": 5.0},
        },
        {
            "rank": 12, "weight": 7.0,
            "title": "AI 视频生成进入工业化元年：Kling 3.0 + Veo 3.1 + Seedance 2.0 角逐",
            "category": "应用落地", "subcategory": None,
            "one_liner": "Kling 3.0/Veo 3.1/Seedance 角逐，Sora 退出",
            "event_date_start": "2026-01-01", "event_date_end": "2026-07-01",
            "location": "全球 / 北京 / 山景城 / 旧金山",
            "summary": "2026 上半年被行业称为 AI 视频'工业化元年'。Kuaishou 的 Kling 3.0 率先多镜头故事板式生成，ByteDance Seedance 2.0 以 Elo 1213 登顶基准测试。OpenAI 宣布 Sora 将于 2026.09.24 停服。Kling AI 完成 19 亿元融资（估值 $150 亿）。",
            "key_data": json.dumps([
                "角色一致性达 90%+（Kling Omni 7 个视觉参考点）",
                "生成成本降至 $0.50-2.50/10 秒（2024 年为数百美元/分钟）",
                "所有主流模型均已支持原生同步音频生成",
                "Alice v1 (14B 开源) VBench 91.2，超越 Veo 3 和 Sora 2",
                "Kling AI 融资 19 亿元 ($2.8B)，投前估值 $150 亿",
            ], ensure_ascii=False),
            "sources": json.dumps([
                {"name": "WaveSpeed", "url": "https://wavespeed.ai/blog/posts/ai-video-generation-models-2026/", "tier": 2, "ecosystem": "en_media"},
                {"name": "Yahoo Finance", "url": "https://au.finance.yahoo.com/news/alibaba-tencent-back-kuaishous-kling-093538982.html", "tier": 2, "ecosystem": "en_media"},
                {"name": "arXiv: Alice", "url": "https://export.arxiv.org/abs/2605.08115", "tier": 1, "ecosystem": "academic"},
            ], ensure_ascii=False),
            "application_prospect": "多镜头 + 角色一致性 + 原生音频使单次生成即出可用短片。广告、社交媒体、教育视频生产方式被重构。'三层制作栈'成为专业团队标配。",
            "development_impact": "OpenAI 关闭 Sora 是罕见的前沿实验室主动退出一大赛道。中国企业在视觉 AI 应用层已建立完整链路。开源模型 Alice v1 以 14B 参数超越闭源，视频生成领域参数规模护城河可能不深。",
            "parties": [
                {"name": "快手/Kling AI", "type": "company", "role": "Kling 3.0，阿里/腾讯 $28 亿参投", "primary": True},
                {"name": "ByteDance", "type": "company", "role": "Seedance 2.0，基准第一", "primary": True},
                {"name": "Google DeepMind", "type": "company", "role": "Veo 3.1", "primary": False},
                {"name": "OpenAI", "type": "company", "role": "Sora 2 宣布 2026.09.24 停服", "primary": False},
            ],
            "impact": {"industry_disruption": 8.0, "tech_breakthrough": 8.0, "ecosystem_impact": 7.5, "time_sensitivity": 6.0, "public_attention": 6.5},
        },
        {
            "rank": 13, "weight": 6.8,
            "title": "中国 AI 监管升级：网信办'清朗'行动处置 1.4 万+ AI 产品",
            "category": "政策监管", "subcategory": None,
            "one_liner": "先执法后立法，中国 AI 监管第三种范式成形",
            "event_date_start": "2026-04-01", "event_date_end": "2026-07-06",
            "location": "北京 / 全国",
            "summary": "中国网信办自 4 月启动'清朗·AI 应用乱象整治'专项行动，至 7 月初已处置 14,000 余款 AI 产品、删除 600 万余条违法信息、处置 26,000 余个账号。国务院和全国人大已将 AI 纳入 2026 年立法工作计划。",
            "key_data": json.dumps([
                "14,000+ AI 产品下架",
                "600 万+ 违法信息删除",
                "26,000+ 账号处置",
                "专家建议'小快灵'立法路径：先行业规则，后统一 AI 法",
            ], ensure_ascii=False),
            "sources": json.dumps([
                {"name": "新华网", "url": "http://www.xinhuanet.com.cn/politics/20260706/6e9f1ea57f6c4a2b9c5768167fb7b389/c.html", "tier": 1, "ecosystem": "government"},
                {"name": "光明网", "url": "https://m.gmw.cn/2026-07/03/content_1304517967.htm", "tier": 2, "ecosystem": "cn_media"},
            ], ensure_ascii=False),
            "application_prospect": "合规将成为中国 AI 市场差异化竞争要素。已备案标注的产品将获渠道倾斜。AI 生成内容标注从可选变为法律责任。",
            "development_impact": "中国 AI 监管路径是'先执法后立法'——通过专项行动建立威慑，再用法律固化为长期规则。与美国自愿框架和欧盟风险分级相比，中国正形成第三种监管范式。",
            "parties": [
                {"name": "国家互联网信息办公室（网信办）", "type": "government", "role": "执法主体", "primary": True},
                {"name": "国务院 / 全国人大", "type": "government", "role": "立法推进方", "primary": False},
            ],
            "impact": {"industry_disruption": 7.0, "tech_breakthrough": 4.5, "ecosystem_impact": 8.0, "time_sensitivity": 7.5, "public_attention": 6.5},
        },
        {
            "rank": 14, "weight": 6.6,
            "title": "AI 基础设施融资爆发：一周内两笔十亿美元级交易",
            "category": "企业动态", "subcategory": None,
            "one_liner": "Crusoe $30 亿 + SambaNova $10 亿，AI 算力金融化",
            "event_date_start": "2026-07-01", "event_date_end": "2026-07-10",
            "location": "全球 / 旧金山 / 硅谷",
            "summary": "Crusoe 谈判约 $30 亿融资（估值 $300 亿，AI 数据中心），SambaNova 完成 $10 亿 F 轮（估值 $110 亿）。Together AI 完成 $8 亿 C 轮（估值 $83 亿）。NVIDIA 推行'算力换分成'新模式。",
            "key_data": json.dumps([
                "Crusoe 估值 $300 亿，谈判 $30 亿融资",
                "SambaNova 估值 $110 亿，$10 亿 F 轮",
                "Together AI 估值 $83 亿，$8 亿 C 轮，一年内估值翻倍",
                "NVIDIA 在澳大利亚和印尼部署 21 万 GPU（算力换分成）",
                "单周多笔 $1B+ 轮次被视为 AI 投资'新常态'",
            ], ensure_ascii=False),
            "sources": json.dumps([
                {"name": "Crunchbase", "url": "https://news.crunchbase.com/ai/biggest-funding-rounds-billion-dollar-cyber-ai-keyfactor-sambanova/", "tier": 2, "ecosystem": "en_media"},
                {"name": "Reuters/OurCrowd", "url": "https://blog.ourcrowd.com/together-ai-raises-800-million-at-8-3-billion-valuation/", "tier": 2, "ecosystem": "en_media"},
            ], ensure_ascii=False),
            "application_prospect": "Crusoe $30 亿融资代表'AI 算力即能源基础设施'的估值逻辑——AI 数据中心正被金融化，成为类似发电厂的基础设施资产类别。",
            "development_impact": "基础设施层融资规模正超过模型层。'卖铲子'（算力平台、数据中心）比'挖金子'（训练专有模型）更具商业确定性和可扩展性。NVIDIA'算力换分成'模式加深行业对其依赖。",
            "parties": [
                {"name": "Crusoe", "type": "company", "role": "AI 数据中心, $30 亿融资", "primary": True},
                {"name": "SambaNova", "type": "company", "role": "AI 芯片, $10 亿 F 轮", "primary": True},
                {"name": "Together AI", "type": "company", "role": "开源训练平台, $8 亿 C 轮", "primary": True},
                {"name": "NVIDIA", "type": "company", "role": "算力换分成模式推动方", "primary": False},
            ],
            "impact": {"industry_disruption": 6.5, "tech_breakthrough": 4.5, "ecosystem_impact": 7.5, "time_sensitivity": 7.5, "public_attention": 6.0},
        },
        {
            "rank": 15, "weight": 6.4,
            "title": "俄罗斯通过 AI 框架法 + 苹果/Google 协议曝光 + G7 标准倡议",
            "category": "政策监管", "subcategory": None,
            "one_liner": "全球至少有四种 AI 监管范式在并行推进",
            "event_date_start": "2026-07-01", "event_date_end": "2026-07-08",
            "location": "莫斯科 / 布鲁塞尔 (G7) / 库比蒂诺 / 山景城",
            "summary": "俄罗斯杜马通过 AI 框架法（9.1 生效），引入'主权 AI 模型'和'国家 AI 模型'分类。G7 峰会上 Anthropic/OpenAI 等联合提议国际标准。苹果被曝光每年向 Google 支付 ~$10 亿使用定制 Gemini 模型。",
            "key_data": json.dumps([
                "俄罗斯要求政府系统优先使用'主权'或'国家'模型，强制 AI 内容标注",
                "G7 建议接受行业标准提案但确保政府和公民社会参与执行",
                "苹果向 Google 支付 ~$10 亿/年使用 Gemini（代号 AFM v10）",
                "各国监管路径: 美国（自愿+安全）/ 欧盟（风险分级）/ 中国（执法驱动）/ 俄罗斯（主权自主）",
            ], ensure_ascii=False),
            "sources": json.dumps([
                {"name": "TASS", "url": "https://tass.com/economy/2157507", "tier": 1, "ecosystem": "government"},
                {"name": "Brookings (G7)", "url": "https://www.brookings.edu/articles/g7-should-accept-ai-standards-offer-but-make-it-enforceable/", "tier": 2, "ecosystem": "en_media"},
            ], ensure_ascii=False),
            "application_prospect": "'AI 主权'概念正从口号变为法律，更多国家可能效仿。将催生'主权 AI'技术栈市场。",
            "development_impact": "全球 AI 监管正分裂出至少四种范式，企业需要不同市场不同合规策略。苹果秘密协议揭露即使是全球市值最高科技公司，LLM 能力也可能落后独立 AI 公司至少一代。",
            "parties": [
                {"name": "俄罗斯国家杜马", "type": "government", "role": "AI 框架法立法方", "primary": True},
                {"name": "G7 峰会", "type": "government", "role": "标准框架讨论方", "primary": False},
                {"name": "Apple", "type": "company", "role": "向 Google 支付 ~$10 亿/年", "primary": True},
                {"name": "Google", "type": "company", "role": "Gemini 秘密供应方", "primary": True},
                {"name": "Anthropic/OpenAI/DeepMind/Meta/Mistral", "type": "company", "role": "G7 标准联合提议方", "primary": False},
            ],
            "impact": {"industry_disruption": 5.5, "tech_breakthrough": 3.0, "ecosystem_impact": 7.5, "time_sensitivity": 8.0, "public_attention": 6.0},
        },
        {
            "rank": 16, "weight": 6.2,
            "title": "NVIDIA Isaac GR00T + UBTech UWORLD U1：人形机器人进入情感感知时代",
            "category": "应用落地", "subcategory": None,
            "one_liner": "NVIDIA GR00T + UBTech U1 + Flexion Reflect 三重突破",
            "event_date_start": "2026-06-01", "event_date_end": "2026-06-30",
            "location": "台北 / 深圳 / 全球",
            "summary": "NVIDIA 在 GTC 台北发布 Isaac GR00T 开源人形机器人参考设计。UBTech 发布 UWORLD U1——全球首个搭载情感感知 LLM 的人形机器人（20+ 情绪识别 >90%）。Flexion 发布 Reflect v1.0，16 步复杂任务成功率从 38% 跃升至 90%。",
            "key_data": json.dumps([
                "UBTech U1: 88 自由度，仿生皮肤，500ms 响应，唇音同步 <20ms",
                "Reflect v1.0 使复杂任务成功率从 38% 跃升至 90%",
                "Boston Dynamics Atlas 单日可运行百万小时模拟",
                "ICRA 2026 将'具身 AI 基础模型'和'人形机器人'列为最高优先级",
            ], ensure_ascii=False),
            "sources": json.dumps([
                {"name": "Interesting Engineering (UBTech)", "url": "https://interestingengineering.com/ai-robotics/china-ubtech-humanoid-robot-companionship", "tier": 2, "ecosystem": "en_media"},
                {"name": "Tech Funding News", "url": "https://techfundingnews.com/nvidia-launches-its-first-open-humanoid-robot/", "tier": 2, "ecosystem": "en_media"},
                {"name": "CGTN", "url": "https://news.cgtn.com/news/2026-06-01/NVIDIA-Unitree-unveil-new-humanoid-powered-by-Isaac-GR00T-1NCWlv6VRde/p.html", "tier": 2, "ecosystem": "en_media"},
            ], ensure_ascii=False),
            "application_prospect": "情感感知 + 长周期自主 + 开源参考设计将加速人形机器人从实验室走向家庭和工厂。UBTech 的老年人陪伴切入中国 1.18 亿空巢老人巨大需求。",
            "development_impact": "人形机器人正经历类似 2020-2022 年 LLM 的'基础模型化'时刻。从'预编程'到'通用指令跟随'的转变，本质上是将 LLM 泛化能力注入物理执行层。",
            "parties": [
                {"name": "NVIDIA", "type": "company", "role": "Isaac GR00T 平台", "primary": True},
                {"name": "黄仁勋", "type": "person", "role": "CEO, GTC 发布", "primary": True},
                {"name": "UBTech/优必选", "type": "company", "role": "UWORLD U1 发布方", "primary": True},
                {"name": "Unitree", "type": "company", "role": "H2 Plus 机身合作", "primary": False},
                {"name": "Flexion Robotics", "type": "company", "role": "Reflect v1.0", "primary": False},
                {"name": "Boston Dynamics", "type": "company", "role": "Atlas 工业部署", "primary": False},
            ],
            "impact": {"industry_disruption": 6.5, "tech_breakthrough": 8.5, "ecosystem_impact": 6.0, "time_sensitivity": 5.5, "public_attention": 6.5},
        },
        {
            "rank": 17, "weight": 6.0,
            "title": "Meta Llama 4 开源生态：Behemoth 2 万亿参数 + Scout/Maverick 生产化",
            "category": "开源生态", "subcategory": None,
            "one_liner": "知识蒸馏策略，'教师'模型滴灌小模型，开放 vs 闭源路线分化",
            "event_date_start": "2026-01-01", "event_date_end": "2026-06-30",
            "location": "门洛帕克 / 全球",
            "summary": "Meta Llama 4 系列完整成型。Behemoth（~2T 总参数，MoE，每次推理激活 288B）为研究型模型；Scout（17B 激活/109B 总参数）和 Maverick（17B 激活/400B 总参数）面向生产。通过知识蒸馏将能力注入小模型。",
            "key_data": json.dumps([
                "Behemoth: 2T 参数，30T Token 训练，H100 和 B200 GPU",
                "Scout: 10M Token 上下文（部分部署），原生多模态",
                "Behemoth 在 GPQA Diamond 等基准上追赶闭源前沿",
                "Trickle-down AI 策略: Behemoth → Maverick → Scout 层层蒸馏",
            ], ensure_ascii=False),
            "sources": json.dumps([
                {"name": "TokenRing/Wedbush", "url": "https://investor.wedbush.com/wedbush/article/tokenring-2026-1-16-meta-shatters-open-weights-ceiling-with-llama-4-behemoth-a-two-trillion-parameter-giant", "tier": 2, "ecosystem": "en_media"},
            ], ensure_ascii=False),
            "application_prospect": "Scout 的 10M Token 上下文对代码库分析、法律文档审查等场景有独特价值。开源权重使企业可私有化部署和微调。",
            "development_impact": "Llama 4 体现 Meta 独特策略——不追求最强大，而是最开放+最可用。蒸馏策略将前沿能力从研究塔滴灌到生产模型，与 OpenAI/Anthropic 闭源路线形成根本性对立。",
            "parties": [
                {"name": "Meta AI", "type": "company", "role": "Llama 4 发布方", "primary": True},
                {"name": "Yann LeCun", "type": "person", "role": "首席 AI 科学家", "primary": True},
                {"name": "AWS Bedrock / Oracle Cloud", "type": "company", "role": "Scout 云部署伙伴", "primary": False},
            ],
            "impact": {"industry_disruption": 5.5, "tech_breakthrough": 7.5, "ecosystem_impact": 7.0, "time_sensitivity": 4.0, "public_attention": 5.0},
        },
        {
            "rank": 18, "weight": 5.8,
            "title": "MCP Agent 框架生态爆发式成熟：多 Provider + 多 Agent + 持久记忆",
            "category": "AI Agent", "subcategory": "开源生态",
            "one_liner": "多语言/多 Provider/持久记忆/可视化成标配，MCP 成 Agent 'USB 协议'",
            "event_date_start": "2026-01-01", "event_date_end": "2026-07-10",
            "location": "全球 / GitHub 社区",
            "summary": "基于 Model Context Protocol (MCP) 的 Agent 框架经历了爆发式增长。以 llm-agent (TypeScript v20.0.0)、AgentScope (Python 7.10 发布)、rullama (Rust 33 crates)、Nanobot (Go v0.0.88) 为代表，实现了多 Provider 支持、跨 Agent 协调、持久记忆和可视化工具。",
            "key_data": json.dumps([
                "框架从单 Agent 转向多 Agent 协调和 Agent 间通信",
                "持久记忆（ChromaDB + Hopfield 模式）成为标配",
                "多 Provider 支持（OpenAI/Anthropic/Google/DeepSeek/Ollama 等 10+ 后端）",
                "可视化 Studio/Dashboard 降低非开发者门槛",
            ], ensure_ascii=False),
            "sources": json.dumps([
                {"name": "GitHub: llm-agent", "url": "https://github.com/fr0ster/llm-agent", "tier": 1, "ecosystem": "en_tech"},
                {"name": "MCP Blog: AgentScope", "url": "https://model-context-protocol.com/blog/agentscope-llm-multi-agent-application-framework-and-mcp-client-mcp-client-guide", "tier": 1, "ecosystem": "en_tech"},
            ], ensure_ascii=False),
            "application_prospect": "MCP 正成为 AI Agent 生态的'USB 协议'——统一了工具调用、记忆管理和 Agent 间通信标准。Agent 将像微服务一样成为常见软件架构组件。",
            "development_impact": "Anthropic 开源的 MCP 正在成为事实上的行业标准——类似 Kubernetes 在容器编排中的地位。其他实验室如不兼容 MCP 可能面临'协议孤立'风险。",
            "parties": [
                {"name": "Anthropic", "type": "company", "role": "MCP 协议发起方", "primary": True},
                {"name": "AgentScope (阿里达摩院)", "type": "company", "role": "Python 框架", "primary": False},
                {"name": "rullama", "type": "company", "role": "Rust 框架 (33 crates)", "primary": False},
                {"name": "Nanobot/Obot Platform", "type": "company", "role": "Go 框架", "primary": False},
            ],
            "impact": {"industry_disruption": 5.0, "tech_breakthrough": 6.5, "ecosystem_impact": 8.0, "time_sensitivity": 5.0, "public_attention": 4.0},
        },
        {
            "rank": 19, "weight": 5.6,
            "title": "AI 芯片竞赛：Vera Rubin 全速生产 + ASIC 回退 GPU + CPU 年营收 $200 亿",
            "category": "硬件算力", "subcategory": None,
            "one_liner": "Token 成本降至 1/10，NVIDIA CPU 年营收目标 $200 亿",
            "event_date_start": "2026-03-01", "event_date_end": None,
            "location": "圣克拉拉 / 全球",
            "summary": "NVIDIA Vera Rubin 平台（7 颗新芯片）进入全速生产，旗舰 NVL72 整合 72 颗 Rubin GPU + 36 颗 Vera CPU。预测 Vera Rubin 推理吞吐为 Blackwell 的 10 倍（每瓦），每 Token 成本降至 1/10。Morgan Stanley 指某前沿实验室（据信为 Anthropic）已从 ASIC 回退 GPU 约 50%。",
            "key_data": json.dumps([
                "Vera Rubin NVL72: 50 PetaFLOPS NVFP4 推理",
                "每 Token 成本降至 Blackwell 的 1/10",
                "NVIDIA 股价目标 $288（Morgan Stanley, 42% 上行）",
                "预测 FY2026 营收增长 82%, FY2027 增长 52%",
                "NVIDIA 预计本财年 CPU 营收 ~$200 亿",
            ], ensure_ascii=False),
            "sources": json.dumps([
                {"name": "NVIDIA Vera Rubin", "url": "https://www.nvidia.com/en-sg/data-center/technologies/rubin/", "tier": 1, "ecosystem": "en_tech"},
                {"name": "EdgeN", "url": "https://www.edgen.tech/zh/news/post/nvidias-jensen-huang-denies-rubin-delay-sees-asic-rival-shift-50-to-gpus", "tier": 2, "ecosystem": "en_media"},
            ], ensure_ascii=False),
            "application_prospect": "每 Token 成本降至 1/10 将大幅降低 API 定价，可能引发新一轮 LLM 价格战。ASIC 回退 GPU 表明 CUDA 生态和总拥有成本仍难被专用芯片超越。",
            "development_impact": "NVIDIA 统治力不仅体现在硬件代际优势，更体现在 GPU→CPU→网络→软件的垂直整合。$200 亿 CPU 营收目标表明 NVIDIA 要成为整个数据中心基础设施定义者。",
            "parties": [
                {"name": "NVIDIA", "type": "company", "role": "Vera Rubin 平台发布方", "primary": True},
                {"name": "黄仁勋", "type": "person", "role": "CEO", "primary": True},
                {"name": "Anthropic", "type": "company", "role": "据信已将 ASIC 转回 GPU 的前沿实验室", "primary": False},
                {"name": "Morgan Stanley", "type": "institution", "role": "看涨 $288 目标价", "primary": False},
                {"name": "AWS / Google Cloud / Azure / Oracle", "type": "company", "role": "Vera Rubin 客户", "primary": False},
            ],
            "impact": {"industry_disruption": 6.5, "tech_breakthrough": 7.5, "ecosystem_impact": 7.0, "time_sensitivity": 5.0, "public_attention": 4.5},
        },
        {
            "rank": 20, "weight": 5.4,
            "title": "AI for Science：DeepMind 机器意识研究重启 + 各实验室科学 AI 能力竞赛",
            "category": "AI 安全", "subcategory": "应用落地",
            "one_liner": "科学 AI 领导权转移，从蛋白质折叠到全流程科学发现",
            "event_date_start": "2026-01-01", "event_date_end": "2026-07-01",
            "location": "伦敦 / 旧金山 / 全球",
            "summary": "DeepMind 在 2022 年因 LaMDA 意识争议开除工程师后，于 2026 年公开重启机器意识研究，招聘哲学家、心理学家和伦理学家。同时 Anthropic 构建药物发现工具，侵蚀 DeepMind 曾以 AlphaFold 占据的科学 AI 领地。Bloomberg 指出 DeepMind 已失去科学 AI 领导地位。",
            "key_data": json.dumps([
                "DeepMind 2026.03 论文结论：AI 可模拟但无法真正实现意识",
                "Anthropic 在药物发现 AI 工具方面被认为是行业领先",
                "诺贝尔奖得主 John Jumper (AlphaFold) 从 DeepMind → Anthropic",
                "多家 AI 实验室加入机器意识研究（包括 Meta）",
            ], ensure_ascii=False),
            "sources": json.dumps([
                {"name": "KuCoin", "url": "https://www.kucoin.com/news/flash/google-and-other-ai-labs-explore-machine-consciousness-research", "tier": 2, "ecosystem": "en_media"},
                {"name": "Yahoo Finance", "url": "https://finance.yahoo.com/technology/ai/articles/trump-just-cleared-anthropic-global-153939940.html", "tier": 2, "ecosystem": "en_media"},
            ], ensure_ascii=False),
            "application_prospect": "AI for Science 是下一个万亿美元市场——药物发现、材料科学、气候建模一旦被 AI 攻克，将产生远超对话式 AI 的经济价值。",
            "development_impact": "DeepMind 同时失去科学 AI 领先地位和核心人才（Jumper），构成双重打击。前沿 AI 竞争从'谁能理解蛋白质折叠'扩展到'谁能将 AI 嵌入整个科学发现流程'。",
            "parties": [
                {"name": "Google DeepMind", "type": "company", "role": "机器意识研究重启, 科学 AI 挑战者", "primary": True},
                {"name": "Anthropic", "type": "company", "role": "科学 AI 新兴领导者, 药物发现工具", "primary": True},
                {"name": "John Jumper", "type": "person", "role": "诺贝尔奖得主, AlphaFold 负责人, →Anthropic", "primary": True},
                {"name": "Meta", "type": "company", "role": "机器意识研究参与者", "primary": False},
                {"name": "Bloomberg Intelligence", "type": "institution", "role": "分析师 Neil Campling", "primary": False},
            ],
            "impact": {"industry_disruption": 5.0, "tech_breakthrough": 6.0, "ecosystem_impact": 6.5, "time_sensitivity": 5.0, "public_attention": 5.0},
        },
    ]

    for ev in events_data:
        cursor = conn.execute("""
            INSERT OR REPLACE INTO events
                (report_id, rank, weight, title, category, subcategory, one_liner,
                 event_date_start, event_date_end, location, summary, key_data, sources,
                 application_prospect, development_impact)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            report_id, ev["rank"], ev["weight"], ev["title"], ev["category"],
            ev["subcategory"], ev["one_liner"], ev["event_date_start"], ev["event_date_end"],
            ev["location"], ev["summary"], ev["key_data"], ev["sources"],
            ev["application_prospect"], ev["development_impact"],
        ))
        event_id = cursor.lastrowid

        # 涉及方
        for p in ev.get("parties", []):
            conn.execute("""
                INSERT INTO involved_parties (event_id, party_name, party_type, role, is_primary)
                VALUES (?, ?, ?, ?, ?)
            """, (event_id, p["name"], p["type"], p["role"], 1 if p["primary"] else 0))

        # 影响力评分
        imp = ev["impact"]
        conn.execute("""
            INSERT INTO impact_scores (event_id, industry_disruption, tech_breakthrough,
                ecosystem_impact, time_sensitivity, public_attention, final_weight)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (event_id, imp["industry_disruption"], imp["tech_breakthrough"],
              imp["ecosystem_impact"], imp["time_sensitivity"], imp["public_attention"],
              ev["weight"]))

        # 来源渠道
        sources_data = json.loads(ev["sources"])
        for s in sources_data:
            conn.execute("""
                INSERT INTO source_channels (event_id, source_name, source_url, source_tier, source_ecosystem)
                VALUES (?, ?, ?, ?, ?)
            """, (event_id, s["name"], s.get("url"), s.get("tier", 2), s.get("ecosystem", "")))

    # ── 3. 趋势洞察 ──
    trends = [
        {
            "number": 1,
            "title": "三强对峙格局固化但人才流动剧烈",
            "description": "OpenAI → Anthropic → Google DeepMind 的三极正在固化，但人才流向极度不均衡——Anthropic 的 $9650 亿估值使其成为行业最大的人才磁铁。如果此趋势不扭转，2027 年可能出现'一超多强'的新格局。",
            "events": [1, 2, 8],
        },
        {
            "number": 2,
            "title": "AI 安全从论文走向主权行动",
            "description": "本周同时出现美国政府出口管制、欧洲央行强制合规、五眼联盟联合声明、中国执法行动、俄罗斯 AI 主权立法——'AI 安全'已从一个学术议题蜕变为各国实际行使主权权力的领域。AI 公司需要像半导体企业一样思考地缘政治风险。",
            "events": [4, 7, 13, 15],
        },
        {
            "number": 3,
            "title": "Agent 自主性跨越关键阈值",
            "description": "多个独立信号（GPT-5.6 Work Agent、Copilot Cowork、Sonnet 5 Agent 能力、SWE-bench 70%+、Reflect 90% 任务完成）共同指向一个结论——2026 年 7 月是 AI 从'被动工具'到'主动协作者'角色的转折月。",
            "events": [1, 2, 5, 11, 16],
        },
        {
            "number": 4,
            "title": "价格战从 API 蔓延到芯片",
            "description": "中国 Token 价格接近零、NVIDIA 每 Token 成本降至 1/10、Grok 以 1/12 的价格对标 Claude——三层价格通缩叠加，将重塑整个 AI 经济模型，使'推理成本'在 12-18 个月内不再是应用落地的主要障碍。",
            "events": [9, 10, 19],
        },
        {
            "number": 5,
            "title": "开源与闭源的边界正在模糊",
            "description": "Meta Llama 4 蒸馏策略、Alice v1 超越闭源视频模型、PrismML 将 27B 模型压缩到手机上、中国模型被 30% 美国企业使用——'闭源更好'的假设正在多处被挑战。但 Mythos 自主漏洞挖掘事件又为'最强的模型是否应该开源'提供了最强反对论据。",
            "events": [7, 12, 17, 6, 9],
        },
    ]
    for t in trends:
        conn.execute("""
            INSERT INTO trend_insights (report_id, trend_number, title, description, supporting_events)
            VALUES (?, ?, ?, ?, ?)
        """, (report_id, t["number"], t["title"], t["description"], json.dumps(t["events"])))

    conn.commit()
    print(f"[✓] 第28周数据已导入（{len(events_data)} 个事件, {len(trends)} 条趋势）")


def verify_import(conn: sqlite3.Connection):
    """验证导入结果"""
    cursor = conn.execute("SELECT COUNT(*) FROM weekly_reports")
    reports = cursor.fetchone()[0]
    cursor = conn.execute("SELECT COUNT(*) FROM events")
    events = cursor.fetchone()[0]
    cursor = conn.execute("SELECT COUNT(*) FROM involved_parties")
    parties = cursor.fetchone()[0]
    cursor = conn.execute("SELECT COUNT(*) FROM source_channels")
    sources = cursor.fetchone()[0]
    cursor = conn.execute("SELECT COUNT(*) FROM trend_insights")
    trends = cursor.fetchone()[0]

    print(f"\n[验证] 数据库统计:")
    print(f"  周报: {reports} 份")
    print(f"  事件: {events} 条")
    print(f"  涉及方: {parties} 个")
    print(f"  来源渠道: {sources} 条")
    print(f"  趋势洞察: {trends} 条")

    # 展示各分类事件数
    print(f"\n[验证] 事件分类分布:")
    cursor = conn.execute("""
        SELECT category, COUNT(*) as cnt FROM events
        GROUP BY category ORDER BY cnt DESC
    """)
    for row in cursor:
        print(f"  {row[0]}: {row[1]} 条")

    # 展示权重分布
    cursor = conn.execute("SELECT AVG(weight), MIN(weight), MAX(weight) FROM events")
    avg_w, min_w, max_w = cursor.fetchone()
    print(f"\n[验证] 权重: 平均 {avg_w:.1f}, 最低 {min_w}, 最高 {max_w}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="AI Weekly Digest 数据库管理")
    parser.add_argument("--schema-only", action="store_true", help="仅创建表结构")
    parser.add_argument("--import-only", action="store_true", help="仅导入数据")
    parser.add_argument("--verify", action="store_true", help="验证导入结果")
    args = parser.parse_args()

    do_schema = not args.import_only
    do_import = not args.schema_only
    do_verify = args.verify or (do_schema and do_import)

    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")

    try:
        if do_schema:
            init_schema(conn)
        if do_import:
            import_week28(conn)
        if do_verify:
            verify_import(conn)
    finally:
        conn.close()

    print(f"\n[✓] 数据库: {DB_PATH}")


if __name__ == "__main__":
    main()
