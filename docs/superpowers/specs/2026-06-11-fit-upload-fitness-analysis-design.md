# FIT 文件上传与骑行水平分析 — 设计文档

日期: 2026-06-11

## 1. 概述

用户可上传 FIT 文件（Garmin/码表格式），系统自动解析骑行数据，计算 FTP 和骑行水平，并用体能数据评估路线难度。

## 2. 数据模型

### 2.1 新增表 `activity_records`

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BigInteger PK | 自增 |
| user_id | BigInteger FK | 关联 User |
| name | String(128) | 活动名称 |
| fit_oss_url | String(1024) | 原始 FIT 文件 OSS 地址 |
| distance | Float | 总距离 (m) |
| duration | Float | 总时长 (s) |
| elevation_gain | Float | 累计爬升 (m) |
| avg_speed | Float | 平均速度 (km/h) |
| avg_hr | Float | 平均心率 (bpm) |
| avg_power | Float | 平均功率 (W), NULLABLE |
| avg_cadence | Float | 平均踏频 (rpm) |
| max_hr | Float | 最大心率 |
| max_power | Float | 最大功率 |
| np | Float | 标准化功率 |
| tss | Float | 训练压力分数 |
| if_score | Float | 强度因子 |
| power_curve | JSON | 关键时长功率点 |
| hr_zones | JSON | 心率区间分布 |
| track_data | JSON | 轨迹点（存 OSS，API 返回时动态加载） |
| device_info | String(128) | 设备名称 |
| start_time | DateTime | 活动开始时间 |
| track_points | Integer | 轨迹点数 |
| created_at | DateTime | 上传时间 |

### 2.2 新增表 `fitness_profiles`

| 字段 | 类型 | 说明 |
|------|------|------|
| user_id | BigInteger PK | 关联 User |
| ftp | Float | 当前 FTP (W) |
| ftp_wkg | Float | 功体比 (W/kg) |
| ftp_confidence | Float | 置信度 0-1 |
| fitness_level | String(16) | beginner/amateur/advanced/expert |
| updated_at | DateTime | 更新时间 |

## 3. API

### 3.1 活动记录

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/activities` | GET | 列表，分页 |
| `/api/activities` | POST | 上传 FIT (multipart, max 10MB) |
| `/api/activities/{id}` | GET | 详情，含轨迹点、功率曲线、心率区间 |
| `/api/activities/{id}` | DELETE | 删除 + OSS 清理 |

### 3.2 骑行水平

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/fitness` | GET | 当前 FTP、功体比、等级、置信度 |
| `/api/fitness/history` | GET | FTP 变化趋势 |

### 3.3 路线评估

在 `GET /api/routes/{id}` 返回中新增 `fitness_match` 字段：

```json
{
  "fit_level": "适合",
  "estimated_completion": 5400,
  "key_challenges": ["2级爬坡需要较好体能"],
  "ftp_required": 220,
  "your_ftp": 245
}
```

## 4. 核心算法

### 4.1 FIT 解析

- 库：`fitdecode`
- 提取 FIT 文件中的 record 消息：timestamp, lat, lon, altitude, heart_rate, power, cadence, speed, distance
- 从 session/lap 消息提取汇总数据
- 计算 NP/TSS/IF（标准化功率/训练压力/强度因子）

### 4.2 Power Curve → FTP

1. 从 record 消息构建时间-功率序列
2. 遍历每个点，计算之后 5s/30s/1m/5m/10m/20m/30m/40m/60m 的平均功率，记录最大值
3. 合并所有历史活动的 Power Curve，每个时长取全局最大值
4. FTP 候选：`20m×0.95`、`30m×0.97`、`40m×0.99`、`60m×1.00`
5. 加权平均合并所有候选值（权重：20m=0.3, 30m=0.3, 40m=0.2, 60m=0.2），有完整数据时权重之和=1.0，缺某个时长时按比例缩放
6. 最近 3 条记录的 FTP 加权平均（时间越近权重越高：0.5/0.3/0.2），不足 3 条全用（1 条权 1.0，2 条权 0.6/0.4）

### 4.3 等级评定

有功率数据：

| 功体比 (W/kg) | 等级 |
|-------------|------|
| < 1.5 | beginner |
| 1.5 – 2.5 | amateur |
| 2.5 – 3.5 | advanced |
| 3.5 – 4.5 | expert |
| > 4.5 | pro |

无功率数据时退到经验分级：根据用户历史活动的平均速度、爬升能力、骑行距离综合定级。

### 4.4 路线难度评估

```
VAM = 爬升 / 时间
需求功率 ≈ 滚动阻力 + 爬坡 + 风阻
需求 W/kg = 需求功率 / 用户体重
```

匹配判定：

| 用户 vs 需求 | 评估 |
|-------------|------|
| 用户 > 需求 × 1.2 | 轻松 |
| 用户 在 需求 × [0.8, 1.2] | 适合 |
| 用户 在 需求 × [0.5, 0.8) | 有挑战 |
| 用户 < 需求 × 0.5 | 超出能力 |

## 5. 文件存储

- 原始 FIT 文件存 OSS：`activities/{user_id}/{timestamp}_{uuid}.fit`
- 轨迹点（track_data JSON）较大时存 OSS，API 返回时动态加载
- 活动详情 API 返回轨迹点供前端渲染地图

## 6. 技术栈

- FIT 解析：`fitdecode`
- 后端框架：FastAPI (已有)
- DB：MySQL + SQLAlchemy (已有)
- 文件存储：阿里云 OSS (已有)
- 前端：Vue 3 + Element Plus + Baidu Maps + Canvas 图表 (已有)

## 7. 前端新增页面

- 活动上传按钮（导航栏或路书页）
- 活动列表页（卡片式，摘要数据）
- 活动详情页：轨迹地图 + 功率曲线 + 心率区间饼图 + 数据摘要，类似 Strava

## 8. 新增依赖

- `fitdecode` — FIT 文件解析
- 无需额外系统依赖

## 9. 文件清单（预估）

| 文件 | 用途 |
|------|------|
| `app/models.py` | 新增 ORM 模型 |
| `app/api/v1/activity_routes.py` | 活动 CRUD 路由 |
| `app/api/v1/fitness_routes.py` | 体能查询路由 |
| `app/api/v1/schemas.py` | 新增 Pydantic schema |
| `app/services/fit_service.py` | FIT 解析、Power Curve、NP/TSS/IF 计算 |
| `app/services/fitness_service.py` | FTP 估算、等级评定、路线匹配 |
| `tests/test_fit_service.py` | FIT 服务测试 |
| `tests/test_fitness_service.py` | 体能服务测试 |
| `static/index.html` | 前端页面新增 |
| `static/css/style.css` | 样式新增 |
| `pyproject.toml` | 添加 fitdecode 依赖 |
