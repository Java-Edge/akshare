# 🤖 AI投资顾问系统 - 使用指南

## 📋 系统概述

本系统是一个基于本地大模型的QDII基金智能投资决策辅助工具，完全遵循您在 `principle.md` 中定义的个人投资原则。

### ✨ 核心功能

1. **智能数据管理**：只更新数据库中缺失的交易日数据，避免重复保存
2. **双层分析架构**：基础技术分析 + AI深度分析
3. **个性化建议**：基于您的投资原则生成买卖决策
4. **完全本地化**：数据隐私可控，无需云端API

---

## 🚀 快速开始

### 1️⃣ 测试LLM连接

```bash
cd /Users/javaedge/soft/PyCharmProjects/akshare/my-trade
python test_llm_connection.py
```

**预期输出：**
```
✅ 连接成功！
✅ 本地模型配置正确，可以使用投资顾问了！
```

### 2️⃣ 运行主程序（启用AI分析）

```bash
python qdii-stock-plan.py
```

**程序流程：**
1. 📊 从数据库查询历史数据
2. 🔍 检测缺失的交易日
3. 📡 从API获取缺失数据（如有）
4. 💾 只保存新获取的数据到数据库
5. 📈 执行技术分析
6. 🤖 调用本地LLM进行深度分析
7. 📝 输出完整投资建议
8. 🎨 生成可视化图表

### 3️⃣ 运行数据流测试

```bash
python test_qdii_flow.py
```

这会删除最近3条数据，然后您可以再次运行主程序验证增量更新逻辑。

---

## 📊 输出示例

### 基础技术分析

```
📊 市场状态:
  最新价格: 1.8910
  最新涨跌: -0.53%
  近期总收益: -2.62%
  胜率: 30.0% (9/30天上涨)

📈 技术指标:
  RSI(14): 37.2
  5日动量: -0.66%
  相对MA5: +0.27%

📉 趋势分析:
  方向: 下跌 (强度: 弱)
  动量: 20.0%

🎯 交易信号:
  信号: 持有
  综合评分: -1.0
  置信度: 25.0%

💰 仓位建议:
  建议仓位 36%
```

### 🤖 AI深度分析（基于您的投资原则）

```
## 投资建议：513100 (2026-01-25)

【操作建议】持有

【建议仓位】5%-10% (作为日经指数配置的补充)

【决策理由】
1. 符合核心配置方向：513100跟踪日经225指数，符合"核心配置方向：
   日经指数和美股指数"的原则
2. 低风险特性：波动率较低（0.91%），符合稳健投资基调
3. 技术指标显示潜在反弹机会：RSI(37.2)处于正常范围

【风险提示】
- 下跌趋势：当前基金处于下跌趋势，短期可能持续
- 胜率低：30%的胜率表明该基金近期表现不稳定
- 日经指数整体波动：受国际经济形势影响较大

【操作计划】
1. 持有现有仓位：鉴于基金整体风险较低，建议持有
2. 不新增建仓：考虑到下跌趋势，短期内不建议新增
3. 关注反弹信号：若突破MA10，可考虑分批加仓
4. 设置止盈点：1.95元以上及时卖出
5. 分批减仓：若跌破MA20则止损
```

---

## ⚙️ 配置与自定义

### 修改基金代码

编辑 `qdii-stock-plan.py` 第371行：

```python
fund_code = "513100"  # 改为您要分析的基金代码
days = 30             # 分析最近N个交易日
```

**常用QDII基金代码：**
- 513100: 纳斯达克100ETF
- 513500: 标普500ETF
- 159920: 恒生ETF
- 513050: 中概互联ETF

### 调整分析策略

编辑 `investment_advisor.py` 的配置参数：

```python
def _default_config(self) -> Dict:
    return {
        'strong_buy_return': 5.0,   # 强烈买入阈值（%）
        'buy_return': 2.0,          # 买入阈值（%）
        'sell_return': -3.0,        # 卖出阈值（%）
        'high_volatility': 3.0,     # 高波动率阈值（%）
        'trend_days': 5,            # 趋势判断天数
        'max_position': 100,        # 最大仓位（%）
        'min_position': 10,         # 最小仓位（%）
    }
```

### 修改投资原则

编辑 `docs/principle.md` 文件，AI会严格遵循您定义的原则：

```markdown
# 个人理财投资体系与心得总结

## 一、 投资工具选择：场内 V.S 场外
必须购买场内基金...

## 二、 卖出与止盈策略
七天止盈策略...

## 三、 板块与资产配置
主要战场：日经指数和美股指数...
```

### 禁用AI分析（仅使用技术分析）

修改 `investment_advisor.py` 第48行：

```python
advisor = InvestmentAdvisor(use_llm=False)
```

或在初始化时指定：

```python
from investment_advisor import InvestmentAdvisor

advisor = InvestmentAdvisor(use_llm=False)
advice = advisor.analyze(df, fund_code)
advisor.print_advice(advice)
```

---

## 🔧 系统架构

### 文件说明

```
my-trade/
├── qdii-stock-plan.py          # 主程序（数据获取、分析、可视化）
├── investment_advisor.py       # 投资建议模块（技术分析 + LLM）
├── llm_client.py              # 本地大模型客户端
├── database_config.py          # 数据库配置
├── test_llm_connection.py     # LLM连接测试
├── test_qdii_flow.py          # 数据流测试
├── test_data_save.py          # 数据保存逻辑测试
├── README_AI_ADVISOR.md       # 系统说明文档
└── docs/
    ├── principle.md           # ⭐ 投资原则（AI分析依据）
    └── QUICK_START.md         # 快速入门
```

### 数据流程

```
┌─────────────────┐
│   主程序启动    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 查询数据库数据  │ ◄─── MySQL数据库
└────────┬────────┘
         │
         ▼
    ┌─────────┐
    │有缺失？ │
    └────┬────┘
         │
    是   │   否
    ▼    │    ▼
┌───────┐│ ┌──────────┐
│调用API││ │使用现有  │
└───┬───┘│ │数据分析  │
    │    │ └────┬─────┘
    ▼    │      │
┌───────┐│      │
│保存新 ││      │
│数据   ││      │
└───┬───┘│      │
    │    │      │
    └────┴──────┘
         │
         ▼
┌─────────────────┐
│  技术指标计算   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ LLM深度分析     │ ◄─── 本地LM Studio
│ (基于principle) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  输出投资建议   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  生成可视化图表 │
└─────────────────┘
```

---

## 💡 关键优化点

### 1. 智能数据更新

**优化前：**
```python
# 每次都保存全部30条数据
save_to_database(df, fund_code)
```

**优化后：**
```python
df, new_data = get_qdii_fund_data(fund_code, days)
if not new_data.empty:
    print(f"💾 正在保存 {len(new_data)} 条新数据...")
    save_to_database(new_data, fund_code)
else:
    print("✅ 无需保存，数据库已是最新")
```

**效果：**
- ✅ 减少不必要的数据库写操作
- ✅ 只更新缺失的交易日数据
- ✅ 提高程序运行效率

### 2. 模块化架构

**investment_advisor.py** 独立模块：
- 可在其他项目中复用
- 支持自定义策略配置
- 可选启用/禁用LLM
- 便于后续针对性优化

### 3. 基于个人原则的AI分析

AI严格遵循 `principle.md` 中的规则：
- ✅ 场内外基金选择建议
- ✅ 止盈止损策略提醒
- ✅ 板块配置建议
- ✅ 风险控制提示
- ✅ 具体操作计划

---

## 🐛 故障排查

### LLM连接失败

**症状：**
```
⚠️  无法连接到本地模型服务
```

**解决方法：**
1. 检查LM Studio是否运行
2. 确认服务地址：`http://10.56.88.6:1234`
3. 验证模型加载：`google/gemma-3-27b`
4. 测试连接：`python test_llm_connection.py`

### 数据库连接问题

**症状：**
```
❌ 数据库错误: ...
```

**解决方法：**
1. 检查 `database_config.py` 配置
2. 确认MySQL服务运行
3. 验证数据库权限
4. 测试连接：`python test_qdii_flow.py`

### 投资原则未加载

**症状：**
```
⚠️  未找到投资原则文档
⚠️  本地大模型不可用，将使用基础分析
```

**解决方法：**
1. 确认文件存在：`docs/principle.md`
2. 检查文件编码：UTF-8
3. 验证文件路径正确

### 数据获取失败

**症状：**
```
❌ 数据获取失败: HTTPSConnectionPool...
💡 正在尝试使用模拟数据演示功能...
```

**原因：**
- 网络连接问题
- 代理配置错误
- AKShare API限制

**解决方法：**
- 检查网络连接
- 配置代理（如需要）
- 稍后重试
- 程序会自动使用模拟数据演示

---

## 📚 下一步优化建议

### 1. 支持多基金批量分析

```python
fund_codes = ["513100", "513500", "159920"]
for fund_code in fund_codes:
    df, new_data = get_qdii_fund_data(fund_code, days)
    analyze_fund_performance(df, fund_code, days)
    if not new_data.empty:
        save_to_database(new_data, fund_code)
```

### 2. 添加历史建议追踪

保存每次AI建议到数据库，分析建议准确性：

```python
CREATE TABLE investment_advice (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fund_code VARCHAR(10),
    advice_date DATE,
    signal VARCHAR(20),
    recommended_position INT,
    actual_return_7d DECIMAL(10, 4),
    advice_content TEXT
);
```

### 3. 集成通知功能

当出现强烈买入/卖出信号时，发送通知：

```python
if signal['signal'] in ['强烈买入', '强烈卖出']:
    send_notification(fund_code, signal, advice['llm_analysis'])
```

### 4. Web界面

使用Flask/FastAPI构建Web界面：
- 可视化仪表板
- 历史建议查询
- 实时数据更新
- 多基金对比

---

## ⚠️ 免责声明

**本系统仅供学习和参考使用，不构成任何投资建议。**

- 投资有风险，决策需谨慎
- AI分析基于历史数据和既定规则
- 市场情况瞬息万变，请独立判断
- 建议结合自身情况和专业意见做决策

---

## 🎉 使用技巧

### 每日操作流程

1. **上午开盘前**：运行主程序查看分析
2. **关注关键信号**：强烈买入/卖出信号
3. **执行决策**：按照AI建议和个人判断操作
4. **记录结果**：追踪建议准确性

### 定期优化

1. **每周**：回顾AI建议准确性
2. **每月**：调整 `principle.md` 中的规则
3. **每季度**：优化技术指标参数
4. **持续**：完善投资原则文档

---

## 📞 技术支持

如有问题：
1. 查看代码注释
2. 阅读文档
3. 运行测试脚本诊断
4. 检查日志输出

---

**Happy Trading! 📈**

*最后更新：2026-01-25*
