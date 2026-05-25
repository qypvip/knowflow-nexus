# 🌐 KnowFlow Nexus — 预测系统的共享知识库

> **像一个"Wikipedia + 数据源地图 + 方法论引擎"的综合体。**

KnowFlow Nexus 是一个开源共享的**预测系统知识库**。它不提供某个具体领域的预测模型，而是提供**所有预测系统共用的底层知识**：

- 📡 **数据源档案**：哪个网站能爬、怎么爬、有什么坑
- 🧩 **解析器配方**：从特定类型网页提取数据的标准代码
- 🧪 **元参数模式**：跨领域通用的调参策略
- 🔄 **自进化框架**：预测→复盘→调参的闭环标准
- 🧠 **多Agent协作模式**：并行分析+裁决的标准流程
- 🔌 **基础设施绑定**：IMA同步、QQ推送、数据持久化

## 🎯 核心思想

> **特斯拉的数据飞轮：** 200万辆车的驾驶数据 → 模型变准 → 车更好卖 → 更多数据
>
> **KnowFlow Nexus 的元知识飞轮：** N个用户的预测经验 → 数据源档案更准 → 更多人用 → 更多反馈

我们不共享"这个比分是多少"（领域特定），我们共享"这个网站能爬不能爬、用什么方式"（跨领域通用）。

## 🏗️ 项目结构

```
knowflow-nexus/
├── schema/                      # 数据格式标准 (JSON Schema)
│   ├── data-source.schema.json  #   数据源档案格式
│   ├── parser-recipe.schema.json#   解析器配方格式
│   ├── feedback-record.schema.json# 反馈记录格式
│   └── meta-parameter.schema.json # 元参数模式格式
│
├── registry/                    # 数据注册表（实际数据）
│   ├── data-sources.json        #   数据源档案库（全部已知数据源）
│   ├── parser-recipes.json      #   解析器配方库
│   └── meta-parameters.json     #   元参数模式库
│
├── examples/                    # 各领域示例
│   ├── football/
│   ├── stock/
│   ├── gaokao/
│   └── sports/
│
├── scripts/                     # 验证和工具脚本
│   └── validate.py              #   Schema校验工具
│
└── docs/                        # 文档
    ├── architecture.md          #   架构设计文档
    └── contribution-guide.md    #   贡献指南
```

## 📋 数据源档案（17个已收录）

| 数据源 | 类型 | 状态 | 适用领域 |
|--------|------|------|---------|
| **ESPN 球队名单** | 服务端HTML | ✅ 已验证 | 足球/体育 |
| **懂球帝 Mobile API** | JSON API | ✅ 已验证 | 足球 |
| **腾讯财经行情API** | 文本API | ✅ 已验证 | 股票 |
| **腾讯历史K线API** | JSON API | ✅ 已验证 | 股票 |
| **Efinance Python包** | Python库 | ⚠️ 部分可用 | 股票 |
| **新浪财经API** | JSON API | ✅ 已验证 | 股票 |
| **阳光高考网** | WAF | ❌ 不可用 | 高考 |
| **夸克高考** | SPA | ⚠️ 勉强可用 | 高考 |
| **必应搜索(CDP)** | CDP | ✅ 已验证 | 全领域 |
| **百度百科** | 验证码 | ❌ 不可用 | 全领域 |
| **维基百科** | 连接重置 | ❌ 不可用 | 全领域 |
| **教育部官网** | 空响应 | ❌ 不可用 | 高考 |
| **河北教育考试院** | 服务端HTML | ⚠️ 待验证 | 高考 |
| **澎湃新闻** | 服务端HTML | ⚠️ 部分可用 | 教育/新闻 |
| **中国教育在线** | 服务端HTML | ✅ 已验证 | 教育 |
| **GitHub** | 连接重置 | ❌ 不可用 | 通用 |
| **Gitee** | 服务端HTML | ✅ 已验证 | 通用 |

> ⚠️ 数据源的可用性随时间变化。欢迎提 PR 更新数据源状态！

## 🚀 快速开始

```bash
# 克隆
git clone https://github.com/qypvip/knowflow-nexus.git
cd knowflow-nexus

# 查看所有数据源
cat registry/data-sources.json | jq '.[].name'

# 查找某个领域可用的数据源
cat registry/data-sources.json | jq '.[] | select(.domains | index("stock")) | {name, type, accessibility}'

# 验证数据格式
python3 scripts/validate.py registry/data-sources.json
```

## 🤝 如何贡献

7 种贡献方式，总有一种适合你：

1. **📡 添加数据源**：发现了一个新网站可用？加一条记录到 `data-sources.json`
2. **🔧 更新状态**：某个数据源挂了？更新 `accessibility.status`
3. **🧩 贡献解析器**：写了一个提取器？加到 `parser-recipes.json`
4. **📝 添加踩坑记录**：踩了一个坑？加到 `known_issues`
5. **🧪 贡献元参数**：发现一个新的跨领域调参模式？加到 `meta-parameters.json`
6. **🌐 添加示例**：在其他领域（天气、房价、体育赛事）复用了本知识库？
7. **📖 改进文档**：翻译、补充、纠错

详见 [贡献指南](docs/contribution-guide.md)

## 📜 协议

MIT License — 自由使用、修改、商用。

## 🏠 国内镜像

- GitHub: https://github.com/qypvip/knowflow-nexus
- Gitee: https://gitee.com/qypvip/knowflow-nexus
