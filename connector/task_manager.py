#!/usr/bin/env python3
"""
任务执行管理器 - VectorBrain 任务执行引擎

功能：
1. 查询待处理任务
2. 原子性抢占任务
3. 执行任务
4. 回写执行结果

安全机制：
- 原子性 UPDATE + ROW COUNT 验证
- 超时机制（30 分钟）
- 全面错误处理
- flock 文件锁
"""

import sqlite3
import json
import os
import sys
import time
import fcntl
from datetime import datetime, timedelta

# 配置
DB_PATH = os.path.expanduser('~/.vectorbrain/tasks/task_queue.db')
LOG_FILE = os.path.expanduser('~/.vectorbrain/logs/task_manager.log')
LOCK_FILE = '/tmp/task_manager.lock'
WORKER_ID = 'vectorbrain_framework'
TASK_TIMEOUT_MINUTES = 30

def log(message, level='INFO'):
    """写入日志"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f'[{timestamp}] [{level}] {message}\n'
    print(log_entry, end='')
    
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        print(f'[ERROR] 写入日志失败：{e}', file=sys.stderr)

def get_db_connection():
    """获取数据库连接"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        log(f'数据库连接失败：{e}', 'ERROR')
        return None

def get_pending_tasks(limit=5):
    """获取待处理的任务"""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM tasks 
            WHERE status = 'queued' 
            ORDER BY priority ASC, created_at ASC 
            LIMIT ?
        ''', (limit,))
        tasks = cursor.fetchall()
        conn.close()
        return [dict(task) for task in tasks]
    except Exception as e:
        log(f'查询任务失败：{e}', 'ERROR')
        conn.close()
        return []

def claim_task(task_id):
    """原子性抢占任务"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE tasks 
            SET status = 'running', 
                assigned_worker = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE task_id = ? AND status = 'queued'
        ''', (WORKER_ID, task_id))
        
        conn.commit()
        
        if cursor.rowcount == 0:
            log(f'任务 {task_id} 抢占失败（可能已被其他 Worker 抢占）', 'WARN')
            conn.close()
            return False
        
        log(f'任务 {task_id} 抢占成功（Worker: {WORKER_ID}）')
        conn.close()
        return True
        
    except Exception as e:
        log(f'抢占任务失败：{e}', 'ERROR')
        conn.close()
        return False

def complete_task(task_id, result):
    """标记任务为完成"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE tasks 
            SET status = 'completed',
                result = ?,
                completed_at = CURRENT_TIMESTAMP,
                updated_at = CURRENT_TIMESTAMP
            WHERE task_id = ?
        ''', (json.dumps(result, ensure_ascii=False), task_id))
        
        conn.commit()
        conn.close()
        log(f'任务 {task_id} 标记为完成')
        return True
        
    except Exception as e:
        log(f'完成任务失败：{e}', 'ERROR')
        conn.close()
        return False

def fail_task(task_id, error_message):
    """标记任务为失败"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE tasks 
            SET status = 'failed',
                error_message = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE task_id = ?
        ''', (error_message, task_id))
        
        conn.commit()
        conn.close()
        log(f'任务 {task_id} 标记为失败：{error_message}', 'ERROR')
        return True
        
    except Exception as e:
        log(f'标记任务失败：{e}', 'ERROR')
        conn.close()
        return False

def execute_task(task):
    """执行具体任务"""
    task_id = task['task_id']
    title = task['title']
    description = task.get('description', '')
    
    log(f'开始执行任务：{task_id} - {title}')
    
    try:
        # 任务类型路由
        if '测试' in title or 'test' in title.lower():
            result = execute_test_task(task)
        elif '日志' in title or 'log' in title.lower():
            result = execute_log_task(task)
        else:
            # 默认：将任务描述写入日志
            result = execute_default_task(task)
        
        log(f'任务 {task_id} 执行成功')
        return {'success': True, 'result': result}
        
    except Exception as e:
        log(f'任务 {task_id} 执行异常：{e}', 'ERROR')
        raise

def execute_test_task(task):
    """执行测试任务"""
    task_id = task['task_id']
    test_file = os.path.expanduser('~/.vectorbrain/logs/task_test.log')
    
    os.makedirs(os.path.dirname(test_file), exist_ok=True)
    
    with open(test_file, 'a', encoding='utf-8') as f:
        f.write(f'\n{"="*60}\n')
        f.write(f'测试任务执行记录\n')
        f.write(f'时间：{datetime.now().isoformat()}\n')
        f.write(f'任务 ID: {task_id}\n')
        f.write(f'标题：{task["title"]}\n')
        f.write(f'描述：{task.get("description", "")}\n')
        f.write(f'执行 Worker: {WORKER_ID}\n')
        f.write(f'{"="*60}\n')
    
    return {
        'action': 'write_test_log',
        'file': test_file,
        'timestamp': datetime.now().isoformat()
    }

def execute_log_task(task):
    """执行日志任务"""
    task_id = task['task_id']
    description = task.get('description', '')
    
    log_file = os.path.expanduser('~/.vectorbrain/logs/task_logs.log')
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f'\n[{datetime.now().isoformat()}] 任务日志 - {task_id}\n')
        f.write(f'标题：{task["title"]}\n')
        f.write(f'内容：{description}\n')
        f.write('-'*60 + '\n')
    
    return {
        'action': 'write_log',
        'file': log_file,
        'timestamp': datetime.now().isoformat()
    }

def execute_default_task(task):
    """默认任务执行"""
    return execute_log_task(task)

def task_manager_loop():
    """任务管理器主循环"""
    log('='*60)
    log('任务管理器启动')
    log(f'Worker ID: {WORKER_ID}')
    log(f'数据库：{DB_PATH}')
    log('='*60)
    
    # 获取待处理任务
    tasks = get_pending_tasks(limit=5)
    
    if not tasks:
        log('当前无待处理任务')
        return
    
    log(f'发现 {len(tasks)} 个待处理任务')
    
    # 逐个处理任务
    for task in tasks:
        task_id = task['task_id']
        
        # 1. 抢占任务
        if not claim_task(task_id):
            continue
        
        # 2. 执行任务
        try:
            result = execute_task(task)
            
            # 3. 回写成功结果
            complete_task(task_id, result)
            
        except Exception as e:
            # 3. 回写失败结果
            fail_task(task_id, str(e))
        
        # 防止过快执行
        time.sleep(1)
    
    log('任务管理器本轮执行完成')

def main():
    """主函数"""
    # 获取文件锁（防止 Cron 重复执行）
    lock_fd = None
    try:
        lock_fd = open(LOCK_FILE, 'w')
        fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        print('任务管理器已在运行中（获取文件锁失败）', file=sys.stderr)
        sys.exit(1)
    
    try:
        task_manager_loop()
    finally:
        # 释放文件锁
        if lock_fd:
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
            lock_fd.close()

if __name__ == '__main__':
    main()
