# 智能投资顾问系统

基于本地大模型的QDII基金投资决策辅助系统

## 🎯 系统特点

### 1. 双层分析架构
- **基础技术分析层**：传统技术指标（RSI、MA、动量等）+ 统计分析
- **AI深度分析层**：基于个人投资原则的本地大模型深度分析

### 2. 完全符合个人投资原则
- 严格遵守 `docs/principle.md` 中定义的投资策略
- 场内外基金选择建议
- 止盈止损策略
- 仓位管理建议
- 风险控制提示

### 3. 数据智能管理
- 自动检测数据库中的数据完整性
- 只更新缺失的交易日数据
- 避免重复写入，提高效率

### 4. 本地化部署
- 使用本地 LM Studio 部署的大模型
- 数据隐私完全可控
- 无需依赖云端API

## 📁 文件结构

```
my-trade/
├── qdii-stock-plan.py          # 主程序：数据获取、分析、可视化
├── investment_advisor.py       # 投资建议模块（技术分析 + LLM集成）
├── llm_client.py              # 本地大模型客户端
├── investment_config.py        # 投资策略配置（可选）
├── database_config.py          # 数据库配置
├── test_llm_connection.py     # 测试LLM连接
├── test_qdii_flow.py          # 测试数据流
└── docs/
    ├── principle.md           # 个人投资原则（重要！）
    └── QUICK_START.md         # 快速入门指南
```

## 🚀 快速开始

### 第一步：启动本地大模型

1. 启动 LM Studio
2. 加载模型：`google/gemma-3-27b` 或其他支持的模型
3. 启动服务器，监听在 `10.56.88.6:1234`

### 第二步：测试LLM连接

```bash
cd my-trade
python test_llm_connection.py
```

如果看到 `✅ 连接成功！` 说明LLM已就绪。

### 第三步：运行投资分析

```bash
python qdii-stock-plan.py
```

程序会：
1. 从数据库加载历史数据
2. 检测并补充缺失的交易日数据
3. 执行技术分析
4. 调用本地LLM进行深度分析
5. 输出完整的投资建议
6. 生成可视化图表

## 📊 输出示例

### 基础技术分析
```
📊 市场状态:
  最新价格: 1.2345
  最新涨跌: +2.34%
  近期总收益: +5.67%
  胜率: 56.7% (17/30天上涨)

📈 技术指标:
  RSI(14): 65.4
  5日动量: +3.21%
  相对MA5: +1.23%

📉 趋势分析:
  方向: 上涨 (强度: 强)
  动量: 66.7%

🎯 交易信号:
  信号: 买入
  综合评分: 2.5
  置信度: 62.5%

💰 仓位建议:
  建议仓位 60%
```

### AI深度分析
```
🤖 AI投资顾问深度分析（基于您的投资原则）

【操作建议】强烈买入

【建议仓位】60-70%

【决策理由】
1. 当前为场内QDII基金，符合您"必须购买场内基金"的原则
2. 近期总收益+5.67%，已达到您设定的买入阈值
3. RSI 65.4处于健康区间，未超买
4. 趋势强劲，5日动量+3.21%表明短期势头良好
5. 建议分批建仓，预留30-40%现金应对回调

【风险提示】
- 注意执行"七天止盈"策略
- 设置5-7%的止盈点
- 如遇美股大跌，可考虑分批减仓

【操作计划】
1. 第一批：建仓30%（今日或明日）
2. 第二批：等待回调1-2%再加仓30%
3. 保留40%现金等待更好机会
```

## ⚙️ 配置说明

### 1. 数据库配置 (`database_config.py`)

```python
MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'your_user',
    'password': 'your_password',
    'database': 'your_database',
}
```

### 2. LLM配置 (`llm_client.py`)

```python
API_URL = "http://10.56.88.6:1234/v1/chat/completions"
MODEL = "google/gemma-3-27b"
```

### 3. 投资原则 (`docs/principle.md`)

这是最重要的配置文件！包含：
- 场内外基金选择规则
- 止盈止损策略
- 板块配置原则
- 风险控制要求
- 交易纪律

**强烈建议根据您的实际情况修改此文件！**

### 4. 策略参数 (`investment_advisor.py`)

可以调整技术指标的阈值：
```python
'strong_buy_return': 5.0,   # 强烈买入阈值
'buy_return': 2.0,           # 买入阈值
'sell_return': -3.0,         # 卖出阈值
'high_volatility': 3.0,      # 高波动率阈值
```

## 🔧 高级用法

### 1. 不使用LLM（仅技术分析）

```python
from investment_advisor import InvestmentAdvisor

advisor = InvestmentAdvisor(use_llm=False)
advice = advisor.analyze(df, fund_code)
advisor.print_advice(advice)
```

### 2. 使用自定义配置

```python
custom_config = {
    'strong_buy_return': 10.0,  # 更高的买入阈值
    'sell_return': -5.0,        # 更严格的止损
}

advisor = InvestmentAdvisor(config=custom_config)
```

### 3. 批量分析多个基金

修改 `qdii-stock-plan.py`：
```python
fund_codes = ["513100", "513500", "159920"]
for fund_code in fund_codes:
    df, new_data = get_qdii_fund_data(fund_code, days)
    analyze_fund_performance(df, fund_code, days)
    # ...
```

## 🐛 故障排查

### LLM连接失败

```bash
# 检查LM Studio是否运行
curl http://10.56.88.6:1234/v1/models

# 测试连接
python test_llm_connection.py
```

### 数据库连接问题

```bash
# 检查MySQL服务
mysql -u your_user -p

# 测试数据流
python test_qdii_flow.py
```

### 数据获取失败

可能原因：
1. 网络连接问题
2. AKShare API限制
3. 基金代码错误

程序会自动使用模拟数据演示功能。

## 📚 扩展阅读

- [投资原则文档](docs/principle.md) - 了解系统遵循的投资逻辑
- [快速入门指南](docs/QUICK_START.md) - 5分钟快速上手
- [数据优化说明](docs/QDII_OPTIMIZATION_SUMMARY.md) - 了解数据管理逻辑

## ⚠️ 免责声明

本系统仅供学习和参考使用，不构成任何投资建议。
投资有风险，决策需谨慎。请根据自身情况做出独立判断。

## 🔄 更新日志

### v2.0 (2025-01-25)
- ✅ 集成本地大模型深度分析
- ✅ 基于个人投资原则的AI建议
- ✅ 优化数据库更新逻辑
- ✅ 模块化代码结构
- ✅ 完善文档和测试工具

### v1.0
- ✅ 基础技术分析
- ✅ 数据获取和可视化
- ✅ 数据库存储

## 📞 支持

如有问题或建议，请查看代码注释或提Issue。

---

**Happy Trading! 📈**
