# 🏗️ VectorBrain 架构详解

**最后更新:** 2026-03-11  
**版本:** 1.0  
**阅读时间:** 20 分钟

---

## 📋 目录

1. [整体架构](#整体架构)
2. [核心组件](#核心组件)
3. [数据流](#数据流)
4. [模块详解](#模块详解)
5. [部署架构](#部署架构)

---

## 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                      用户 (任何平台)                        │
│                          👤                                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ 消息/命令
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    OpenClaw Gateway                         │
│                      🚪 消息网关                             │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │  消息路由   │  │  Hooks 系统  │  │  技能调度系统       │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
         │                    │
         │ Hooks 调用         │ 技能调用
         ▼                    ▼
┌─────────────────┐  ┌─────────────────────────────────────┐
│  VectorBrain    │  │  VectorBrain 技能包                 │
│  Connector      │  │                                     │
│  (钩子)         │  │  ┌──────────────┐ ┌──────────────┐ │
│                 │  │  │ 记忆检索技能 │ │ 任务管理技能 │ │
│  - message:new  │  │  └──────────────┘ └──────────────┘ │
│  - command:new  │  │  ┌──────────────┐ ┌──────────────┐ │
│                 │  │  │ 机会扫描技能 │ │ 网络监控技能 │ │
│                 │  │  └──────────────┘ └──────────────┘ │
└─────────────────┘  └─────────────────────────────────────┘
         │
         │ 数据读写
         ▼
┌─────────────────────────────────────────────────────────────┐
│                    VectorBrain 大脑系统                     │
│                        🧠 记忆层                             │
│                                                             │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │  episodic_memory │  │  knowledge_memory│                │
│  │  情景记忆        │  │  知识记忆        │                │
│  │  (对话历史)      │  │  (提炼知识)      │                │
│  └──────────────────┘  └──────────────────┘                │
│                                                             │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │   reflections    │  │     tasks        │                │
│  │   反思记录       │  │   任务队列       │                │
│  └──────────────────┘  └──────────────────┘                │
│                                                             │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │   opportunities  │  │     goals        │                │
│  │   机会发现       │  │   目标系统       │                │
│  └──────────────────┘  └──────────────────┘                │
└─────────────────────────────────────────────────────────────┘
```

---

## 核心组件

### 1. OpenClaw Connector

**位置:** `connector/openclaw_connector.py`

**职责:**
- 监听 OpenClaw 消息和命令
- 保存消息到 VectorBrain 记忆
- 检索相关记忆并注入上下文
- 执行 VectorBrain 任务

**Hooks:**
- `message:new` - 新消息处理
- `command:new` - 新命令处理

---

### 2. Network Monitor

**位置:** `connector/network_monitor.py`

**职责:**
- 每 10 秒检测一次网络
- 连续 6 次失败后判定断网
- 自动切换到本地模型
- 网络恢复后切回云端

**配置:**
```json
{
  "check_interval": 10,
  "fail_threshold": 6,
  "check_urls": [
    "8.8.8.8",
    "https://dashscope.aliyuncs.com"
  ]
}
```

---

### 3. Task Manager

**位置:** `connector/task_manager.py`

**职责:**
- 查询待处理任务
- 原子性抢占任务
- 执行任务
- 回写执行结果

**安全机制:**
- 原子性 UPDATE + ROW COUNT 验证
- 超时机制（30 分钟）
- flock 文件锁

---

### 4. Smart Proxy

**位置:** `connector/smart_proxy.py`

**职责:**
- 智能模型路由
- 云端超时自动降级
- 本地模型备用

**工作流:**
```
请求 → 云端模型 (3 秒超时)
        ↓ 失败
     本地模型 (120 秒)
        ↓
     返回结果
```

---

### 5. Opportunity Poller

**位置:** `connector/opportunity_poller.py`

**职责:**
- 轮询 opportunities 数据库
- 查找高优先级未处理机会
- 发送通知
- 更新状态

---

## 数据流

### 消息处理流程

```
用户发送消息
    ↓
OpenClaw Gateway
    ↓
message:new Hook
    ↓
VectorBrain Connector
    ↓
┌─────────────────────┐
│ 1. 保存消息到记忆   │
│ 2. 检索相关记忆     │
│ 3. 注入上下文       │
│ 4. 返回给 OpenClaw  │
└─────────────────────┘
    ↓
OpenClaw 生成回复
    ↓
用户收到回复
```

### 断网降级流程

```
网络正常
    ↓
使用云端模型
    ↓
网络检测失败
    ↓
连续 6 次失败（60 秒）
    ↓
切换到本地模型
    ↓
发送通知
    ↓
网络恢复
    ↓
切换回云端模型
    ↓
发送通知
```

### 任务执行流程

```
任务创建
    ↓
任务队列 (queued)
    ↓
Task Manager 轮询
    ↓
抢占任务 (running)
    ↓
执行任务
    ↓
┌──────────────┐
│ 成功 → completed │
│ 失败 → failed    │
└──────────────┘
    ↓
回写结果
```

---

## 模块详解

### 记忆系统

**数据库:**
- `episodic_memory.db` - 情景记忆（对话历史）
- `knowledge_memory.db` - 知识记忆（提炼知识）
- `reflections.db` - 反思记录
- `tasks.db` - 任务队列
- `opportunities.db` - 机会发现
- `goals.db` - 目标系统

**记忆检索:**
```python
# 向量检索
from vector_search import search_memories

memories = search_memories(query, limit=5, threshold=0.7)

# 注入上下文
context = "\n".join([m['value'] for m in memories])
```

### 任务系统

**任务状态:**
- `queued` - 待处理
- `running` - 执行中
- `completed` - 已完成
- `failed` - 失败

**任务优先级:**
- 1-3: 高优先级
- 4-7: 中优先级
- 8-10: 低优先级

---

## 部署架构

### 单节点部署

```
单台服务器
├── OpenClaw Gateway
├── VectorBrain Connector
├── Network Monitor
├── Task Manager
├── Smart Proxy
└── Dashboard (18790)
```

### 多节点部署（推荐）

```
节点 1 (主节点)
├── OpenClaw Gateway
├── VectorBrain Connector
└── Dashboard

节点 2 (工作节点)
├── Network Monitor
├── Task Manager
└── Smart Proxy

节点 3 (数据库节点)
├── VectorBrain 数据库
└── 备份系统
```

---

## 性能优化

### 数据库优化

```sql
-- 创建索引
CREATE INDEX idx_timestamp ON episodes(timestamp);
CREATE INDEX idx_status ON tasks(status);
CREATE INDEX idx_severity ON opportunities(severity);

-- 定期清理旧数据
DELETE FROM episodes WHERE created_at < datetime('now', '-30 days');
```

### 缓存策略

```python
# 使用 LRU 缓存
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_memory(key):
    # 从数据库读取
    pass
```

---

## 监控和告警

### 健康检查

```bash
# 运行健康检查
python scripts/health_check.py

# 检查服务状态
systemctl status openclaw
systemctl status vectorbrain
```

### 日志监控

```bash
# 实时查看日志
tail -f logs/connector.log
tail -f logs/network_monitor.log
tail -f logs/task_manager.log

# 错误日志
grep ERROR logs/*.log | tail -20
```

---

## 📚 相关文档

- [安装指南](INSTALL.md)
- [配置详解](CONFIGURATION.md)
- [OpenClaw 集成](OPENCLAW_INTEGRATION.md)
- [故障排查](TROUBLESHOOTING.md)
