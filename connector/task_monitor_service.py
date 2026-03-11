#!/usr/bin/env python3
"""
任务监控服务 - 监控所有定时任务的运行状态

功能：
- 每 30 秒收集一次统计数据
- 监控任务运行次数、成功/失败次数
- 提供 REST API 查询状态
"""

import json
import time
import os
from datetime import datetime
from pathlib import Path

STATS_FILE = Path(__file__).parent.parent / "state" / "task_monitor_stats.json"
LOG_FILE = Path(__file__).parent.parent / "logs" / "task_monitor.log"

def log(message):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {message}"
    print(log_msg)

def collect_stats():
    """收集任务统计信息"""
    # 这里实现具体的统计逻辑
    # 实际使用时需要检查各个任务的日志文件
    stats = {
        "last_update": datetime.now().isoformat(),
        "tasks": []
    }
    return stats

def main():
    """主循环"""
    log("=" * 50)
    log("任务监控服务启动")
    log("更新间隔：30 秒")
    log("=" * 50)
    
    while True:
        try:
            stats = collect_stats()
            
            # 保存统计数据
            STATS_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(STATS_FILE, 'w', encoding='utf-8') as f:
                json.dump(stats, f, indent=2, ensure_ascii=False)
            
            log("统计数据已更新")
            
        except KeyboardInterrupt:
            log("监控被用户中断")
            break
        except Exception as e:
            log(f"收集统计失败：{e}")
        
        time.sleep(30)

if __name__ == "__main__":
    main()
