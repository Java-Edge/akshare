# 投资建议模块 - 快速入门

## 🚀 5分钟上手

### 第一步：查看预设策略

```bash
python -c "from investment_config import list_strategies; list_strategies()"
```

### 第二步：运行主程序（使用默认策略）

```bash
python qdii-stock-plan.py
```

程序会自动：
1. 从数据库查询基金数据
2. 如有缺失，从API获取
3. 进行技术分析
4. 生成投资建议（包括买卖信号、仓位建议等）
5. 绘制图表

### 第三步：尝试不同策略

修改 `qdii-stock-plan.py` 的 `analyze_fund_performance` 函数：

```python
# 使用激进策略
from investment_config import get_strategy_config
config = get_strategy_config('aggressive')
quick_advice(df, fund_code, config=config)
```

或直接在函数中修改：

```python
def analyze_fund_performance(df: pd.DataFrame, fund_code: str, days: int):
    # ...前面的代码...
    
    # 选择策略：'conservative', 'balanced', 'aggressive', 'daytrader', 'longterm'
    from investment_config import get_strategy_config
    strategy_config = get_strategy_config('aggressive')  # 改这里
    quick_advice(df, fund_code, config=strategy_config)
```

---

## 📊 每日决策流程

### 方式1：使用主程序（推荐）

```bash
# 每天运行一次
python qdii-stock-plan.py
```

查看输出的：
- 🎯 交易信号（强烈买入/买入/持有/卖出/强烈卖出）
- 💰 仓位建议（0-100%）
- 🎬 具体操作建议

### 方式2：使用示例程序

```bash
# 比较不同策略
python investment_examples.py
# 选择选项 3 - 比较不同策略
```

### 方式3：Python脚本

创建 `daily_decision.py`：

```python
#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""每日投资决策脚本"""

from qdii_stock_plan import get_qdii_fund_data
from investment_advisor import quick_advice
from investment_config import get_strategy_config

# 配置
FUND_CODE = "513100"  # 你的基金代码
STRATEGY = "balanced"  # 你的策略
DAYS = 30

# 获取数据
df, new_data = get_qdii_fund_data(FUND_CODE, DAYS)

# 选择策略
config = get_strategy_config(STRATEGY)

# 生成建议
advice = quick_advice(df, FUND_CODE, config)

# 根据建议做决策
signal = advice['signal']['signal']
position = advice['position']['recommended']

print(f"\n📢 今日决策建议：")
print(f"   信号：{signal}")
print(f"   建议仓位：{position}%")

if signal in ["强烈买入", "买入"]:
    print(f"   ✅ 操作：考虑买入，目标仓位{position}%")
elif signal in ["强烈卖出", "卖出"]:
    print(f"   ⚠️  操作：考虑卖出，降低仓位至{position}%")
else:
    print(f"   📊 操作：持有观望，保持仓位{position}%")
```

运行：
```bash
python daily_decision.py
```

---

## 🎯 实战建议

### 保守投资者

```python
# 使用保守策略 + 降低仓位
from investment_config import create_custom_strategy

my_strategy = create_custom_strategy(
    name="我的保守策略",
    strong_buy=8.0,   # 需要很高收益才买入
    buy=5.0,
    sell=-2.0,        # 小幅亏损就卖出
    strong_sell=-3.0,
    max_pos=50,       # 最多50%仓位
    min_pos=0
)
```

### 积极投资者

```python
# 使用激进策略
config = get_strategy_config('aggressive')
```

### 短线交易者

```python
# 使用短线策略 + 调整参数
config = get_strategy_config('daytrader')
config['trend_days'] = 3  # 只看3天趋势
```

### 长线投资者

```python
# 使用长线策略
config = get_strategy_config('longterm')
config['trend_days'] = 20  # 看20天趋势
```

---

## 📝 决策记录模板

建议每次根据建议做决策后，记录下来：

```
日期：2025-11-09
基金代码：513100
当前价格：115.60
当前仓位：60%

=== 分析结果 ===
信号：买入
置信度：62.5%
建议仓位：65%
总收益：+15.26%
波动率：2.26%
RSI：52.3

=== 我的决策 ===
操作：买入5%，从60%增加到65%
理由：信号为买入，总收益表现良好，风险适中
买入价格：115.60
买入金额：XXXX元

=== 备注 ===
市场趋势向好，但RSI接近超买，密切关注
```

---

## ⚡ 常用命令

```bash
# 查看所有策略
python -c "from investment_config import list_strategies; list_strategies()"

# 运行主程序
python qdii-stock-plan.py

# 运行示例
python investment_examples.py

# 测试投资建议模块
python investment_advisor.py

# 查看配置
python investment_config.py
```

---

## 🔔 每日提醒

1. ✅ 每天运行一次分析
2. ✅ 查看交易信号变化
3. ✅ 关注仓位建议
4. ✅ 结合市场情况决策
5. ✅ 记录每次操作
6. ✅ 定期回顾效果

---

## 💡 小贴士

1. **不要盲目跟随**：建议仅供参考，要结合自己判断
2. **控制仓位**：严格按照建议仓位操作
3. **分批操作**：不要一次性全仓
4. **设置止损**：提前设定止损点
5. **定期回顾**：每月回顾策略效果
6. **调整参数**：根据实际情况优化配置

---

## 🆘 遇到问题？

1. **信号总是"持有"**：可能阈值设置太严格，尝试调低买入阈值
2. **信号变化太频繁**：可能太激进，尝试增加趋势判断天数
3. **置信度总是很低**：正常现象，市场不确定性高时置信度会降低
4. **仓位建议太保守**：可以提高 max_position 参数

---

## 📚 延伸阅读

- `INVESTMENT_ADVISOR_README.md` - 完整使用文档
- `investment_advisor.py` - 核心代码
- `investment_config.py` - 策略配置
- `investment_examples.py` - 使用示例

---

**记住**：投资有风险，建议仅供参考，请谨慎决策！ ⚠️

