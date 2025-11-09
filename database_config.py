# 数据库配置
MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',  # 请根据实际情况修改
    'password': '123456',  # 请根据实际情况修改
    'database': 'trade',
    'charset': 'utf8mb4'
}

# 建表SQL语句
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS qdii_fund_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fund_code VARCHAR(10) NOT NULL COMMENT '基金代码',
    trade_date DATE NOT NULL COMMENT '交易日期',
    open_price DECIMAL(10, 4) COMMENT '开盘价',
    close_price DECIMAL(10, 4) COMMENT '收盘价',
    high_price DECIMAL(10, 4) COMMENT '最高价',
    low_price DECIMAL(10, 4) COMMENT '最低价',
    change_percent DECIMAL(8, 4) COMMENT '涨跌幅(%)',
    volume BIGINT COMMENT '成交量',
    turnover DECIMAL(20, 4) COMMENT '成交额',
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE KEY uk_fund_date (fund_code, trade_date),
    INDEX idx_fund_code (fund_code),
    INDEX idx_trade_date (trade_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='QDII基金历史数据表';
"""