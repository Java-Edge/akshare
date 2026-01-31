# 📚 AKShare A股API实战学习 - 湖南黄金（002716）

## 🎯 学习目标

通过实际操作湖南黄金（002716）这只股票，快速掌握 AKShare 的核心 API，为量化投资打下基础。

## 📁 创建的学习文件

### 1. quick_test_stock_api.py （⭐ 推荐新手）
**快速测试版本** - 5分钟了解核心API

```bash
python quick_test_stock_api.py
```

**包含的API：**
- `stock_zh_a_spot_em()` - 获取实时行情
- `stock_zh_a_hist()` - 获取历史K线数据
- `stock_individual_info_em()` - 获取个股详细信息
- `stock_board_industry_name_em()` - 获取行业板块数据

**输出内容：**
- 实时价格、涨跌幅、成交额
- 最近5天K线数据
- 技术指标（MA5、MA10）
- 股票基本信息
- 黄金板块数据

---

### 2. stock_demo_hunan_silver.py
**完整演示版本** - 自动运行所有功能

```bash
python stock_demo_hunan_silver.py
```

**演示内容：**
1. ✅ 股票基本信息查询
2. ✅ 实时行情数据
3. ✅ 历史K线数据（90天）
4. ✅ 技术指标计算（MA、RSI、MACD、布林带）
5. ✅ 财务数据分析
6. ✅ 资金流向监控
7. ✅ 行业板块分析
8. ✅ API使用总结

**特点：**
- 自动运行，无需手动干预
- 完整展示所有核心API
- 包含技术分析和解读
- 生成学习总结报告

---

### 3. stock_tutorial_hunan_silver.py
**互动教程版本** - 一步步学习（需要手动按回车）

```bash
python stock_tutorial_hunan_silver.py
```

**教程章节：**
- 第1课：获取股票基本信息
- 第2课：获取实时行情数据
- 第3课：获取历史行情数据
- 第4课：技术指标计算与分析
- 第5课：获取财务数据
- 第6课：获取资金流向数据
- 第7课：数据可视化（生成K线图）
- 第8课：行业与板块分析
- 第9课：生成综合分析报告

**特点：**
- 逐课学习，深入理解
- 详细的API说明
- 生成可视化图表
- 完整的分析报告

---

## 🚀 快速开始

### 方式1：快速测试（推荐）

```bash
cd /Users/javaedge/soft/PyCharmProjects/akshare/my-trade
python quick_test_stock_api.py
```

**适合场景：**
- 快速验证AKShare是否正常工作
- 了解核心API的使用方法
- 获取湖南黄金的最新数据

---

### 方式2：完整演示

```bash
python stock_demo_hunan_silver.py
```

**适合场景：**
- 系统学习所有核心API
- 了解完整的股票分析流程
- 查看详细的数据展示

---

### 方式3：互动教程

```bash
python stock_tutorial_hunan_silver.py
```

**适合场景：**
- 逐步学习，深入理解
- 需要生成图表和报告
- 希望详细了解每个API

---

## 📊 核心API速查

### 1. 实时行情

```python
import akshare as ak

# 获取所有A股实时行情
spot_df = ak.stock_zh_a_spot_em()

# 筛选湖南黄金
hunan = spot_df[spot_df['代码'] == '002716']
print(hunan[['名称', '最新价', '涨跌幅', '成交额']])
```

**返回字段：**
- 代码、名称、最新价、涨跌幅、涨跌额
- 成交量、成交额、振幅、换手率
- 市盈率、市净率等

---

### 2. 历史K线

```python
# 获取历史日线数据
hist_df = ak.stock_zh_a_hist(
    symbol="002716",          # 股票代码
    period="daily",           # 周期: daily/weekly/monthly
    start_date="20250101",    # 开始日期
    end_date="20260125",      # 结束日期
    adjust=""                 # 复权: 空/qfq/hfq
)

print(hist_df[['日期', '开盘', '收盘', '最高', '最低', '涨跌幅']])
```

**可选周期：**
- `daily` - 日线
- `weekly` - 周线
- `monthly` - 月线

**复权类型：**
- `""` - 不复权
- `"qfq"` - 前复权
- `"hfq"` - 后复权

---

### 3. 个股信息

```python
# 获取个股详细信息
info_df = ak.stock_individual_info_em(symbol="002716")
print(info_df)
```

**返回信息：**
- 总市值、流通市值
- 行业、上市时间
- PE、PB等估值指标
- 股东人数等

---

### 4. 财务数据

```python
# 获取财务分析指标
financial_df = ak.stock_financial_analysis_indicator(symbol="002716")
print(financial_df[['日期', 'ROE', 'ROA', '净利润同比增长率']])
```

**主要指标：**
- ROE - 净资产收益率
- ROA - 总资产收益率
- 净利润增长率
- 营收增长率
- 资产负债率等

---

### 5. 资金流向

```python
# 获取个股资金流向
fund_flow = ak.stock_individual_fund_flow(
    stock="002716",
    market="深证"  # 深证/沪市
)
print(fund_flow[['日期', '主力净流入-净额', '主力净流入-净占比']])
```

**资金分类：**
- 主力资金（超大单+大单）
- 超大单（>50万元）
- 大单（10-50万元）
- 中单（2-10万元）
- 小单（<2万元）

---

### 6. 行业板块

```python
# 获取所有行业板块
industry_df = ak.stock_board_industry_name_em()

# 筛选黄金相关
gold_industry = industry_df[industry_df['板块名称'].str.contains('黄金')]
print(gold_industry[['板块名称', '涨跌幅', '总市值']])
```

---

## 💡 技术指标计算示例

### 移动平均线（MA）

```python
# 计算5日、10日、20日均线
df['MA5'] = df['收盘'].rolling(window=5).mean()
df['MA10'] = df['收盘'].rolling(window=10).mean()
df['MA20'] = df['收盘'].rolling(window=20).mean()
```

### RSI相对强弱指标

```python
def calculate_rsi(prices, period=14):
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

df['RSI'] = calculate_rsi(df['收盘'])
```

### MACD

```python
# 计算MACD
exp1 = df['收盘'].ewm(span=12, adjust=False).mean()
exp2 = df['收盘'].ewm(span=26, adjust=False).mean()
df['MACD'] = exp1 - exp2
df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
df['Histogram'] = df['MACD'] - df['Signal']
```

### 布林带（BOLL）

```python
# 计算布林带
df['BB_middle'] = df['收盘'].rolling(window=20).mean()
bb_std = df['收盘'].rolling(window=20).std()
df['BB_upper'] = df['BB_middle'] + 2 * bb_std
df['BB_lower'] = df['BB_middle'] - 2 * bb_std
```

---

## 🎯 实战应用场景

### 场景1：每日监控

```python
# 获取最新行情
spot = ak.stock_zh_a_spot_em()
hunan = spot[spot['代码'] == '002716'].iloc[0]

# 判断买卖点
if hunan['RSI'] < 30:
    print("RSI超卖，可以考虑买入")
elif hunan['RSI'] > 70:
    print("RSI超买，可以考虑卖出")
```

### 场景2：资金监控

```python
# 获取资金流向
fund_flow = ak.stock_individual_fund_flow(stock="002716", market="深证")
latest = fund_flow.iloc[0]

if latest['主力净流入-净额'] > 0:
    print(f"主力净流入 {latest['主力净流入-净额']/10000:.2f} 万元，市场看好")
else:
    print("主力净流出，需谨慎")
```

### 场景3：行业轮动

```python
# 获取行业板块涨幅
industry = ak.stock_board_industry_name_em()
top5 = industry.sort_values('涨跌幅', ascending=False).head(5)
print("今日涨幅前5的行业：")
print(top5[['板块名称', '涨跌幅']])
```

---

## 📈 数据可视化

### K线图 + 均线

```python
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))
plt.plot(df['日期'], df['收盘'], label='收盘价', linewidth=2)
plt.plot(df['日期'], df['MA5'], label='MA5')
plt.plot(df['日期'], df['MA10'], label='MA10')
plt.plot(df['日期'], df['MA20'], label='MA20')
plt.legend()
plt.title('湖南黄金 K线图')
plt.show()
```

### RSI指标图

```python
plt.figure(figsize=(12, 4))
plt.plot(df['日期'], df['RSI'], label='RSI', color='purple')
plt.axhline(y=70, color='r', linestyle='--', label='超买线')
plt.axhline(y=30, color='g', linestyle='--', label='超卖线')
plt.legend()
plt.title('RSI 指标')
plt.show()
```

---

## 🔄 修改分析其他股票

只需修改股票代码即可分析其他股票：

```python
# 在文件开头修改
STOCK_CODE = "000001"  # 改为平安银行
STOCK_NAME = "平安银行"

# 或者
STOCK_CODE = "600519"  # 改为贵州茅台
STOCK_NAME = "贵州茅台"
```

**常见股票代码：**
- 000001 - 平安银行
- 000002 - 万科A
- 600000 - 浦发银行
- 600519 - 贵州茅台
- 601318 - 中国平安
- 002716 - 湖南黄金

---

## 📚 扩展学习

### 推荐文档

1. **akshare_quant_guide.md** - AKShare完整量化开发指南
2. **USAGE_GUIDE.md** - AI投资顾问使用指南
3. **docs/principle.md** - 个人投资原则（AI分析依据）

### 推荐项目文件

1. **qdii-stock-plan.py** - QDII基金分析主程序
2. **investment_advisor.py** - AI投资建议模块
3. **llm_client.py** - 本地大模型客户端

### AKShare官方资源

- [官方文档](https://akshare.akfamily.xyz/)
- [GitHub仓库](https://github.com/akfamily/akshare)
- [示例代码](https://github.com/akfamily/akshare/tree/main/examples)

---

## 💪 进阶挑战

1. **多股票对比分析**
   - 同时分析多只黄金股票
   - 对比涨跌幅、资金流向
   - 筛选出最优股票

2. **量化策略开发**
   - 开发MA金叉死叉策略
   - 开发RSI超买超卖策略
   - 回测策略收益率

3. **AI投资顾问集成**
   - 结合 investment_advisor.py
   - 生成AI投资建议
   - 基于个人投资原则决策

4. **数据持久化**
   - 将数据保存到MySQL
   - 建立历史数据库
   - 长期跟踪分析

---

## ⚠️ 注意事项

1. **数据更新频率**
   - 实时行情有延迟（通常几秒到几分钟）
   - 财务数据季度更新
   - 避免过于频繁调用API

2. **网络问题**
   - 部分API需要良好的网络连接
   - 如遇网络问题，程序会显示错误信息
   - 可以稍后重试

3. **数据准确性**
   - 建议交叉验证数据
   - 重要决策前核对官方数据
   - 数据仅供参考，不构成投资建议

---

## 🎉 学习成果

完成本教程后，您将掌握：

✅ AKShare核心API的使用方法  
✅ A股股票数据的获取和处理  
✅ 技术指标的计算和应用  
✅ 数据可视化的基本技巧  
✅ 量化投资的基础知识  

---

## 📞 获取帮助

如遇问题：
1. 查看代码注释
2. 阅读 akshare_quant_guide.md
3. 访问 AKShare 官方文档
4. 检查网络连接和依赖包

---

**祝您学习顺利，投资成功！📈**

*最后更新：2026-01-25*
