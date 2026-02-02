# 基金估值API文档

## 🎯 概述

基金估值后端API服务，提供场外基金实时估值查询功能，支持单个查询、批量查询、搜索和历史数据查询。

## 🚀 快速开始

### 安装依赖

```bash
pip install flask flask-cors pymysql akshare pandas
```

### 启动服务

```bash
cd my-trade
python fund_estimate_api.py
```

服务将在 `http://localhost:8083` 启动。

## 📡 API接口

### 1. 查询单个基金估值

**请求:**
```
GET /api/fund/estimate/<fund_code>?use_cache=true
```

**路径参数:**
- `fund_code`: 基金代码（6位数字），如 `000001`

**查询参数:**
- `use_cache`: 是否使用缓存，默认 `true`

**响应示例:**
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
  "message": "查询成功",
  "cached": false
}
```

**TypeScript接口定义:**
```typescript
interface FundEstimate {
  code: string              // 基金代码
  estimateNav: number       // 估算净值
  estimateChange: number    // 估算涨跌幅（%）
  estimateChangeAmount: number  // 估算涨跌额
  estimateTime: string      // 估算时间
  updateTime: string        // 上次更新时间
}
```

### 2. 批量查询基金估值

**请求:**
```
POST /api/fund/estimate/batch
Content-Type: application/json

{
  "codes": ["000001", "161116", "110022"]
}
```

**响应示例:**
```json
{
  "success": true,
  "data": [
    {
      "code": "000001",
      "estimateNav": 1.1806,
      "estimateChange": 0.65,
      "estimateChangeAmount": 0.0076,
      "estimateTime": "2026-02-01 22:00:00",
      "updateTime": "2026-02-01 22:00:00"
    },
    {
      "code": "161116",
      "estimateNav": 2.0366,
      "estimateChange": -0.03,
      "estimateChangeAmount": -0.0006,
      "estimateTime": "2026-02-01 22:00:00",
      "updateTime": "2026-02-01 22:00:00"
    }
  ],
  "failed": [
    {
      "code": "110022",
      "reason": "未找到数据"
    }
  ],
  "message": "查询成功 2/3 个基金，1 个失败"
}
```

### 3. 搜索基金

**请求:**
```
GET /api/fund/search?keyword=黄金
```

**查询参数:**
- `keyword`: 搜索关键词（基金代码或名称）

**响应示例:**
```json
{
  "success": true,
  "data": [
    {
      "code": "161116",
      "name": "易方达黄金主题人民币A",
      "estimateNav": 2.0366,
      "estimateChange": -0.03
    },
    {
      "code": "007977",
      "name": "易方达黄金主题美元现汇A",
      "estimateNav": 2.0366,
      "estimateChange": -0.03
    }
  ],
  "message": "找到 2 个相关基金"
}
```

### 4. 查询历史估值数据

**请求:**
```
GET /api/fund/history/<fund_code>?days=7
```

**路径参数:**
- `fund_code`: 基金代码（6位数字）

**查询参数:**
- `days`: 获取最近N天的数据，默认7天，最大30天

**响应示例:**
```json
{
  "success": true,
  "data": [
    {
      "code": "000001",
      "name": "华夏成长混合",
      "estimateNav": 1.1806,
      "estimateChange": 0.65,
      "estimateChangeAmount": 0.0076,
      "estimateTime": "2026-02-01 14:30:00",
      "updateTime": "2026-02-01 14:30:00"
    },
    {
      "code": "000001",
      "name": "华夏成长混合",
      "estimateNav": 1.1730,
      "estimateChange": -0.51,
      "estimateChangeAmount": -0.0060,
      "estimateTime": "2026-01-31 14:30:00",
      "updateTime": "2026-01-31 14:30:00"
    }
  ],
  "message": "查询成功，共 2 条记录"
}
```

### 5. 健康检查

**请求:**
```
GET /api/health
```

**响应示例:**
```json
{
  "status": "ok",
  "timestamp": "2026-02-01 22:00:00"
}
```

## 🔧 前端集成示例

### React + TypeScript

```typescript
// types.ts
export interface FundEstimate {
  code: string
  estimateNav: number
  estimateChange: number
  estimateChangeAmount: number
  estimateTime: string
  updateTime: string
}

export interface ApiResponse<T> {
  success: boolean
  data: T
  message: string
  cached?: boolean
}

// api.ts
const API_BASE_URL = 'http://localhost:8083/api'

export const fundApi = {
  // 查询单个基金
  async getEstimate(fundCode: string, useCache = true): Promise<FundEstimate> {
    const response = await fetch(
      `${API_BASE_URL}/fund/estimate/${fundCode}?use_cache=${useCache}`
    )
    const result: ApiResponse<FundEstimate> = await response.json()
    
    if (!result.success) {
      throw new Error(result.message)
    }
    
    return result.data
  },

  // 批量查询
  async getEstimateBatch(codes: string[]): Promise<FundEstimate[]> {
    const response = await fetch(`${API_BASE_URL}/fund/estimate/batch`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ codes })
    })
    const result: ApiResponse<FundEstimate[]> = await response.json()
    
    if (!result.success) {
      throw new Error(result.message)
    }
    
    return result.data
  },

  // 搜索基金
  async search(keyword: string) {
    const response = await fetch(
      `${API_BASE_URL}/fund/search?keyword=${encodeURIComponent(keyword)}`
    )
    const result = await response.json()
    
    if (!result.success) {
      throw new Error(result.message)
    }
    
    return result.data
  },

  // 查询历史数据
  async getHistory(fundCode: string, days = 7): Promise<FundEstimate[]> {
    const response = await fetch(
      `${API_BASE_URL}/fund/history/${fundCode}?days=${days}`
    )
    const result: ApiResponse<FundEstimate[]> = await response.json()
    
    if (!result.success) {
      throw new Error(result.message)
    }
    
    return result.data
  }
}

// Component.tsx
import React, { useState, useEffect } from 'react'
import { fundApi, FundEstimate } from './api'

export const FundEstimateCard: React.FC<{ code: string }> = ({ code }) => {
  const [estimate, setEstimate] = useState<FundEstimate | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchEstimate = async () => {
      try {
        setLoading(true)
        const data = await fundApi.getEstimate(code)
        setEstimate(data)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchEstimate()
    
    // 每分钟刷新一次
    const interval = setInterval(fetchEstimate, 60000)
    return () => clearInterval(interval)
  }, [code])

  if (loading) return <div>加载中...</div>
  if (error) return <div>错误: {error}</div>
  if (!estimate) return null

  return (
    <div className="fund-card">
      <h3>基金代码: {estimate.code}</h3>
      <div className="estimate-nav">
        估算净值: {estimate.estimateNav.toFixed(4)}
      </div>
      <div className={`estimate-change ${estimate.estimateChange >= 0 ? 'up' : 'down'}`}>
        涨跌幅: {estimate.estimateChange.toFixed(2)}%
        ({estimate.estimateChange >= 0 ? '+' : ''}{estimate.estimateChangeAmount.toFixed(4)})
      </div>
      <div className="estimate-time">
        估算时间: {estimate.estimateTime}
      </div>
    </div>
  )
}
```

### Vue 3 + TypeScript

```typescript
// api.ts
import { ref } from 'vue'

export interface FundEstimate {
  code: string
  estimateNav: number
  estimateChange: number
  estimateChangeAmount: number
  estimateTime: string
  updateTime: string
}

const API_BASE_URL = 'http://localhost:8083/api'

export function useFundEstimate(fundCode: string) {
  const estimate = ref<FundEstimate | null>(null)
  const loading = ref(true)
  const error = ref<string | null>(null)

  const fetchEstimate = async () => {
    try {
      loading.value = true
      const response = await fetch(`${API_BASE_URL}/fund/estimate/${fundCode}`)
      const result = await response.json()
      
      if (result.success) {
        estimate.value = result.data
        error.value = null
      } else {
        error.value = result.message
      }
    } catch (err) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  return {
    estimate,
    loading,
    error,
    fetchEstimate
  }
}

// Component.vue
<template>
  <div v-if="loading">加载中...</div>
  <div v-else-if="error">错误: {{ error }}</div>
  <div v-else-if="estimate" class="fund-card">
    <h3>基金代码: {{ estimate.code }}</h3>
    <div class="estimate-nav">
      估算净值: {{ estimate.estimateNav.toFixed(4) }}
    </div>
    <div :class="['estimate-change', estimate.estimateChange >= 0 ? 'up' : 'down']">
      涨跌幅: {{ estimate.estimateChange.toFixed(2) }}%
      ({{ estimate.estimateChange >= 0 ? '+' : '' }}{{ estimate.estimateChangeAmount.toFixed(4) }})
    </div>
    <div class="estimate-time">
      估算时间: {{ estimate.estimateTime }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'
import { useFundEstimate } from './api'

const props = defineProps<{
  code: string
}>()

const { estimate, loading, error, fetchEstimate } = useFundEstimate(props.code)

onMounted(() => {
  fetchEstimate()
  const interval = setInterval(fetchEstimate, 60000)
  
  onUnmounted(() => {
    clearInterval(interval)
  })
})
</script>
```

## 🗄️ 数据库配置

### MySQL表结构

```sql
CREATE TABLE IF NOT EXISTS fund_estimate (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fund_code VARCHAR(10) NOT NULL COMMENT '基金代码',
    fund_name VARCHAR(100) COMMENT '基金名称',
    estimate_nav DECIMAL(10, 4) COMMENT '估算净值',
    estimate_change DECIMAL(8, 4) COMMENT '估算涨跌幅(%)',
    estimate_change_amount DECIMAL(10, 4) COMMENT '估算涨跌额',
    estimate_time DATETIME COMMENT '估算时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    UNIQUE KEY uk_fund_code_time (fund_code, estimate_time),
    INDEX idx_fund_code (fund_code),
    INDEX idx_estimate_time (estimate_time),
    INDEX idx_update_time (update_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='基金估值数据表';
```

### 配置数据库

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

## 🔍 错误处理

### 错误响应格式

```json
{
  "success": false,
  "data": null,
  "message": "错误信息描述"
}
```

### 常见错误码

| HTTP状态码 | 说明 |
|-----------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |
| 503 | 服务不可用 |

## 📊 性能优化

1. **缓存机制**: 使用 `use_cache=true` 参数从数据库缓存读取数据
2. **批量查询**: 使用批量接口一次查询多个基金
3. **数据库索引**: 已为常用查询字段建立索引
4. **连接池**: 数据库连接自动管理

## 🐛 故障排查

### 问题1: 数据库连接失败

**原因**: MySQL未启动或配置错误

**解决**: 
1. 检查MySQL服务是否启动
2. 确认 `database_config.py` 配置正确
3. 服务会自动降级为纯API模式

### 问题2: 查询返回空数据

**原因**: 基金代码不存在或非交易时间

**解决**:
1. 确认基金代码正确
2. 检查是否为场外基金
3. 交易时间内数据更新

### 问题3: CORS错误

**原因**: 跨域请求被阻止

**解决**: 
- 服务已启用CORS，确认前端请求URL正确
- 使用代理或配置nginx转发

## 📝 日志

服务运行日志示例:

```
2026-02-01 22:00:00 - root - INFO - ================================================================================
2026-02-01 22:00:00 - root - INFO - 基金估值API服务启动中...
2026-02-01 22:00:00 - root - INFO - ================================================================================
2026-02-01 22:00:00 - root - INFO - API端点:
2026-02-01 22:00:00 - root - INFO -   GET  /api/fund/estimate/<fund_code>  - 查询单个基金估值
2026-02-01 22:00:00 - root - INFO -   POST /api/fund/estimate/batch        - 批量查询基金估值
2026-02-01 22:00:00 - root - INFO -   GET  /api/fund/search?keyword=xxx    - 搜索基金
2026-02-01 22:00:00 - root - INFO -   GET  /api/fund/history/<fund_code>   - 查询历史估值数据
2026-02-01 22:00:00 - root - INFO -   GET  /api/health                     - 健康检查
2026-02-01 22:00:00 - root - INFO - ================================================================================
2026-02-01 22:00:00 - root - INFO - 数据库状态: ✅ 已连接
2026-02-01 22:00:00 - root - INFO - ================================================================================
```

## 🚀 部署建议

### 生产环境部署

1. **使用Gunicorn**:
```bash
gunicorn -w 4 -b 0.0.0.0:8083 fund_estimate_api:app
```

2. **使用Nginx反向代理**:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /api/ {
        proxy_pass http://localhost:8083;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

3. **使用Docker**:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8083", "fund_estimate_api:app"]
```

## 📄 许可证

MIT License

---

**文档版本**: 1.0  
**最后更新**: 2026-02-01
