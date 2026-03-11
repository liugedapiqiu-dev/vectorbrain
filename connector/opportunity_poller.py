#!/usr/bin/env python3
"""
机会扫描器 - 发现系统中的机会和风险

功能：
1. 轮询 opportunities 数据库
2. 查找高优先级未处理机会
3. 发送通知
4. 更新状态为已处理
"""

import sqlite3
import json
import os
import time
from pathlib import Path
from datetime import datetime

# 配置
DB_PATH = Path.home() / '.vectorbrain' / 'opportunity' / 'opportunities.db'
NOTIFY_LOG = Path.home() / '.vectorbrain' / 'state' / 'pending_notifications.json'
LOG_FILE = Path.home() / '.vectorbrain' / 'logs' / 'opportunity_poller.log'

def log(message):
    """记录日志"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_msg = f'[{timestamp}] {message}'
    print(log_msg)
    
    try:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_msg + '\n')
    except Exception as e:
        print(f'写入日志失败：{e}')

def get_pending_opportunities(limit=5):
    """获取所有高优先级的待处理机会"""
    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT opportunity_id, type, title, description, suggested_action, severity
            FROM opportunities 
            WHERE status = 'pending' AND severity = 'high'
            ORDER BY detected_at DESC 
            LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                'opportunity_id': row[0],
                'type': row[1],
                'title': row[2],
                'description': row[3],
                'suggested_action': row[4],
                'severity': row[5]
            }
            for row in results
        ]
    except Exception as e:
        log(f'❌ 读取数据库失败：{e}')
        return []

def mark_as_notified(opp_id):
    """将机会状态更新为已通知"""
    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE opportunities 
            SET status = 'notified', addressed_at = ?
            WHERE opportunity_id = ?
        ''', (datetime.now().isoformat(), opp_id))
        
        conn.commit()
        conn.close()
        
        log(f'✅ 已更新状态：{opp_id}')
        return True
    except Exception as e:
        log(f'❌ 更新状态失败：{e}')
        return False

def send_feishu_alert(title, description, suggested_action):
    """发送飞书消息警报"""
    msg_content = f'''🚨 发现系统风险/机会

📌 标题：{title}
📄 描述：{description}
💡 建议：{suggested_action}

此消息由 VectorBrain Opportunity Poller 自动生成'''
    
    try:
        # 写入通知日志文件（供其他系统读取发送）
        notifications = []
        if NOTIFY_LOG.exists():
            with open(NOTIFY_LOG, 'r', encoding='utf-8') as f:
                notifications = json.load(f)
        
        # 添加新通知
        notifications.append({
            'timestamp': datetime.now().isoformat(),
            'type': 'risk_alert',
            'title': title,
            'description': description,
            'suggested_action': suggested_action,
            'message': msg_content
        })
        
        # 写回文件
        NOTIFY_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(NOTIFY_LOG, 'w', encoding='utf-8') as f:
            json.dump(notifications, f, ensure_ascii=False, indent=2)
        
        log(f'✅ 通知已写入日志：{NOTIFY_LOG}')
        return True
        
    except Exception as e:
        log(f'❌ 写入通知失败：{e}')
        return False

def radar_sweep():
    """雷达扫描主函数"""
    log('📡 [雷达扫描] 开始检测高优未处理机会...')
    
    opportunities = get_pending_opportunities(limit=5)
    
    if not opportunities:
        log('✅ 当前无高危警报。')
        return
    
    log(f'⚠️ 发现 {len(opportunities)} 个高危事项，准备通知！')
    
    for opp in opportunities:
        opp_id = opp['opportunity_id']
        title = opp['title']
        desc = opp['description']
        action = opp['suggested_action']
        
        # 1. 发送警报
        success = send_feishu_alert(title, desc, action)
        
        # 2. 如果发送成功，更新状态
        if success:
            mark_as_notified(opp_id)
            log(f'🔔 已通知并标记：{opp_id} ({title})')
        else:
            log(f'⛔ 通知失败，保留 pending 状态：{opp_id}')
        
        # 防止频率过高
        time.sleep(1)

if __name__ == '__main__':
    radar_sweep()
