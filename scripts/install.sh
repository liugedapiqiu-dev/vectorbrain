#!/bin/bash
# VectorBrain 自动安装脚本
# 适用系统：macOS, Linux

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/.."

echo ""
echo "========================================"
echo "  🚀 VectorBrain 自动安装脚本"
echo "========================================"
echo ""

# 检查 Python 版本
log_info "检查 Python 版本..."
if ! command -v python3 &> /dev/null; then
    log_error "Python 3 未安装，请先安装 Python 3.11+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
log_success "Python $PYTHON_VERSION 已安装"

# 检查 Node.js 版本
log_info "检查 Node.js 版本..."
if ! command -v node &> /dev/null; then
    log_warning "Node.js 未安装，OpenClaw 需要 Node.js 18+"
else
    NODE_VERSION=$(node --version)
    log_success "Node.js $NODE_VERSION 已安装"
fi

# 检查 OpenClaw
log_info "检查 OpenClaw..."
if ! command -v openclaw &> /dev/null; then
    log_warning "OpenClaw 未安装"
    echo ""
    log_info "安装 OpenClaw:"
    echo "  npm install -g openclaw"
    echo ""
    read -p "是否现在安装 OpenClaw? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        npm install -g openclaw
        log_success "OpenClaw 安装完成"
    fi
else
    OPENCLAW_VERSION=$(openclaw --version)
    log_success "OpenClaw $OPENCLAW_VERSION 已安装"
fi

# 安装 Python 依赖
log_info "安装 Python 依赖..."
pip3 install -r requirements.txt
log_success "依赖安装完成"

# 初始化数据库
log_info "初始化 VectorBrain 数据库..."
python3 scripts/init_databases.py
log_success "数据库初始化完成"

# 创建 OpenClaw 技能目录
log_info "创建 OpenClaw 技能目录..."
SKILLS_DIR="$HOME/.openclaw/skills/vectorbrain"
mkdir -p "$SKILLS_DIR"
log_success "技能目录创建完成：$SKILLS_DIR"

# 复制文件
log_info "复制文件到技能目录..."
cp -r * "$SKILLS_DIR/"
log_success "文件复制完成"

# 配置模板
log_info "配置技能..."
cd "$SKILLS_DIR"

if [ ! -f config/config.json ]; then
    cp config/config.example.json config/config.json
    log_warning "请编辑 config/config.json 填入你的 API Key"
    echo "  nano config/config.json"
else
    log_success "配置文件已存在"
fi

if [ ! -f skill.json ]; then
    cp skill.json.example skill.json
    log_success "技能配置已创建"
fi

# 启用技能
log_info "启用 VectorBrain 技能..."
if command -v openclaw &> /dev/null; then
    openclaw skills enable vectorbrain 2>/dev/null || log_warning "技能启用失败，请手动启用"
    log_success "技能启用完成"
else
    log_warning "OpenClaw 未安装，跳过技能启用"
fi

# 运行测试
log_info "运行集成测试..."
python3 scripts/test_integration.py

echo ""
echo "========================================"
echo "  🎉 安装完成！"
echo "========================================"
echo ""
echo "下一步:"
echo "  1. 编辑配置文件:"
echo "     nano $SKILLS_DIR/config/config.json"
echo ""
echo "  2. 添加 API Key 到配置"
echo ""
echo "  3. 重启 OpenClaw:"
echo "     openclaw gateway restart"
echo ""
echo "  4. 测试功能:"
echo "     发送消息：@阿豪 测试"
echo ""
echo "文档:"
echo "  - 快速启动：cat QUICKSTART.md"
echo "  - 安装指南：cat docs/INSTALL.md"
echo "  - 配置详解：cat docs/CONFIGURATION.md"
echo ""
echo "GitHub: https://github.com/liugedapiqiu-dev/vectorbrain"
echo ""
echo "========================================"
echo ""
