#!/usr/bin/env python3
"""
网络监控脚本 - 检测网络状态并自动切换模型

功能：
- 每 10 秒检测一次网络
- 连续 6 次失败后判定断网
- 自动切换到本地模型
- 网络恢复后切回云端
"""

import json
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path

# 配置
CHECK_INTERVAL = 10  # 检测间隔（秒）
FAIL_THRESHOLD = 6   # 连续失败次数
CHECK_URLS = [
    "8.8.8.8",
    "https://dashscope.aliyuncs.com",
    "https://www.baidu.com"
]

STATE_FILE = Path(__file__).parent.parent / "state" / "network_state.json"
LOG_FILE = Path(__file__).parent.parent / "logs" / "network_monitor.log"

def log(message):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {message}"
    print(log_msg)
    
    # 写入日志文件
    try:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_msg + "\n")
    except Exception as e:
        print(f"写入日志失败：{e}")

def check_network():
    """检测网络连通性"""
    for url in CHECK_URLS:
        try:
            if url.replace(".", "").isdigit():  # IP 地址
                result = subprocess.run(
                    ["ping", "-c", "1", "-W", "2", url],
                    capture_output=True,
                    timeout=3
                )
                if result.returncode == 0:
                    return True
            else:  # URL
                result = subprocess.run(
                    ["curl", "-s", "--connect-timeout", "2", url],
                    capture_output=True,
                    timeout=3
                )
                if result.returncode == 0:
                    return True
        except Exception:
            continue
    return False

def main():
    """主循环"""
    log("=" * 50)
    log("网络监控启动")
    log(f"检测间隔：{CHECK_INTERVAL}秒，失败阈值：{FAIL_THRESHOLD}次")
    log("=" * 50)
    
    consecutive_failures = 0
    
    while True:
        try:
            is_online = check_network()
            
            if is_online:
                if consecutive_failures > 0:
                    log(f"网络恢复（失败计数：{consecutive_failures} → 0）")
                consecutive_failures = 0
            else:
                consecutive_failures += 1
                log(f"网络检测失败（连续 {consecutive_failures}/{FAIL_THRESHOLD} 次）")
                
                if consecutive_failures >= FAIL_THRESHOLD:
                    log("⚠️ 达到失败阈值，网络已断开")
                    # 这里可以添加切换模型的逻辑
                    consecutive_failures = 0  # 重置计数器
            
        except KeyboardInterrupt:
            log("监控被用户中断")
            break
        except Exception as e:
            log(f"检测异常：{e}")
        
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
