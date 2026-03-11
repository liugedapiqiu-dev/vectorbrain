# 🚀 安装指南

**版本:** 1.0  
**适用系统:** macOS, Windows, Linux

---

## 📋 目录

1. [系统要求](#系统要求)
2. [安装 OpenClaw](#安装-openclaw)
3. [安装框架](#安装框架)
4. [配置](#配置)
5. [启动服务](#启动服务)
6. [验证安装](#验证安装)
7. [跨平台说明](#跨平台说明)

---

## 系统要求

### 必需
- **Python:** 3.11+
- **Node.js:** 18+
- **Git:** 2.0+
- **磁盘空间:** 10GB+

### 可选
- **Ollama:** 本地模型（推荐 qwen2.5:14b）
- **DashScope API Key:** 云端模型

---

## 安装 OpenClaw

### macOS/Linux
```bash
npm install -g openclaw
openclaw --version
```

### Windows
```powershell
# 管理员权限运行
npm install -g openclaw
openclaw --version
```

---

## 安装框架

### 方法 1: Git 克隆（推荐）

```bash
# macOS/Linux
git clone https://github.com/liugedapiqiu-dev/vectorbrain.git
cd vectorbrain
pip install -r requirements.txt

# Windows
git clone https://github.com/liugedapiqiu-dev/vectorbrain.git
cd vectorbrain
python -m pip install -r requirements.txt
```

### 方法 2: 下载 ZIP

1. 访问 https://github.com/liugedapiqiu-dev/vectorbrain
2. 点击 "Code" → "Download ZIP"
3. 解压
4. 安装依赖

---

## 配置

### 步骤 1: 复制配置模板

```bash
cp config/config.example.json config/config.json
```

### 步骤 2: 编辑配置

```bash
# macOS/Linux
nano config/config.json

# Windows
notepad config/config.json
```

### 步骤 3: 填写配置

**必须配置:**
- `cloud.api_key`: 你的 DashScope API Key
- `ollama.enabled`: 是否启用本地模型（true/false）

**可选配置:**
- `ollama.model`: 本地模型名称
- `network_monitor.check_interval`: 网络检测间隔（秒）

---

## 启动服务

### 启动 Dashboard

```bash
# macOS/Linux
python connector/dashboard_server.py

# Windows
python connector\dashboard_server.py
```

访问：http://localhost:18790

### 启动网络监控

```bash
# 后台运行
python connector/network_monitor.py &

# Windows (PowerShell)
Start-Process python -ArgumentList "connector/network_monitor.py" -WindowStyle Hidden
```

### 启动任务监控

```bash
# 后台运行
python connector/task_monitor_service.py &
```

---

## 验证安装

### 运行健康检查

```bash
python scripts/health_check.py
```

**预期输出:**
```
✅ OpenClaw Gateway - 运行中
✅ Ollama Serve - 运行中（如已安装）
✅ Network Monitor - 运行中
✅ Dashboard - 运行中
健康评分：🟢 95/100
```

### 测试 Dashboard

打开浏览器访问：http://localhost:18790

**应该看到:**
- 💚 系统健康状态
- 📊 CPU/内存使用率
- 🧩 脚本运行状态
- 📋 定时任务监控

---

## 跨平台说明

### macOS
- 使用 Homebrew 安装依赖：`brew install python@3.11 node git`
- 使用 cron 设置定时任务

### Windows
- 使用 PowerShell 运行脚本
- 使用任务计划程序设置定时任务
- 参考 `docs/WINDOWS_INSTALL.md`

### Linux
- 使用系统包管理器安装依赖
- 使用 systemd 或 cron 设置定时任务

---

## 下一步

安装完成后：
1. 📖 阅读 `docs/CONFIGURATION.md` 了解详细配置
2. 🎯 配置你的第一个定时任务
3. 📊 访问 Dashboard 监控系统
4. 🎓 查看示例和最佳实践

---

## 遇到问题？

- 📚 查看 `docs/TROUBLESHOOTING.md`
- 💬 提交 Issue
- 📧 联系社区
