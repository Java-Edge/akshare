# 投资建议模块使用指南

## 📚 模块说明

投资建议模块是一个独立的、可扩展的投资决策系统，专门用于分析QDII基金数据并提供买卖决策建议。

### 核心文件

| 文件名 | 说明 |
|--------|------|
| `investment_advisor.py` | 核心投资建议引擎 |
| `investment_config.py` | 策略配置管理 |
| `investment_examples.py` | 使用示例 |

---

## 🚀 快速开始

### 1. 基础使用

```python
from investment_advisor import quick_advice
import pandas as pd

# 假设你已经有了基金数据 df
advice = quick_advice(df, fund_code='513100')
```

### 2. 使用预设策略

```python
from investment_advisor import quick_advice
from investment_config import get_strategy_config

# 获取激进策略配置
config = get_strategy_config('aggressive')

# 生成投资建议
advice = quick_advice(df, fund_code='513100', config=config)
```

### 3. 集成到现有代码

在 `qdii-stock-plan.py` 中已经自动集成，运行即可：

```bash
python qdii-stock-plan.py
```

---

## 📊 预设策略

### 1. 激进策略 (aggressive)
- **适用对象**: 风险承受能力强的投资者
- **特点**: 追求高收益，能承受较大波动
- **买入阈值**: 1% 就考虑买入
- **卖出阈值**: -2% 才卖出
- **最大仓位**: 100%

### 2. 稳健策略 (balanced) ⭐ 默认
- **适用对象**: 平衡型投资者
- **特点**: 平衡收益与风险
- **买入阈值**: 2% 考虑买入
- **卖出阈值**: -3% 考虑卖出
- **最大仓位**: 80%

### 3. 保守策略 (conservative)
- **适用对象**: 风险厌恶型投资者
- **特点**: 追求稳定，规避风险
- **买入阈值**: 4% 才考虑买入
- **卖出阈值**: -2% 就卖出
- **最大仓位**: 60%

### 4. 短线策略 (daytrader)
- **适用对象**: 短线交易者
- **特点**: 快进快出，对短期波动敏感
- **买入阈值**: 0.5% 考虑买入
- **卖出阈值**: -1% 考虑卖出
- **最大仓位**: 100%

### 5. 长线策略 (longterm)
- **适用对象**: 价值投资者
- **特点**: 长期持有，忽略短期波动
- **买入阈值**: 5% 考虑买入
- **卖出阈值**: -5% 考虑卖出
- **最小仓位**: 60%

---

## 🎯 核心功能

### 1. 多维度技术分析

- **基础统计**: 总收益、日均收益、波动率、胜率等
- **技术指标**: RSI、移动平均线(MA5/10/20)、动量等
- **趋势分析**: 上涨/下跌/震荡，强度评估
- **风险评估**: 低/中/高/极高风险等级

### 2. 交易信号生成

基于多维度评分系统，生成5级交易信号：

| 信号 | 含义 | 评分范围 |
|------|------|----------|
| 强烈买入 | 市场强势，建议积极买入 | ≥3分 |
| 买入 | 市场向好，建议适量买入 | 1.5-3分 |
| 持有 | 观望为主，保持现有仓位 | -1.5-1.5分 |
| 卖出 | 市场走弱，建议减仓 | -3--1.5分 |
| 强烈卖出 | 市场很差，建议大幅减仓 | ≤-3分 |

### 3. 仓位建议

根据信号强度、风险等级和置信度，动态调整仓位建议（0-100%）

### 4. 具体操作建议

提供具体的买入/卖出/持有建议，以及详细的理由分析

---

## 🔧 自定义配置

### 方法1: 使用配置文件

```python
from investment_config import create_custom_strategy

# 创建自定义策略
my_strategy = create_custom_strategy(
    name="我的策略",
    strong_buy=4.0,    # 4%强烈买入
    buy=1.5,           # 1.5%买入
    sell=-2.5,         # -2.5%卖出
    strong_sell=-4.5,  # -4.5%强烈卖出
    max_pos=90,        # 最大仓位90%
    min_pos=15         # 最小仓位15%
)

# 使用自定义策略
advice = quick_advice(df, fund_code='513100', config=my_strategy)
```

### 方法2: 直接传入配置字典

```python
custom_config = {
    'strong_buy_return': 3.0,
    'buy_return': 1.0,
    'sell_return': -2.0,
    'strong_sell_return': -4.0,
    'high_volatility': 3.5,
    'medium_volatility': 2.0,
    'low_volatility': 1.0,
    'trend_days': 7,
    'momentum_threshold': 0.65,
    'max_position': 85,
    'min_position': 15,
}

advice = quick_advice(df, config=custom_config)
```

---

## 📈 高级用法

### 1. 获取详细分析结果

```python
from investment_advisor import InvestmentAdvisor

advisor = InvestmentAdvisor(config)
advice = advisor.analyze(df, fund_code='513100')

# 访问各项数据
print(advice['statistics'])    # 统计数据
print(advice['technical'])     # 技术指标
print(advice['trend'])         # 趋势分析
print(advice['risk'])          # 风险评估
print(advice['signal'])        # 交易信号
print(advice['position'])      # 仓位建议
print(advice['action'])        # 操作建议
```

### 2. 批量分析多个基金

```python
from investment_advisor import InvestmentAdvisor

fund_codes = ['513100', '513050', '159941']
advisor = InvestmentAdvisor()

for code in fund_codes:
    # 获取数据
    df = get_fund_data(code)  # 你的数据获取函数
    
    # 分析
    advice = advisor.analyze(df, code)
    
    # 比较信号
    print(f"{code}: {advice['signal']['signal']} "
          f"(仓位{advice['position']['recommended']}%)")
```

### 3. 策略回测

```python
from investment_advisor import InvestmentAdvisor
import pandas as pd

# 获取历史数据
historical_df = get_historical_data('513100', days=100)

# 模拟每天的决策
advisor = InvestmentAdvisor()
signals = []

for i in range(30, len(historical_df), 5):  # 每5天分析一次
    window_df = historical_df.iloc[i-30:i]
    advice = advisor.analyze(window_df)
    signals.append({
        'date': window_df.iloc[0]['日期'],
        'signal': advice['signal']['signal'],
        'position': advice['position']['recommended']
    })

# 分析信号效果
signals_df = pd.DataFrame(signals)
print(signals_df)
```

---

## 🎨 输出示例

```
======================================================================
💡 投资决策建议 - 2025-11-09 15:30:45
基金代码: 513100
======================================================================

📊 市场状态:
  最新价格: 115.5982
  最新涨跌: -2.63%
  近期总收益: +15.26%
  日均收益: +0.51%
  胜率: 50.0% (15/30天上涨)

📈 技术指标:
  RSI(14): 52.3
  5日动量: +1.85%
  相对MA5: +0.42%
  相对MA10: +1.23%

📉 趋势分析:
  方向: 上涨 (强度: 中)
  动量: 60.0%
  近5天: 3涨 2跌

⚠️  风险评估:
  风险等级: 中等风险
  波动率: 2.26%
  RSI状态: 正常
  说明: 波动率2.26%，市场波动适中

🎯 交易信号:
  信号: 买入
  综合评分: 2.5
  信号置信度: 62.5%

💰 仓位建议:
  建议仓位 65%
  (范围: 10%-80%)

🎬 操作建议:
  📈 建议适量买入，建议仓位65%
  ⚠️  市场波动较大，注意控制风险

📝 理由分析:
  • 近期表现良好，总收益15.26%
  • 市场趋势上涨，可以关注

======================================================================
⚠️  免责声明: 以上建议仅供参考，不构成投资建议，投资有风险，入市需谨慎！
======================================================================
```

---

## 🔍 技术指标说明

### RSI（相对强弱指标）
- **范围**: 0-100
- **超买**: RSI > 70，可能回调
- **超卖**: RSI < 30，可能反弹
- **正常**: 30-70

### 动量 (Momentum)
- 近N日涨跌幅累计
- 正值表示上涨动量
- 负值表示下跌动量

### 移动平均线 (MA)
- MA5: 5日平均价格
- MA10: 10日平均价格
- MA20: 20日平均价格
- 当前价格 > MA，表示强势

---

## ⚙️ 参数调优建议

根据实际使用效果，可以调整以下参数：

### 1. 收益率阈值
```python
# 如果信号太保守（买入机会少）
'buy_return': 1.0,  # 降低买入阈值

# 如果信号太激进（频繁交易）
'buy_return': 3.0,  # 提高买入阈值
```

### 2. 波动率容忍度
```python
# 如果对波动过于敏感
'high_volatility': 4.0,  # 提高阈值

# 如果想更早识别风险
'high_volatility': 2.0,  # 降低阈值
```

### 3. 趋势判断窗口
```python
# 短期操作
'trend_days': 3,

# 中期操作
'trend_days': 5,

# 长期操作
'trend_days': 10,
```

---

## 🎓 最佳实践

### 1. 选择合适的策略
- 新手投资者：建议使用 `conservative`（保守策略）
- 有经验投资者：建议使用 `balanced`（稳健策略）
- 专业交易者：可以使用 `aggressive` 或自定义策略

### 2. 结合人工判断
- 建议作为辅助决策工具，不要盲目跟随
- 考虑宏观经济、行业趋势等因素
- 关注基金的基本面变化

### 3. 定期回顾调整
- 每月回顾策略效果
- 根据市场变化调整参数
- 记录每次操作和结果

### 4. 风险控制
- 严格遵守仓位建议
- 设置止损止盈点
- 分散投资，不要孤注一掷

---

## 📝 常见问题

**Q: 为什么同样的数据，不同策略给出不同建议？**  
A: 不同策略有不同的参数阈值，对同样的市场状况会有不同的解读。这正是策略的价值所在。

**Q: 信号置信度是什么意思？**  
A: 表示该信号的可靠程度，0-100%。置信度越高，说明各项指标越一致。

**Q: 如何选择合适的策略？**  
A: 根据你的风险承受能力、投资期限和交易频率来选择。建议先用稳健策略观察一段时间。

**Q: 可以用于其他类型的基金或股票吗？**  
A: 可以！只要数据格式符合要求（包含日期、收盘、涨跌幅等字段），就可以使用。

---

## 📧 后续优化方向

- [ ] 添加更多技术指标（MACD、布林带等）
- [ ] 支持机器学习模型
- [ ] 回测功能完善
- [ ] 实时监控和告警
- [ ] 多基金组合优化
- [ ] Web界面支持

---

## ⚠️ 免责声明

本模块提供的投资建议仅供参考，不构成任何投资建议。投资有风险，入市需谨慎。请根据自身情况谨慎决策，自行承担投资风险。

---

**作者**: JavaEdge  
**创建日期**: 2025-11-09  
**最后更新**: 2025-11-09

