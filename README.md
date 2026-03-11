# 🚀 OpenClaw 智能助理框架

**版本:** 1.0  
**作者:** OpenClaw Community  
**许可:** MIT  
**最后更新:** 2026-03-11

---

## 🎯 功能特性

### ✅ 核心功能
- 📊 **定时任务监控** - 自动运行和监控多个后台任务
- 🌐 **断网自动降级** - 网络断开时自动切换到本地模型
- 🛡️ **智能模型路由** - 云端/本地模型自动切换（可选）
- 📈 **Dashboard 监控** - Web 界面实时监控系统状态
- 📦 **自动备份** - 自动备份到 GitHub

### 🔧 预置脚本
- `network_monitor.py` - 网络监控和自动切换
- `task_monitor_service.py` - 定时任务状态监控
- `smart_proxy.py` - 智能模型路由代理（可选）
- `opportunity_poller.py` - 机会扫描器
- `task_manager.py` - 任务执行引擎

---

## 🚀 快速开始

### 安装

```bash
# 1. 克隆仓库
git clone https://github.com/liugedapiqiu-dev/vectorbrain.git
cd vectorbrain

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置
cp config/config.example.json config/config.json
# 编辑 config/config.json 填入你的配置

# 4. 启动
python connector/dashboard_server.py
```

### 访问 Dashboard

打开浏览器访问：http://localhost:18790

---

## 📚 文档

- **[安装指南](docs/INSTALL.md)** - 详细安装步骤
- **[配置详解](docs/CONFIGURATION.md)** - 配置说明
- **[故障排查](docs/TROUBLESHOOTING.md)** - 常见问题解决
- **[Windows 安装](docs/WINDOWS_INSTALL.md)** - Windows 专项指南

---

## 🎯 适用场景

- ✅ 个人 AI 助理
- ✅ 企业自动化
- ✅ 智能客服
- ✅ 任务调度系统
- ✅ 监控和告警系统

---

## 🔧 系统要求

- **Python:** 3.11+
- **Node.js:** 18+ (OpenClaw 要求)
- **Git:** 2.0+
- **磁盘空间:** 至少 10GB

**可选:**
- **Ollama:** 本地模型运行

---

## 📦 目录结构

```
vectorbrain/
├── connector/              # 核心连接器脚本
│   ├── network_monitor.py      # 网络监控
│   ├── task_monitor_service.py # 任务监控
│   ├── smart_proxy.py          # 智能路由（可选）
│   └── ...
├── scripts/                # 工具脚本
│   ├── health_check.py         # 健康检查
│   └── ...
├── config/                 # 配置文件
│   ├── config.json             # 主配置
│   └── config.example.json     # 配置模板
├── docs/                   # 文档
├── requirements.txt        # Python 依赖
└── README.md              # 项目说明
```

---

## 🎓 学习资源

- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [Ollama 文档](https://ollama.ai)
- [DashScope 文档](https://dashscope.aliyuncs.com)

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可

MIT License - 详见 LICENSE 文件

---

**🌟 如果这个项目对你有帮助，请给个 Star！**
