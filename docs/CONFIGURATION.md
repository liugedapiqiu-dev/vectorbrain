# 📖 配置详解

**最后更新:** 2026-03-11

---

## 📋 配置文件位置

```
config/
├── config.json              # 主配置文件（需手动创建）
└── config.example.json      # 配置模板
```

---

## ⚙️ 配置项说明

### 1. Ollama 配置

```json
{
  "ollama": {
    "enabled": true,           // 是否启用本地模型
    "base_url": "http://127.0.0.1:11434",  // Ollama 服务地址
    "model": "qwen2.5:14b",    // 模型名称
    "timeout": 120             // 请求超时（秒）
  }
}
```

**参数说明:**
- `enabled`: true/false - 设为 false 禁用本地模型
- `base_url`: Ollama 服务的 URL
- `model`: 使用的模型名称（需提前下载）
- `timeout`: 请求超时时间

---

### 2. 云端模型配置

```json
{
  "cloud": {
    "enabled": true,           // 是否启用云端模型
    "provider": "dashscope",   // 提供商
    "api_key": "YOUR_KEY",     // API Key
    "model": "qwen3.5-plus",   // 模型名称
    "timeout": 30              // 请求超时（秒）
  }
}
```

**获取 API Key:**
1. 访问 https://dashscope.aliyuncs.com
2. 注册/登录账号
3. 创建 API Key
4. 复制到配置文件

---

### 3. 网络监控配置

```json
{
  "network_monitor": {
    "enabled": true,           // 是否启用网络监控
    "check_interval": 10,      // 检测间隔（秒）
    "fail_threshold": 6,       // 失败阈值（次）
    "check_urls": [            // 检测目标
      "8.8.8.8",
      "https://dashscope.aliyuncs.com",
      "https://www.baidu.com"
    ]
  }
}
```

**参数说明:**
- `check_interval`: 多久检测一次网络
- `fail_threshold`: 连续失败多少次判定断网
- `check_urls`: 检测目标列表（任一成功即判定为正常）

---

### 4. Dashboard 配置

```json
{
  "dashboard": {
    "enabled": true,           // 是否启用 Dashboard
    "host": "127.0.0.1",       // 监听地址
    "port": 18790              // 监听端口
  }
}
```

**访问地址:** http://127.0.0.1:18790

---

### 5. 日志配置

```json
{
  "logging": {
    "level": "INFO",           // 日志级别
    "format": "%(asctime)s...",// 日志格式
    "log_dir": "logs"          // 日志目录
  }
}
```

**日志级别:**
- DEBUG: 调试信息
- INFO: 一般信息
- WARNING: 警告信息
- ERROR: 错误信息
- CRITICAL: 严重错误

---

## 🔒 安全建议

### 1. 保护 API Key

**❌ 不要:**
- 将 config.json 上传到 Git
- 在公开场合分享 API Key
- 将 API Key 写在代码中

**✅ 应该:**
- 使用环境变量
- 将 config.json 加入 .gitignore
- 定期更换 API Key

### 2. 使用环境变量（推荐）

创建 `.env` 文件：
```bash
DASHSCOPE_API_KEY=your_api_key_here
OLLAMA_HOST=127.0.0.1
LOG_LEVEL=INFO
```

在代码中读取：
```python
import os
api_key = os.getenv('DASHSCOPE_API_KEY')
```

---

## 🎯 配置示例

### 最小配置（仅云端）

```json
{
  "cloud": {
    "enabled": true,
    "api_key": "sk-xxx",
    "model": "qwen3.5-plus"
  },
  "ollama": {
    "enabled": false
  }
}
```

### 推荐配置（云端 + 本地）

```json
{
  "cloud": {
    "enabled": true,
    "api_key": "sk-xxx",
    "model": "qwen3.5-plus"
  },
  "ollama": {
    "enabled": true,
    "model": "qwen2.5:14b"
  },
  "network_monitor": {
    "enabled": true,
    "check_interval": 10,
    "fail_threshold": 6
  }
}
```

### 开发配置

```json
{
  "logging": {
    "level": "DEBUG",
    "log_dir": "logs"
  },
  "dashboard": {
    "port": 18790
  }
}
```

---

## 🔧 常见问题

### Q1: 配置不生效？

**检查:**
1. 文件名是否正确（config.json）
2. JSON 格式是否正确
3. 是否重启了服务

### Q2: 如何切换模型？

修改 `cloud.model` 或 `ollama.model`，然后重启服务。

### Q3: 如何关闭网络监控？

设置 `network_monitor.enabled = false`

---

## 📚 相关文档

- [安装指南](INSTALL.md)
- [故障排查](TROUBLESHOOTING.md)
- [快速入门](../README.md)
