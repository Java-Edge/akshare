# 🎯 场外基金投资决策系统 - 项目总览

## 📋 项目简介

这是一套完整的场外基金实时估值查询和智能投资决策系统，基于AKShare数据接口，集成了技术分析、投资原则和AI智能建议，帮助您做出更科学的投资决策。

**核心特性：**
- ✅ 实时估值查询（支持所有场外基金）
- ✅ 智能投资建议（基于技术分析和投资原则）
- ✅ AI深度分析（可选，使用本地大模型）
- ✅ 每日监控工具（批量分析自选基金）
- ✅ 完整文档和示例

## 🚀 30秒快速开始

```bash
# 1. 进入项目目录
cd my-trade

# 2. 运行快速示例
python quick_start.py
```

就这么简单！您将看到华夏成长混合基金的实时估值和投资建议。

## 📦 核心文件说明

### 🔑 核心模块

| 文件 | 说明 | 主要功能 |
|------|------|---------|
| `fund_api.py` | 基金API封装 | 查询、搜索、排行 |
| `fund_investment_advisor.py` | 投资建议生成器 | 技术分析、信号生成、AI建议 |
| `llm_client.py` | 本地大模型客户端 | 连接LM Studio提供AI分析 |

### 📊 实用工具

| 文件 | 说明 | 使用场景 |
|------|------|---------|
| `quick_start.py` | ⭐ 快速入门示例 | 第一次使用看这个 |
| `daily_monitor.py` | ⭐ 每日监控工具 | 实战中每天用这个 |
| `fund_query_example.py` | 查询示例 | 学习如何查询基金 |
| `test_system.py` | 系统测试 | 验证功能是否正常 |

### 📖 文档

| 文件 | 说明 |
|------|------|
| `README_FUND_API.md` | API详细文档 |
| `README_FUND_ADVISOR.md` | 系统完整指南 |
| `IMPLEMENTATION_SUMMARY.md` | 实现总结 |
| `docs/skills.md` | 投资原则 |

## 💡 三种使用方式

### 方式1: 快速查询（最简单）

```python
from fund_api import FundAPI

api = FundAPI()
fund_info = api.get_fund_realtime_value("000001")

if fund_info:
    api.print_fund_info(fund_info)
```

**适合：** 快速查看某个基金的实时估值

### 方式2: 获取投资建议（推荐）

```python
from fund_api import FundAPI
from fund_investment_advisor import FundInvestmentAdvisor

api = FundAPI()
advisor = FundInvestmentAdvisor(use_llm=False)

fund_info = api.get_fund_realtime_value("161116")
if fund_info:
    analysis = advisor.analyze_fund(fund_info)
    advisor.print_advice(analysis)
```

**适合：** 获取技术分析和买卖建议

### 方式3: 每日监控（实战推荐）⭐

```bash
# 编辑 daily_monitor.py，添加自选基金
MY_FUNDS = [
    ("000001", "华夏成长混合"),
    ("161116", "易方达黄金主题"),
]

# 运行监控
python daily_monitor.py

# 简要模式（快速查看）
python daily_monitor.py --simple

# 交互查询模式
python daily_monitor.py --interactive
```

**适合：** 每天定时监控自选基金，辅助买卖决策

## 📊 输出示例

### 基金实时估值
```
================================================================================
  📈 基金实时估值信息
================================================================================
  基金代码: 000001
  基金名称: 华夏成长混合
  查询时间: 2026-02-01 21:38:34
--------------------------------------------------------------------------------
  💰 实时估算净值: 1.1806
  📈 实时估算增长率: +0.65% 🔴
--------------------------------------------------------------------------------
  📊 最新公布净值: 1.1670
  📊 最新公布增长率: -0.51%
================================================================================
```

### 投资建议（含AI）
```
================================================================================
  💡 基金投资决策建议
================================================================================
  基金名称: 易方达黄金主题人民币A
  基金代码: 161116
--------------------------------------------------------------------------------
  📊 当前状态: 横盘 ⚪
  💰 实时净值: 2.0366
  📈 涨跌幅: -0.03%
  ⚠️  风险等级: 低风险
--------------------------------------------------------------------------------
  🎯 交易信号: 买入 (可建仓)
--------------------------------------------------------------------------------
  🤖 AI深度分析:
  **市场判断**：黄金横盘，低风险。
  **操作建议**：买入并适度建仓，因基金属贵金属类且交割日历未出现紧迫到期，
                持有可捕捉潜在回升。
  **风险提示**：关注美元波动及宏观通胀预期，防止突发政策冲击。
================================================================================
```

## 🎓 投资原则（核心理念）

系统遵循以下经过验证的投资原则（docs/skills.md）：

| 原则 | 说明 | 应用 |
|------|------|------|
| **不追涨杀跌** | 上涨时不急于买入，下跌时不急于卖出 | 系统在大涨时给出"持有"建议 |
| **红的才卖** | 盈利时考虑止盈，亏损时耐心持有 | 系统判断盈亏状态给建议 |
| **及时止损** | 方向错了要认错，沉没成本不参与决策 | 系统识别趋势反转信号 |
| **理性预期** | 不幻想买在最低卖在最高 | 系统给出合理的操作区间 |

## 🔧 高级功能

### 启用AI深度分析

1. 安装并启动LM Studio
2. 加载模型（推荐：google/gemma-3-27b）
3. 确保服务运行在 `http://10.56.88.6:1234`
4. 使用时设置 `use_llm=True`：

```python
advisor = FundInvestmentAdvisor(use_llm=True)
```

### 自定义投资原则

编辑 `docs/skills.md`，添加你的投资理念，AI会自动应用。

### 批量分析和导出

```python
from fund_api import FundAPI
from fund_investment_advisor import FundInvestmentAdvisor
import json

api = FundAPI()
advisor = FundInvestmentAdvisor(use_llm=True)

funds = ["000001", "161116", "110022"]
results = []

for code in funds:
    info = api.get_fund_realtime_value(code)
    if info:
        analysis = advisor.analyze_fund(info)
        results.append(analysis)

# 保存为JSON
with open('analysis.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
```

## 📈 实战操作流程（推荐）

### 每日操作

```bash
# 1. 早盘前（9:00前）- 快速查看
python daily_monitor.py --simple

# 2. 盘后（15:00后）- 详细分析
python daily_monitor.py

# 3. 根据建议做出决策
```

### 周末复盘

1. 回顾本周操作
2. 更新自选基金列表（`daily_monitor.py`中的`MY_FUNDS`）
3. 调整投资策略

## ⚠️ 重要提示

1. **数据时效性**：实时估值仅交易日更新，非交易时间显示"---"
2. **仅供参考**：所有建议仅供参考，不构成投资建议
3. **风险自负**：基金投资有风险，投资需谨慎
4. **理性决策**：结合自身情况，不盲目跟从

## 🐛 常见问题

### Q: 提示"无法获取基金数据"？
**A**: 检查基金代码是否正确（6位数字），是否为场外基金。

### Q: AI分析不可用？
**A**: 检查LM Studio是否启动，或设置 `use_llm=False` 使用基础分析。

### Q: 显示"---"是什么意思？
**A**: 该数据项暂无数据，可能是非交易时间或基金暂停估值。

### Q: 如何添加自选基金？
**A**: 编辑 `daily_monitor.py`，在 `MY_FUNDS` 列表中添加基金代码和名称。

## 📚 学习路径

1. **第一步**：运行 `quick_start.py` 了解基本功能
2. **第二步**：阅读 `README_FUND_API.md` 学习API用法
3. **第三步**：配置 `daily_monitor.py` 开始每日监控
4. **第四步**：阅读 `README_FUND_ADVISOR.md` 掌握高级功能
5. **第五步**：学习 `docs/skills.md` 理解投资原则

## 🎯 支持的基金类型

- ✅ 开放式基金（股票型、混合型、债券型）
- ✅ QDII基金
- ✅ LOF基金
- ✅ ETF联接基金
- ❌ 场内交易的ETF（需使用其他API）

## 🔗 相关资源

- AKShare文档：https://akshare.akfamily.xyz/
- LM Studio：https://lmstudio.ai/
- CME交割日历：https://www.cmegroup.com/cn-s/markets/metals/precious/gold.calendar.html

## 📝 版本历史

- **v1.0** (2025-02-01) - 初始版本
  - 基金实时估值查询
  - 投资建议生成
  - AI深度分析
  - 每日监控工具

## 🙏 致谢

- AKShare 提供数据接口
- LM Studio 提供本地大模型支持

## 📄 许可证

MIT License

---

**开始您的智能投资之旅！** 🚀

有问题欢迎提Issue，祝投资顺利！💰
