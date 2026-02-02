# 基金投资决策系统使用指南

## 📚 系统概述

本系统为场外基金投资提供智能决策支持，集成了实时数据查询、技术分析和AI智能建议功能。

## 🎯 核心功能

### 1. 场外基金实时估值查询
- 单只基金查询
- 批量查询和筛选
- 关键词搜索
- 涨跌幅排行

### 2. 投资决策建议
- 基础技术分析
- 风险评估
- 交易信号生成
- AI深度分析（可选）

### 3. 投资原则遵循
- 不追涨杀跌
- 理性止盈止损
- 风险控制优先

## 📦 文件结构

```
my-trade/
├── fund_api.py                    # 基金API封装
├── fund_investment_advisor.py     # 投资建议模块
├── fund_query_example.py          # 查询示例
├── llm_client.py                  # 本地大模型客户端
├── README_FUND_API.md             # API使用文档
├── README_FUND_ADVISOR.md         # 本文档
└── docs/
    └── skills.md                  # 投资原则文档
```

## 🚀 快速开始

### 环境要求

```bash
# Python 3.8+
pip install akshare pandas numpy requests
```

### 基础使用

#### 1. 查询单只基金

```python
from fund_api import FundAPI

api = FundAPI()
fund_info = api.get_fund_realtime_value("000001")

if fund_info:
    api.print_fund_info(fund_info)
```

#### 2. 获取投资建议（不使用AI）

```python
from fund_api import FundAPI
from fund_investment_advisor import FundInvestmentAdvisor

# 初始化
api = FundAPI()
advisor = FundInvestmentAdvisor(use_llm=False)

# 获取基金数据
fund_info = api.get_fund_realtime_value("000001")

# 分析并生成建议
if fund_info:
    analysis = advisor.analyze_fund(fund_info)
    advisor.print_advice(analysis)
```

#### 3. 获取AI增强建议

```python
from fund_api import FundAPI
from fund_investment_advisor import FundInvestmentAdvisor

# 初始化（启用LLM）
api = FundAPI()
advisor = FundInvestmentAdvisor(use_llm=True)

# 获取基金数据
fund_info = api.get_fund_realtime_value("161116")

# 分析并生成AI建议
if fund_info:
    analysis = advisor.analyze_fund(fund_info)
    advisor.print_advice(analysis)
```

## 💡 使用场景

### 场景1: 每日基金监控

```python
"""每日定时查询自选基金并获取建议"""
from fund_api import FundAPI
from fund_investment_advisor import FundInvestmentAdvisor

# 我的自选基金
my_funds = ["000001", "161116", "110022"]

api = FundAPI()
advisor = FundInvestmentAdvisor(use_llm=True)

print("=" * 80)
print("📊 每日基金监控报告")
print("=" * 80)

for fund_code in my_funds:
    print(f"\n正在分析基金 {fund_code}...")
    
    # 获取数据
    fund_info = api.get_fund_realtime_value(fund_code)
    
    if fund_info:
        # 分析并输出建议
        analysis = advisor.analyze_fund(fund_info)
        advisor.print_advice(analysis)
    else:
        print(f"❌ 无法获取基金 {fund_code} 数据\n")
```

### 场景2: 寻找投资机会

```python
"""查找当前可能的买入机会"""
from fund_api import FundAPI
from fund_investment_advisor import FundInvestmentAdvisor

api = FundAPI()
advisor = FundInvestmentAdvisor(use_llm=False)

# 获取QDII基金数据
funds_df = api.get_funds_by_type("QDII")

if funds_df is not None:
    # 筛选跌幅较大的基金（可能是抄底机会）
    rate_col = [col for col in funds_df.columns if '估算增长率' in col][0]
    funds_df[f'{rate_col}_num'] = funds_df[rate_col].astype(str).str.rstrip('%').replace('---', None)
    funds_df[f'{rate_col}_num'] = pd.to_numeric(funds_df[f'{rate_col}_num'], errors='coerce')
    
    # 筛选跌幅在-3%到-1%之间的基金（可能的买入机会）
    opportunity_funds = funds_df[
        (funds_df[f'{rate_col}_num'] >= -3.0) & 
        (funds_df[f'{rate_col}_num'] <= -1.0)
    ]
    
    print(f"\n找到 {len(opportunity_funds)} 只可能的投资机会:")
    print(opportunity_funds[['基金代码', '基金名称', rate_col]].head(10))
```

### 场景3: 批量分析基金

```python
"""批量分析多只基金并保存结果"""
from fund_api import FundAPI
from fund_investment_advisor import FundInvestmentAdvisor
import json
from datetime import datetime

api = FundAPI()
advisor = FundInvestmentAdvisor(use_llm=True)

# 要分析的基金列表
funds_to_analyze = ["000001", "161116", "110022", "270002"]

results = []

for fund_code in funds_to_analyze:
    fund_info = api.get_fund_realtime_value(fund_code)
    
    if fund_info:
        analysis = advisor.analyze_fund(fund_info)
        results.append(analysis)

# 保存结果
output_file = f"fund_analysis_{datetime.now().strftime('%Y%m%d')}.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"✅ 分析结果已保存到 {output_file}")
```

## 📊 分析结果说明

### 交易信号类型

| 信号 | 说明 | 适用场景 |
|-----|------|---------|
| **强烈买入** | 极佳买入时机 | 大幅下跌后反弹，技术面强势 |
| **买入** | 适合建仓或加仓 | 横盘整理，轻微下跌 |
| **持有** | 观望为主 | 温和上涨，方向不明确 |
| **卖出** | 考虑减仓 | 大涨后高位，或趋势转弱 |
| **强烈卖出** | 尽快离场 | 严重下跌趋势，风险极高 |

### 风险等级

| 等级 | 说明 | 特征 |
|-----|------|------|
| **低风险** | 波动较小 | 涨跌幅 < 1% |
| **中等风险** | 正常波动 | 涨跌幅 1%-2% |
| **高风险** | 波动较大 | 涨跌幅 2%-3% |
| **极高风险** | 剧烈波动 | 涨跌幅 > 3% |

## 🎓 投资原则

系统遵循以下核心投资原则（来自 `docs/skills.md`）：

### 1. 永远不要追涨杀跌
- ❌ 错误：上涨时买入，下跌时卖出
- ✅ 正确：下跌时分批买入，上涨时分批卖出

### 2. 不要幻想买在最低点
- 接受"买不到最低，卖不到最高"的现实
- 在合理价位区间操作即可

### 3. 沉没成本不参与决策
- 不要因为"已经亏了"而死拿
- 方向错了要及时止损

### 4. 红的才卖，绿的套着
- 盈利时考虑止盈
- 亏损时除非趋势反转，否则耐心持有

### 5. 关注大宗商品特性（针对贵金属基金）
- 金银不再是避险资产，拿住即可
- 关注交割日历（如CME黄金交割日）
- 铜银受中国经济影响大

## 🔧 高级配置

### 配置本地大模型

如果要使用AI深度分析功能，需要配置本地大模型（LM Studio）：

1. 启动LM Studio并加载模型
2. 确保API服务运行在 `http://10.56.88.6:1234`
3. 修改 `llm_client.py` 中的配置：

```python
class LocalLLMClient:
    def __init__(self, 
                 api_url: str = "http://YOUR_IP:1234/v1/chat/completions",
                 model: str = "YOUR_MODEL_NAME",
                 timeout: int = 120):
        # ...
```

### 自定义投资原则

编辑 `docs/skills.md` 文件，添加你的投资原则。系统会自动加载并应用到AI分析中。

### 调整决策参数

在 `fund_investment_advisor.py` 的 `_generate_signal` 方法中，可以调整信号生成的阈值：

```python
def _generate_signal(self, analysis: Dict) -> str:
    rate = analysis.get('rate_value', 0)
    
    # 自定义阈值
    if rate > 5.0:  # 大涨阈值
        return Signal.SELL.value + " (止盈考虑)"
    # ...
```

## ⚠️ 注意事项

1. **数据时效性**
   - 实时估值数据仅在交易日更新
   - 非交易时间可能显示"---"

2. **仅供参考**
   - 所有建议仅供参考，不构成投资建议
   - 投资决策需结合自身情况

3. **风险提示**
   - 基金投资有风险，入市需谨慎
   - 过往业绩不代表未来表现

4. **技术限制**
   - 本系统仅分析实时数据，未使用历史趋势
   - AI分析需要本地模型支持

## 🐛 故障排查

### 问题1: 查询不到基金数据

**可能原因:**
- 基金代码错误
- 非场外基金
- 网络连接问题

**解决方案:**
```python
# 先搜索确认基金代码
result = api.search_funds("基金名称关键词")
print(result[['基金代码', '基金名称']])
```

### 问题2: LLM不可用

**可能原因:**
- 本地模型服务未启动
- API地址配置错误
- 网络不通

**解决方案:**
```python
# 测试LLM连接
from llm_client import test_llm_client
test_llm_client()

# 或者禁用LLM使用基础分析
advisor = FundInvestmentAdvisor(use_llm=False)
```

### 问题3: 数据显示异常

**可能原因:**
- 数据源暂时不可用
- 基金暂停估值

**解决方案:**
- 稍后重试
- 检查基金是否正常运作

## 📈 未来计划

- [ ] 增加历史数据分析
- [ ] 支持回测功能
- [ ] 添加多基金组合分析
- [ ] 实时监控和预警
- [ ] 数据可视化

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可

MIT License

---

**最后更新**: 2025-02-01
