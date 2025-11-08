# 美股个股分析
from akshare.stock.stock_us_sina import stock_us_daily;

df = stock_us_daily(symbol='AAPL', adjust='');
print(df.iloc[-1])