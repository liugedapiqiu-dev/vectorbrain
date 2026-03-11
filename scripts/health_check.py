#!/usr/bin/env python3
"""
健康检查脚本 - 检查所有服务的运行状态
"""

import subprocess
import sys

def check_service(name, pattern):
    """检查服务是否在运行"""
    try:
        result = subprocess.run(
            ["pgrep", "-f", pattern],
            capture_output=True,
            text=True
        )
        return len(result.stdout.strip().split('\n')) > 0
    except:
        return False

def main():
    print("=" * 60)
    print("🦞 系统健康检查")
    print("=" * 60)
    
    services = [
        ("OpenClaw Gateway", "openclaw"),
        ("Ollama Serve", "ollama serve"),
        ("Network Monitor", "network_monitor.py"),
        ("Task Monitor", "task_monitor_service.py"),
        ("Dashboard", "dashboard_server.py"),
    ]
    
    running = 0
    for name, pattern in services:
        status = "✅" if check_service(name, pattern) else "❌"
        print(f"{status} {name}")
        if check_service(name, pattern):
            running += 1
    
    print("=" * 60)
    health_score = int((running / len(services)) * 100)
    print(f"健康评分：{'🟢' if health_score >= 80 else '🟡' if health_score >= 60 else '🔴'} {health_score}/100")
    print(f"运行中：{running}/{len(services)} 服务")
    print("=" * 60)
    
    return 0 if health_score >= 80 else 1

if __name__ == "__main__":
    sys.exit(main())
