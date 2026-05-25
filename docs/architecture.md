# 🏗️ 架构设计文档

## 设计原则

1. **Schema-first**：所有数据先定义 Schema（JSON Schema），再写数据。Schema 是契约。
2. **领域无关**：核心库不依赖任何特定领域（足球/股票/高考）的代码。领域代码在 examples/ 中。
3. **增量共享**：不要求 "一次到位"。加一条数据源记录、更新一个状态——都是有效贡献。
4. **可验证**：所有数据必须通过 Schema 校验才能合并。

## 核心数据流

```
用户 A（足球分析）  
  贡献：ESPN 数据源档案   ──┐
  贡献：Dongqiudi 踩坑记录 ──┤
                            ├──→ registry/data-sources.json ──→ 用户 B（股票分析）查询
用户 C（股票分析）            │                                      ↓
  贡献：腾讯API 限流记录  ────┘                              知道"这个网站能爬，curl就好"
```

## Schema 生态

```
data-source.schema.json      ← 数据源必须符合此格式
      ↓
parser-recipe.schema.json   ← 解析器配方格式（关联数据源ID）
      ↓
feedback-record.schema.json ← 反馈记录格式（驱动自进化）
      ↓
meta-parameter.schema.json  ← 元参数模式（跨领域通用调参策略）
```

## 领域隔离

```
knowflow-nexus/
├── registry/          ← 共享层（跨领域）
├── examples/          ← 领域示例（供参考）
│   ├── football/      ← 足球领域
│   ├── stock/         ← 股票领域
│   ├── gaokao/        ← 高考领域
│   └── sports/        ← 体育赛事领域
└── schema/            ← 所有Schema（跨领域）
```

## 版本与维护

- 初始版本 v0.1（当前）
- Schema 变更必须 major version bump
- 数据更新不影响版本号
- PR 审核重点：Schema 合规性、信息准确性

## 与 KnowFlow 生态的关系

```
KnowFlow（知识库系统）
   ├── KnowFlow Core（数据持久化、命名空间隔离）
   ├── KnowFlow Dashboard（可视化）
   └── KnowFlow Nexus（← 我们在这里）
         └── 共享知识层：数据源档案 + 解析器 + 元参数
```

Nexus 是 KnowFlow 的"智慧共享层"——独立的模块，但设计理念与 KnowFlow 的命名空间隔离、插件化框架一致。
