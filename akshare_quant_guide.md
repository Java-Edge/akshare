# AKShare 量化程序开发指南

## 项目概述
AKShare 是基于 Python 的开源财经数据接口库，提供股票、期货、期权、基金、债券、外汇、加密货币等金融产品的量价数据、基本面数据和另类数据。

## 核心功能模块

### 1. 股票数据
- **A股市场**: 实时行情、历史数据、分笔数据
- **港股市场**: 实时行情、历史数据
- **美股市场**: 实时行情、历史数据
- **科创板**: 实时行情、历史数据
- **指数数据**: 全球主要指数

### 2. 期货数据
- **国内期货**: 实时行情、历史数据、基差数据
- **外盘期货**: 实时行情
- **商品期权**: 各交易所期权数据
- **金融期权**: 上证50ETF期权等

### 3. 基金数据
- **公募基金**: 净值、持仓、评级
- **私募基金**: 管理人信息、产品数据
- **ETF/LOF**: 实时行情、历史数据

### 4. 债券数据
- **国债**: 收益率曲线
- **企业债**: 行情数据
- **可转债**: 实时行情、转股信息

### 5. 宏观经济数据
- **中国宏观**: GDP、CPI、PMI、货币供应量
- **美国宏观**: 非农、CPI、利率决议
- **欧洲宏观**: GDP、CPI、利率决议
- **全球宏观**: 主要经济体数据

### 6. 另类数据
- **空气质量**: 全国各城市AQI数据
- **疫情数据**: 新冠疫情实时数据
- **舆情数据**: 微博、百度搜索指数
- **企业数据**: 世界500强、独角兽企业

## 快速开始

### 安装
```bash
pip install akshare --upgrade
```

### 基本使用示例
```python
import akshare as ak

# 获取A股历史数据
stock_df = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date="20230101", end_date="20231231")

# 获取实时行情
stock_spot = ak.stock_zh_a_spot()

# 获取宏观经济数据
cpi_df = ak.macro_china_cpi_yearly()

# 获取期货数据
futures_df = ak.futures_zh_spot(symbol="RB0")
```

## 量化策略开发模板

### 1. 数据获取模块
```python
def get_stock_data(symbol, start_date, end_date):
    """获取股票历史数据"""
    return ak.stock_zh_a_hist(symbol=symbol, period="daily", 
                             start_date=start_date, end_date=end_date)

def get_index_data(symbol, start_date, end_date):
    """获取指数数据"""
    return ak.stock_zh_index_daily(symbol=symbol)
```

### 2. 数据处理模块
```python
def calculate_technical_indicators(df):
    """计算技术指标"""
    df['MA5'] = df['收盘'].rolling(window=5).mean()
    df['MA20'] = df['收盘'].rolling(window=20).mean()
    df['RSI'] = calculate_rsi(df['收盘'])
    return df

def calculate_rsi(prices, period=14):
    """计算RSI指标"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))
```

### 3. 策略信号模块
```python
def generate_signals(df):
    """生成交易信号"""
    df['signal'] = 0
    df.loc[df['MA5'] > df['MA20'], 'signal'] = 1  # 金叉买入
    df.loc[df['MA5'] < df['MA20'], 'signal'] = -1  # 死叉卖出
    return df
```

### 4. 回测引擎模块
```python
def backtest_strategy(signals, initial_capital=100000):
    """简单回测引擎"""
    capital = initial_capital
    position = 0
    trades = []
    
    for i, row in signals.iterrows():
        if row['signal'] == 1 and position == 0:  # 买入
            position = capital / row['收盘']
            capital = 0
            trades.append(('buy', row.name, row['收盘']))
        elif row['signal'] == -1 and position > 0:  # 卖出
            capital = position * row['收盘']
            position = 0
            trades.append(('sell', row.name, row['收盘']))
    
    # 计算最终收益
    final_value = capital + position * signals.iloc[-1]['收盘']
    return_rate = (final_value - initial_capital) / initial_capital
    return final_value, return_rate, trades
```

## 高级功能

### 1. 多因子模型
```python
# 获取估值因子
pe_ratio = ak.stock_a_pe(symbol="000001")
pb_ratio = ak.stock_a_pb(symbol="000001")

# 获取质量因子
roa = ak.stock_financial_analysis_indicator(symbol="000001")['ROA']
roe = ak.stock_financial_analysis_indicator(symbol="000001")['ROE']
```

### 2. 风险模型
```python
# 获取波动率数据
volatility = ak.stock_zh_a_hist(symbol="000001", period="daily").std()

# 获取Beta系数
market_return = ak.stock_zh_index_daily(symbol="sh000001")['收盘'].pct_change()
stock_return = ak.stock_zh_a_hist(symbol="000001", period="daily")['收盘'].pct_change()
beta = stock_return.cov(market_return) / market_return.var()
```

### 3. 投资组合优化
```python
def optimize_portfolio(symbols, start_date, end_date):
    """投资组合优化"""
    returns = {}
    for symbol in symbols:
        df = ak.stock_zh_a_hist(symbol=symbol, start_date=start_date, end_date=end_date)
        returns[symbol] = df['收盘'].pct_change()
    
    returns_df = pd.DataFrame(returns)
    cov_matrix = returns_df.cov()
    
    # 使用Markowitz模型优化
    ef = EfficientFrontier(None, cov_matrix)
    weights = ef.max_sharpe()
    return weights
```

## 最佳实践

### 1. 数据缓存
```python
from functools import lru_cache
import pandas as pd

@lru_cache(maxsize=100)
def cached_stock_data(symbol, start_date, end_date):
    """带缓存的数据获取"""
    return ak.stock_zh_a_hist(symbol=symbol, start_date=start_date, end_date=end_date)
```

### 2. 错误处理
```python
def safe_data_fetch(func, *args, **kwargs):
    """安全的数据获取函数"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        print(f"数据获取失败: {e}")
        return None
```

### 3. 性能优化
```python
import concurrent.futures

def fetch_multiple_stocks(symbols, start_date, end_date):
    """并行获取多个股票数据"""
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(
            lambda sym: ak.stock_zh_a_hist(symbol=sym, start_date=start_date, end_date=end_date),
            symbols
        ))
    return dict(zip(symbols, results))
```

## 常用API速查

### 股票相关
- `stock_zh_a_hist()` - A股历史数据
- `stock_zh_a_spot()` - A股实时行情
- `stock_zh_index_daily()` - 指数历史数据
- `stock_zh_a_tick_tx()` - 分笔数据

### 期货相关
- `futures_zh_spot()` - 期货实时行情
- `futures_zh_hist()` - 期货历史数据
- `futures_roll_yield()` - 展期收益

### 基金相关
- `fund_em()` - 公募基金数据
- `fund_etf_em()` - ETF基金数据
- `fund_lof_em()` - LOF基金数据

### 宏观相关
- `macro_china_cpi_yearly()` - 中国CPI
- `macro_usa_non_farm()` - 美国非农
- `macro_euro_cpi_mom()` - 欧洲CPI

## 注意事项

1. **数据频率**: 注意不同接口的数据更新频率
2. **请求限制**: 避免过于频繁的请求
3. **数据质量**: 验证数据的准确性和完整性
4. **错误处理**: 做好网络异常和数据缺失的处理

## 扩展资源

- [官方文档](https://akshare.akfamily.xyz/)
- [GitHub仓库](https://github.com/akfamily/akshare)
- [示例代码](https://github.com/akfamily/akshare/tree/main/examples)

通过AKShare，您可以快速构建专业的量化交易系统，专注于策略开发而非数据获取。