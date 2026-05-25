# 🤝 贡献指南

## 我能贡献什么？

### 1. 📡 添加数据源

你发现了一个新网站/API，可以获取预测所需的数据？

1. 参考 `schema/data-source.schema.json` 了解格式要求
2. 按格式写一条记录
3. 添加到 `registry/data-sources.json` 数组中
4. 提交 PR

**示例（最小记录）：**
```json
{
  "id": "my-new-source",
  "name": "My New Source",
  "name_cn": "我的新数据源",
  "url": "https://example.com/api",
  "type": "json-api",
  "accessibility": {
    "status": "verified-working",
    "last_verified": "2026-05-25",
    "verified_by": "your-github-username"
  },
  "method": {
    "recommended": "curl",
    "auth_required": false,
    "rate_limit": "未知",
    "encoding": "utf-8"
  },
  "domains": ["football"]
}
```

### 2. 🔧 更新数据源状态

某个数据源挂了？或者某网站改版了？

```json
{
  "id": "espn-soccer-squad",
  "accessibility": {
    "status": "verified-broken",  // 从 verified-working 改为 verified-broken
    "last_verified": "2026-06-01",
    "verified_by": "your-github-username",
    "notes": "ESPN改版，页面结构变化，旧解析器失效"
  }
}
```

直接修改 `registry/data-sources.json` 中对应 ID 的记录的 `accessibility` 字段即可。

### 3. 🧩 贡献解析器配方

你写了一个从某类网页提取数据的解析器？

1. 参考 `schema/parser-recipe.schema.json` 格式
2. 添加到 `registry/parser-recipes.json`
3. 在代码片段中提供实际可用的提取代码

### 4. 📝 添加踩坑记录

踩了坑就不要让别人再踩。

在某个数据源的 `known_issues` 字段中添加你的经验：
```json
"known_issues": [
  "原有坑: 部分球队显示超过26人",
  "新增坑: 2026年6月起需要Cookie，否则返回403"
]
```

### 5. 🧪 贡献元参数模式

你发现了一个跨领域通用的调参策略？

1. 参考 `schema/meta-parameter.schema.json`
2. 添加到 `registry/meta-parameters.json`

### 6. 🌐 添加新领域示例

你在天气预测、旅游推荐、房价分析等其他领域复用了本知识库？

1. 创建 `examples/{你的新领域}/` 目录
2. 写一个 `your-example.json`，描述你所用到的共享知识
3. 提交 PR

## PR 流程

1. Fork 本仓库
2. 创建分支：`feature/add-new-source` 或 `fix/update-status`
3. 修改后运行验证：
   ```bash
   python3 scripts/validate.py registry/data-sources.json
   python3 scripts/validate.py registry/parser-recipes.json
   ```
4. 提交 PR 并描述你做了什么、为什么做

## 质量标准

- 所有新增数据必须通过 Schema 验证
- 数据源状态必须标注：`last_verified`（日期）+ `verified_by`（身份）
- 尽量使用中文 name_cn（面向中文用户）
- 贡献代码片段建议使用 Python（最通用的预测工具语言）

## 行为准则

- 尊重别人的踩坑记录——即使你认为某个数据源很好用，如果别人标注了 "broken"，请先验证再修改
- 不共享敏感信息——不要在示例代码中包含真实 Cookie 或 API Key
- 遇到争论先看 Schema——Schema 是契约，先确保数据符合格式，再讨论格式本身
