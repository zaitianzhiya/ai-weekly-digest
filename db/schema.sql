-- AI Weekly Digest 数据库 Schema
-- 存储每周 AI 事件的结构化数据

-- 周报主表
CREATE TABLE IF NOT EXISTS weekly_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    week_number TEXT NOT NULL,              -- 如 "2026-W28"
    week_range TEXT NOT NULL,               -- 如 "2026.07.06 - 2026.07.12"
    report_date TEXT NOT NULL,              -- 生成日期 ISO 格式
    total_events INTEGER NOT NULL,
    methodology TEXT,
    key_numbers TEXT,                       -- 本周关键数字摘要
    created_at TEXT DEFAULT (datetime('now')),
    UNIQUE(week_number)
);

-- 事件表
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_id INTEGER NOT NULL,
    rank INTEGER NOT NULL,                  -- 排名 1-20
    weight DECIMAL(3,1) NOT NULL,           -- 权重评分 1.0-10.0
    title TEXT NOT NULL,                    -- 事件标题
    category TEXT NOT NULL,                 -- 主分类
    subcategory TEXT,                       -- 子分类（可选）
    one_liner TEXT NOT NULL,                -- 一句话要点
    event_date_start TEXT NOT NULL,         -- 事件发生开始日期
    event_date_end TEXT,                    -- 事件发生结束日期
    location TEXT,                          -- 发生地点（城市/国家）
    summary TEXT,                           -- 事件概述 (2-3句)
    key_data TEXT,                          -- 关键数据（JSON 数组）
    sources TEXT,                           -- 来源渠道（JSON 数组）
    application_prospect TEXT,              -- 未来应用前景
    development_impact TEXT,                -- 对 AI 发展的影响
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (report_id) REFERENCES weekly_reports(id),
    UNIQUE(report_id, rank)
);

-- 涉及方表
CREATE TABLE IF NOT EXISTS involved_parties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    party_name TEXT NOT NULL,               -- 公司/人物名称
    party_type TEXT NOT NULL,              -- 'company' | 'person' | 'government' | 'institution'
    role TEXT,                             -- 角色描述 (如 "CEO", "开发方", "审查方")
    is_primary BOOLEAN DEFAULT 0,          -- 是否为主要涉及方
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
);

-- 来源渠道表
CREATE TABLE IF NOT EXISTS source_channels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    source_name TEXT NOT NULL,              -- 来源名称
    source_url TEXT,                        -- URL
    source_tier INTEGER DEFAULT 2,          -- 1=原始源, 2=引用源
    source_ecosystem TEXT,                  -- 'en_tech' | 'cn_tech' | 'academic' | 'government' | 'media'
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
);

-- 趋势洞察表
CREATE TABLE IF NOT EXISTS trend_insights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_id INTEGER NOT NULL,
    trend_number INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    supporting_events TEXT,                 -- 支持该趋势的事件编号（JSON 数组，如 [1,5,11]）
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (report_id) REFERENCES weekly_reports(id),
    UNIQUE(report_id, trend_number)
);

-- 影响力评分明细表（每个事件的各维度得分）
CREATE TABLE IF NOT EXISTS impact_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    industry_disruption DECIMAL(3,1),       -- 行业颠覆性 (0-10)
    tech_breakthrough DECIMAL(3,1),         -- 技术突破度 (0-10)
    ecosystem_impact DECIMAL(3,1),          -- 生态影响力 (0-10)
    time_sensitivity DECIMAL(3,1),          -- 时间敏感性 (0-10)
    public_attention DECIMAL(3,1),          -- 公众关注度 (0-10)
    final_weight DECIMAL(3,1),              -- 最终权重
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    UNIQUE(event_id)
);

-- 分类表（维度字典）
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,              -- 主分类名
    tag TEXT,                               -- 标签如 '#foundation-model'
    description TEXT,
    sort_order INTEGER DEFAULT 0
);

-- 初始化分类数据
INSERT OR IGNORE INTO categories (name, tag, description, sort_order) VALUES
    ('基础模型', '#foundation-model', 'LLM/多模态新模型发布、基准测试、能力突破、API 定价', 1),
    ('AI Agent', '#ai-agent', 'Agent 框架、自主工作流、MCP 生态、多 Agent 协调', 2),
    ('开源生态', '#open-source', '开源模型权重、开源框架、社区项目、许可证变更', 3),
    ('政策监管', '#policy', 'AI 立法、监管行动、出口管制、政府行政令、国际标准', 4),
    ('硬件算力', '#hardware', 'AI 芯片、GPU、数据中心、算力基础设施、芯片制造', 5),
    ('AI 安全', '#ai-safety', '前沿模型风险、安全研究、网络攻防、对齐、可解释性', 6),
    ('企业动态', '#enterprise', 'AI 企业融资、人才流动、收购、IPO、商业策略', 7),
    ('应用落地', '#application', '行业 AI 部署、垂直场景、生产级应用、ROI 数据', 8);

-- 索引
CREATE INDEX IF NOT EXISTS idx_events_report_id ON events(report_id);
CREATE INDEX IF NOT EXISTS idx_events_category ON events(category);
CREATE INDEX IF NOT EXISTS idx_events_weight ON events(weight DESC);
CREATE INDEX IF NOT EXISTS idx_involved_parties_event ON involved_parties(event_id);
CREATE INDEX IF NOT EXISTS idx_source_channels_event ON source_channels(event_id);
CREATE INDEX IF NOT EXISTS idx_trend_insights_report ON trend_insights(report_id);
CREATE INDEX IF NOT EXISTS idx_impact_scores_event ON impact_scores(event_id);

-- 查询视图：完整事件详情
CREATE VIEW IF NOT EXISTS v_event_full AS
SELECT
    wr.week_number,
    wr.week_range,
    e.rank,
    e.weight,
    e.title,
    e.category,
    e.one_liner,
    e.event_date_start,
    e.event_date_end,
    e.location,
    e.summary,
    e.key_data,
    e.application_prospect,
    e.development_impact,
    isc.industry_disruption,
    isc.tech_breakthrough,
    isc.ecosystem_impact,
    isc.time_sensitivity,
    isc.public_attention
FROM events e
LEFT JOIN weekly_reports wr ON e.report_id = wr.id
LEFT JOIN impact_scores isc ON e.id = isc.event_id
ORDER BY wr.week_number DESC, e.rank ASC;
