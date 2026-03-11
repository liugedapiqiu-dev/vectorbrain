# 🚀 OpenClaw 智能助理框架

**版本:** 1.0  
**作者:** OpenClaw Community  
**许可:** MIT  
**最后更新:** 2026-03-11  
**状态:** ✅ 生产就绪

[![GitHub stars](https://img.shields.io/github/stars/liugedapiqiu-dev/vectorbrain)](https://github.com/liugedapiqiu-dev/vectorbrain/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/liugedapiqiu-dev/vectorbrain)](https://github.com/liugedapiqiu-dev/vectorbrain/network)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 功能特性

### ✅ 核心功能
- 📊 **定时任务监控** - 自动运行和监控多个后台任务
- 🌐 **断网自动降级** - 网络断开时自动切换到本地模型
- 🛡️ **智能模型路由** - 云端/本地模型自动切换
- 📈 **Dashboard 监控** - Web 界面实时监控系统状态
- 🧠 **记忆系统** - 向量记忆存储和检索
- 🔍 **机会扫描** - 自动发现系统中的机会和风险
- 🔌 **OpenClaw 集成** - 完美集成到 OpenClaw 生态系统

### 🔧 预置技能
- `memory_search` - 记忆检索技能
- `task_manager` - 任务管理技能
- `opportunity_scan` - 机会扫描技能
- `network_monitor` - 网络监控技能
- `smart_proxy` - 智能模型路由代理

---

## 🚀 快速开始

### 1. 安装 OpenClaw

```bash
# macOS/Linux
npm install -g openclaw

# Windows (管理员权限)
npm install -g openclaw

# 验证安装
openclaw --version
```

### 2. 下载框架

```bash
# 克隆仓库
git clone https://github.com/liugedapiqiu-dev/vectorbrain.git
cd vectorbrain

# 安装 Python 依赖
pip install -r requirements.txt
```

### 3. 配置

```bash
# 复制配置模板
cp config/config.example.json config/config.json
cp skill.json.example skill.json

# 编辑配置文件
# macOS/Linux: nano config/config.json
# Windows: notepad config/config.json
```

**必须配置:**
- `cloud.api_key`: 你的 DashScope API Key
- `ollama.enabled`: 是否启用本地模型
- `ollama.model`: 本地模型名称

### 4. 安装为 OpenClaw 技能

```bash
# 创建技能目录
mkdir -p ~/.openclaw/skills/vectorbrain

# 复制文件
cp -r * ~/.openclaw/skills/vectorbrain/

# 启用技能
cd ~/.openclaw/skills/vectorbrain
openclaw skills enable vectorbrain

# 重启 OpenClaw
openclaw gateway restart
```

### 5. 访问 Dashboard

```bash
# 启动 Dashboard
python connector/dashboard_server.py

# 访问 http://localhost:18790
```

---

## 📚 完整文档

### 入门指南
- **[📖 安装指南](docs/INSTALL.md)** - 详细安装步骤
- **[⚙️ 配置详解](docs/CONFIGURATION.md)** - 配置说明
- **[🔌 OpenClaw 集成](docs/OPENCLAW_INTEGRATION.md)** - 与 OpenClaw 集成指南
- **[🏗️ 架构详解](docs/ARCHITECTURE.md)** - 系统架构说明

### 进阶主题
- **[🔧 故障排查](docs/TROUBLESHOOTING.md)** - 常见问题解决
- **[💻 Windows 安装](docs/WINDOWS_INSTALL.md)** - Windows 专项指南
- **[📊 性能优化](docs/PERFORMANCE.md)** - 性能优化建议

---

## 🎯 适用场景

- ✅ **个人 AI 助理** - 搭建个人智能助理系统
- ✅ **企业自动化** - 企业级自动化解决方案
- ✅ **智能客服** - 7x24 小时智能客服系统
- ✅ **任务调度** - 分布式任务调度系统
- ✅ **监控告警** - 系统监控和告警平台
- ✅ **记忆系统** - 长期记忆存储和检索

---

## 🔧 系统要求

### 必需
- **Python:** 3.11+
- **Node.js:** 18+ (OpenClaw 要求)
- **Git:** 2.0+
- **磁盘空间:** 至少 10GB

### 可选
- **Ollama:** 本地模型运行（推荐 qwen2.5:14b）
- **DashScope API Key:** 云端模型
- **Docker:** 容器化部署

---

## 📦 目录结构

```
vectorbrain/
├── connector/              # 核心连接器脚本
│   ├── openclaw_connector.py   # OpenClaw 连接器
│   ├── network_monitor.py      # 网络监控
│   ├── task_manager.py         # 任务管理
│   ├── task_monitor_service.py # 任务监控
│   ├── smart_proxy.py          # 智能路由
│   └── opportunity_poller.py   # 机会扫描
├── scripts/                # 工具脚本
│   ├── health_check.py         # 健康检查
│   ├── test_integration.py     # 集成测试
│   └── backup.sh               # 备份脚本
├── config/                 # 配置文件
│   ├── config.json             # 主配置
│   └── config.example.json     # 配置模板
├── docs/                   # 文档
│   ├── INSTALL.md              # 安装指南
│   ├── CONFIGURATION.md        # 配置详解
│   ├── OPENCLAW_INTEGRATION.md # OpenClaw 集成
│   ├── ARCHITECTURE.md         # 架构详解
│   └── TROUBLESHOOTING.md      # 故障排查
├── skill.json.example      # 技能配置模板
├── requirements.txt        # Python 依赖
└── README.md              # 项目说明
```

---

## 🎓 学习资源

- **[OpenClaw 官方文档](https://docs.openclaw.ai)**
- **[Ollama 文档](https://ollama.ai)**
- **[DashScope 文档](https://dashscope.aliyuncs.com)**
- **[GitHub Issues](https://github.com/liugedapiqiu-dev/vectorbrain/issues)**

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 贡献方式
1. 🐛 报告 Bug
2. 💡 提出新功能建议
3. 📝 改进文档
4. 🔧 提交代码修复
5. ⭐ 给项目 Star

---

## 📄 许可

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 📬 联系方式

- **GitHub:** https://github.com/liugedapiqiu-dev/vectorbrain
- **Issues:** https://github.com/liugedapiqiu-dev/vectorbrain/issues
- **Discussions:** https://github.com/liugedapiqiu-dev/vectorbrain/discussions

---

**🌟 如果这个项目对你有帮助，请给个 Star！**
