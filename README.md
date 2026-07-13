# AI 每周发展摘要 (AI Weekly Digest)

> 基于多源检索与深度分析的全球 AI 发展周报，方法论继承自 GitHub Weekly Curation 项目。

## 方法论

采用"自动化采集 + AI 初筛 + 深度分析"的人机协作模式：

1. **多源信息采集：** 覆盖各大 AI 企业官方发布、学术预印本、政府公告、科技媒体、行业数据库
2. **交叉验证去重：** 同一事件在多个独立来源确认后才纳入
3. **六维影响力加权：** 行业颠覆性(30%) + 技术突破度(25%) + 生态影响力(20%) + 时间敏感性(15%) + 公众关注度(10%)
4. **深度分析撰写：** 每个 TOP20 事件按"事件概述 → 关键数据 → 来源渠道 → 应用前景 → 行业影响"结构展开
5. **跨条目趋势洞察：** 识别多个事件指向的共同方向

## 目录结构

```
ai-weekly-digest/
├── README.md               # 本文件
├── prompts/
│   ├── weekly-deep.md       # 每周深度分析 Prompt
│   └── taxonomy.md           # 事件分类体系
├── 2026-W28.md              # 2026年第28周 (07.06-07.12)
└── ...
```

## 信息源体系

### Tier 1: 原始数据源
- OpenAI 官方博客 / API 文档
- Anthropic 官方博客 / Release Notes
- Google DeepMind 官方发布
- Meta AI 官方发布
- xAI 官方发布
- Microsoft AI 官方发布
- Apple 官方发布
- arXiv 预印本 (cs.AI, cs.CL, cs.LG, cs.CR)
- 各国政府官方公告

### Tier 2: 引用数据源
- 科技媒体 (EdgeN, VentureBeat, BBC, 36氪, Economic Times 等)
- 行业数据库 (Crunchbase, 东方财富)
- 开源社区 (GitHub Trending, Hugging Face)
- 行业研究报告 (Morgan Stanley, Bloomberg, Concordia AI, Brookings)

## 分类体系

每期事件按以下维度分类：

| 分类 | 标签 | 说明 |
|------|------|------|
| 基础模型 | `#foundation-model` | LLM 新模型发布、基准测试、能力突破 |
| AI Agent | `#ai-agent` | Agent 框架、自主工作流、多 Agent 协调 |
| 开源生态 | `#open-source` | 开源模型、框架、工具链进展 |
| 政策监管 | `#policy` | 各国 AI 立法、监管行动、出口管制 |
| 硬件算力 | `#hardware` | AI 芯片、数据中心、算力基础设施 |
| AI 安全 | `#ai-safety` | 前沿模型风险、安全研究、攻防态势 |
| 企业动态 | `#enterprise` | AI 企业融资、人才流动、商业策略 |
| 应用落地 | `#application` | AI 在具体行业的部署和应用 |

## 贡献

- 📬 反馈: 通过 GitHub Issues 提交
- 🔄 频率: 每周一发布
