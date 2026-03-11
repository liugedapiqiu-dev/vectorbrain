# 🔌 OpenClaw 集成指南

**最后更新:** 2026-03-11  
**难度:** ⭐⭐⭐⭐  
**阅读时间:** 30 分钟

---

## 📋 目录

1. [集成架构](#集成架构)
2. [前置要求](#前置要求)
3. [安装 VectorBrain 技能](#安装-vectorbrain-技能)
4. [配置 OpenClaw Hooks](#配置-openclaw-hooks)
5. [注册 VectorBrain 技能](#注册-vectorbrain-技能)
6. [配置记忆系统](#配置记忆系统)
7. [测试集成](#测试集成)
8. [故障排查](#故障排查)

---

## 集成架构

```
┌─────────────────────────────────────────────────────────┐
│                    OpenClaw Gateway                     │
│                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐ │
│  │  消息路由   │  │  Hooks 系统  │  │  技能调度系统   │ │
│  └─────────────┘  └─────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────┘
         │                    │
         │ Hooks 调用         │ 技能调用
         ▼                    ▼
┌─────────────────┐  ┌─────────────────────────────────────┐
│  VectorBrain    │  │  VectorBrain 技能包                 │
│  Connector      │  │                                     │
│  (钩子)         │  │  - 记忆检索技能                     │
│                 │  │  - 任务管理技能                     │
│  - message:new  │  │  - 机会扫描技能                     │
│  - command:new  │  │  - 网络监控技能                     │
└─────────────────┘  └─────────────────────────────────────┘
```

---

## 前置要求

### 1. 安装 OpenClaw

```bash
# macOS/Linux
npm install -g openclaw

# Windows (管理员权限)
npm install -g openclaw

# 验证安装
openclaw --version
```

### 2. 配置 OpenClaw

```bash
# 运行配置向导
openclaw configure
```

**需要配置:**
- Feishu App ID 和 Secret
- DashScope API Key
- 其他插件配置

### 3. 下载 VectorBrain 框架

```bash
git clone https://github.com/liugedapiqiu-dev/vectorbrain.git
cd vectorbrain

# 安装 Python 依赖
pip install -r requirements.txt
```

---

## 安装 VectorBrain 技能

### 步骤 1: 创建技能目录

```bash
# OpenClaw 技能目录
SKILLS_DIR=~/.openclaw/skills/vectorbrain

# 创建目录结构
mkdir -p $SKILLS_DIR/connector
mkdir -p $SKILLS_DIR/memory
mkdir -p $SKILLS_DIR/config
```

### 步骤 2: 复制核心文件

```bash
# 复制连接器
cp ~/vectorbrain/connector/openclaw_connector.py $SKILLS_DIR/connector/

# 复制技能脚本
cp ~/vectorbrain/connector/vector_search.py $SKILLS_DIR/
cp ~/vectorbrain/connector/task_manager.py $SKILLS_DIR/
cp ~/vectorbrain/connector/opportunity_poller.py $SKILLS_DIR/

# 复制配置文件
cp ~/vectorbrain/config/config.example.json $SKILLS_DIR/config/config.json
```

### 步骤 3: 创建技能配置文件

创建 `~/.openclaw/skills/vectorbrain/skill.json`:

```json
{
  "name": "vectorbrain",
  "version": "1.0.0",
  "description": "VectorBrain 记忆和技能系统",
  "author": "OpenClaw Community",
  "entry": "index.js",
  "hooks": {
    "message:new": {
      "enabled": true,
      "handler": "connector/openclaw_connector.py"
    },
    "command:new": {
      "enabled": true,
      "handler": "connector/openclaw_connector.py"
    }
  },
  "config": {
    "memory_db": "~/.vectorbrain/memory/knowledge_memory.db",
    "task_db": "~/.vectorbrain/tasks/task_queue.db",
    "ollama_url": "http://127.0.0.1:11434",
    "cloud_api_key": "YOUR_DASHSCOPE_API_KEY"
  }
}
```

---

## 配置 OpenClaw Hooks

### 方法 1: 使用 skill.json（推荐）

在 `~/.openclaw/skills/vectorbrain/skill.json` 中配置：

```json
{
  "hooks": {
    "message:new": {
      "enabled": true,
      "priority": 10,
      "filter": {
        "channels": ["feishu", "webchat"],
        "users": ["*"]
      }
    },
    "command:new": {
      "enabled": true,
      "priority": 5,
      "commands": ["task", "memory", "search"]
    }
  }
}
```

### 方法 2: 手动配置 Hooks

编辑 `~/.openclaw/hooks/boot.md`:

```markdown
# VectorBrain Hooks 配置

## message:new Hook
- **脚本:** `~/.openclaw/skills/vectorbrain/connector/openclaw_connector.py`
- **触发条件:** 所有新消息
- **优先级:** 10
- **功能:** 
  - 保存消息到 VectorBrain 记忆
  - 检索相关记忆
  - 注入上下文到 OpenClaw

## command:new Hook
- **脚本:** `~/.openclaw/skills/vectorbrain/connector/openclaw_connector.py`
- **触发条件:** 特定命令
- **命令列表:** task, memory, search
- **功能:**
  - 任务管理
  - 记忆检索
  - 向量搜索
```

### 方法 3: 使用 OpenClaw 配置

编辑 `~/.openclaw/config.json`:

```json
{
  "hooks": {
    "vectorbrain": {
      "enabled": true,
      "path": "~/.openclaw/skills/vectorbrain",
      "events": ["message:new", "command:new"]
    }
  }
}
```

---

## 注册 VectorBrain 技能

### 步骤 1: 在 OpenClaw 中启用技能

```bash
# 列出所有技能
openclaw skills list

# 启用 VectorBrain 技能
openclaw skills enable vectorbrain

# 验证技能状态
openclaw skills status vectorbrain
```

### 步骤 2: 配置技能参数

编辑 `~/.openclaw/skills/vectorbrain/config/config.json`:

```json
{
  "openclaw": {
    "integration_mode": "hook",
    "hook_priority": 10,
    "auto_inject_memory": true,
    "memory_inject_threshold": 0.7
  },
  "vectorbrain": {
    "memory_db": "~/.vectorbrain/memory/knowledge_memory.db",
    "episodic_db": "~/.vectorbrain/memory/episodic_memory.db",
    "task_db": "~/.vectorbrain/tasks/task_queue.db",
    "ollama": {
      "enabled": true,
      "url": "http://127.0.0.1:11434",
      "model": "qwen2.5:14b"
    },
    "cloud": {
      "enabled": true,
      "provider": "dashscope",
      "api_key": "YOUR_API_KEY",
      "model": "qwen3.5-plus"
    }
  }
}
```

### 步骤 3: 重启 OpenClaw

```bash
# 重启 Gateway
openclaw gateway restart

# 检查技能加载
openclaw gateway status
```

---

## 配置记忆系统

### 步骤 1: 初始化 VectorBrain 数据库

```bash
# 运行初始化脚本
python ~/.openclaw/skills/vectorbrain/scripts/init_memory.py
```

### 步骤 2: 配置记忆注入

编辑 `~/.openclaw/skills/vectorbrain/config/config.json`:

```json
{
  "memory": {
    "auto_inject": true,
    "injection_point": "before_llm_call",
    "max_memories": 5,
    "similarity_threshold": 0.7,
    "include_episodic": true,
    "include_knowledge": true
  }
}
```

### 步骤 3: 配置记忆保存

```json
{
  "memory": {
    "auto_save": true,
    "save_on_message": true,
    "save_on_command": true,
    "save_interval": 300,
    "batch_size": 10
  }
}
```

---

## 测试集成

### 测试 1: 检查技能加载

```bash
# 检查技能状态
openclaw skills status vectorbrain

# 预期输出:
# ✅ vectorbrain - 已启用
# ✅ Hooks 已注册
# ✅ 配置已加载
```

### 测试 2: 测试消息 Hook

```bash
# 发送测试消息（通过 Feishu 或 Webchat）
@阿豪 测试记忆保存

# 检查日志
tail -f ~/.openclaw/skills/vectorbrain/logs/connector.log

# 预期输出:
# ✅ 消息已保存到 VectorBrain
# ✅ 检索到 3 条相关记忆
# ✅ 记忆已注入上下文
```

### 测试 3: 测试命令 Hook

```bash
# 测试任务命令
/task create "测试任务"

# 测试记忆命令
/memory search "测试"

# 检查输出
# 应该看到 VectorBrain 的响应
```

### 测试 4: 测试记忆检索

```python
# 运行测试脚本
python ~/.openclaw/skills/vectorbrain/scripts/test_integration.py

# 预期结果:
# ✅ OpenClaw 连接正常
# ✅ VectorBrain 数据库连接正常
# ✅ 记忆检索正常
# ✅ 记忆注入正常
```

---

## 故障排查

### Q1: 技能未加载？

**检查:**
```bash
# 检查技能文件
ls -la ~/.openclaw/skills/vectorbrain/

# 检查 skill.json
cat ~/.openclaw/skills/vectorbrain/skill.json

# 检查日志
tail -100 /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | grep vectorbrain
```

**解决:**
```bash
# 重新启用技能
openclaw skills disable vectorbrain
openclaw skills enable vectorbrain

# 重启 Gateway
openclaw gateway restart
```

### Q2: Hooks 未触发？

**检查:**
```bash
# 检查 Hooks 配置
cat ~/.openclaw/hooks/boot.md

# 检查技能 Hooks
cat ~/.openclaw/skills/vectorbrain/skill.json | grep -A 10 hooks
```

**解决:**
```bash
# 重新注册 Hooks
python ~/.openclaw/skills/vectorbrain/scripts/register_hooks.py

# 重启 Gateway
openclaw gateway restart
```

### Q3: 记忆未保存？

**检查:**
```bash
# 检查数据库连接
python -c "import sqlite3; conn = sqlite3.connect('~/.vectorbrain/memory/knowledge_memory.db'); print('✅ 数据库连接正常')"

# 检查保存日志
tail -f ~/.openclaw/skills/vectorbrain/logs/memory.log
```

**解决:**
```bash
# 检查配置
cat ~/.openclaw/skills/vectorbrain/config/config.json | grep -A 5 auto_save

# 手动保存测试
python ~/.openclaw/skills/vectorbrain/scripts/test_save.py
```

### Q4: 记忆未注入？

**检查:**
```bash
# 检查注入配置
cat ~/.openclaw/skills/vectorbrain/config/config.json | grep -A 10 memory.injection

# 检查检索日志
tail -f ~/.openclaw/skills/vectorbrain/logs/retrieval.log
```

**解决:**
```bash
# 调整检索阈值
# 编辑 config.json，降低 similarity_threshold

# 测试检索
python ~/.openclaw/skills/vectorbrain/scripts/test_retrieval.py
```

---

## 📚 相关文档

- [安装指南](INSTALL.md)
- [配置详解](CONFIGURATION.md)
- [故障排查](TROUBLESHOOTING.md)
- [VectorBrain 架构](VECTORBRAIN_ARCH.md)

---

## 🎓 进阶主题

### 自定义 Hooks

创建自定义 Hook 处理器：
```python
# ~/.openclaw/skills/vectorbrain/connector/custom_hook.py

async def handle_message(msgCtx):
    """自定义消息处理"""
    # 你的逻辑
    pass

async def handle_command(cmdCtx):
    """自定义命令处理"""
    # 你的逻辑
    pass
```

### 扩展记忆系统

添加新的记忆类型：
```python
# ~/.openclaw/skills/vectorbrain/memory/custom_memory.py

class CustomMemory:
    def save(self, data):
        """保存自定义记忆"""
        pass
    
    def search(self, query):
        """检索自定义记忆"""
        pass
```

### 集成其他系统

集成第三方 API:
```python
# ~/.openclaw/skills/vectorbrain/integrations/external_api.py

class ExternalAPI:
    def fetch_data(self):
        """获取外部数据"""
        pass
    
    def sync_memory(self):
        """同步记忆到外部系统"""
        pass
```

---

**🎉 恭喜！你已成功将 VectorBrain 集成到 OpenClaw！**
