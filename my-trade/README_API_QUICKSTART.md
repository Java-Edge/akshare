# 🚀 基金估值API - 快速入门指南

## 📋 项目说明

这是一个完整的基金估值后端API服务，为前端提供场外基金实时估值数据，完全符合您提供的TypeScript接口规范。

## ⚡ 30秒快速开始

```bash
# 1. 安装依赖
pip install flask flask-cors pymysql akshare pandas

# 2. 启动服务
python fund_estimate_api.py

# 3. 测试API（新开终端）
curl http://localhost:5000/api/fund/estimate/000001
```

就这么简单！🎉

## 📊 前端响应格式

```typescript
interface FundEstimate {
  code: string                  // 基金代码
  estimateNav: number           // 估算净值
  estimateChange: number        // 估算涨跌幅（%）
  estimateChangeAmount: number  // 估算涨跌额
  estimateTime: string          // 估算时间
  updateTime: string            // 上次更新时间
}
```

## 🎯 API接口

### 查询单个基金
```
GET /api/fund/estimate/000001
```

### 批量查询
```
POST /api/fund/estimate/batch
Body: {"codes": ["000001", "161116"]}
```

### 搜索基金
```
GET /api/fund/search?keyword=黄金
```

### 历史数据
```
GET /api/fund/history/000001?days=7
```

## 📝 响应示例

```json
{
  "success": true,
  "data": {
    "code": "000001",
    "estimateNav": 1.1806,
    "estimateChange": 0.65,
    "estimateChangeAmount": 0.0076,
    "estimateTime": "2026-02-01 22:00:00",
    "updateTime": "2026-02-01 22:00:00"
  },
  "message": "查询成功"
}
```

## 🔧 前端集成

### React
```typescript
const [data, setData] = useState<FundEstimate | null>(null)

useEffect(() => {
  fetch('http://localhost:5000/api/fund/estimate/000001')
    .then(res => res.json())
    .then(result => setData(result.data))
}, [])
```

### Vue
```typescript
const data = ref<FundEstimate | null>(null)

onMounted(async () => {
  const res = await fetch('http://localhost:5000/api/fund/estimate/000001')
  const result = await res.json()
  data.value = result.data
})
```

## 📂 核心文件

- `fund_estimate_api.py` - 🔑 REST API服务（主文件）
- `jijin_db.py` - 🔑 数据库模块
- `fund_api.py` - 基金数据查询
- `test_api_quick.py` - 快速测试
- `test_api_client.py` - 完整测试
- `API_DOCUMENTATION.md` - 完整API文档

## 🗄️ 数据库配置（可选）

编辑 `database_config.py`:

```python
MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'your_password',
    'database': 'trade',
    'charset': 'utf8mb4'
}
```

**注意**: 不配置数据库也可以运行，服务会自动降级为纯API模式。

## ✅ 功能测试

```bash
# 快速测试
python test_api_quick.py

# 完整测试（需要先启动服务）
python fund_estimate_api.py  # 终端1
python test_api_client.py    # 终端2
```

## 🎯 已完成功能

- ✅ 单个基金估值查询
- ✅ 批量基金估值查询
- ✅ 基金搜索功能
- ✅ 历史估值数据查询
- ✅ 数据库缓存机制
- ✅ CORS跨域支持
- ✅ 完整错误处理
- ✅ 健康检查接口

## 📖 详细文档

- 📘 [API完整文档](API_DOCUMENTATION.md) - 详细的接口说明和示例
- 📘 [项目总结](FUND_API_PROJECT_SUMMARY.md) - 完整的项目说明

## ⚠️ 注意事项

1. **端口**: 默认使用5000端口
2. **数据更新**: 场外基金估值仅交易日更新
3. **跨域**: 已配置CORS，前端可直接调用
4. **缓存**: 支持数据库缓存，提高查询效率

## 🐛 常见问题

### Q: 启动失败？
A: 检查端口5000是否被占用，或安装缺失的依赖。

### Q: 数据库连接失败？
A: 服务会自动降级为纯API模式，不影响基本功能。

### Q: 查询返回空数据？
A: 确认基金代码正确，且为场外基金。

## 🚀 生产部署

```bash
# 使用Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 fund_estimate_api:app
```

## 💡 下一步

1. ✅ 已完成后端API开发
2. 🔲 前端对接API
3. 🔲 添加用户认证
4. 🔲 添加更多数据源

## 📞 技术支持

- 📖 查看 [API_DOCUMENTATION.md](API_DOCUMENTATION.md) 获取详细文档
- 🐛 运行 `python test_api_quick.py` 检查问题
- 📝 查看日志了解详细错误信息

---

**开始使用，让前端开发更简单！** 🎉
