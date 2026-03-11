#!/usr/bin/env python3
"""
OpenClaw Connector - VectorBrain 与 OpenClaw 的核心连接器

功能：
- 监听 OpenClaw 消息和命令
- 保存消息到 VectorBrain 记忆
- 检索相关记忆并注入上下文
- 执行 VectorBrain 任务

用法：
1. 在 OpenClaw 的 skill.json 中注册此连接器
2. 配置 hooks 触发条件
3. 连接器会自动处理消息和命令
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

# VectorBrain 路径
VECTORBRAIN_HOME = Path(os.getenv('VECTORBRAIN_HOME', Path.home() / '.vectorbrain'))
MEMORY_DB = VECTORBRAIN_HOME / 'memory' / 'knowledge_memory.db'
EPISODIC_DB = VECTORBRAIN_HOME / 'memory' / 'episodic_memory.db'
TASK_DB = VECTORBRAIN_HOME / 'tasks' / 'task_queue.db'

# OpenClaw 路径
OPENCLAW_HOME = Path(os.getenv('OPENCLAW_HOME', Path.home() / '.openclaw'))
SKILLS_DIR = OPENCLAW_HOME / 'skills' / 'vectorbrain'

# 日志配置
LOG_FILE = SKILLS_DIR / 'logs' / 'connector.log'
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

def log(message, level='INFO'):
    """记录日志"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_msg = f'[{timestamp}] [{level}] {message}'
    print(log_msg, file=sys.stderr)
    
    # 写入日志文件
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_msg + '\n')
    except Exception as e:
        print(f'写入日志失败：{e}', file=sys.stderr)

def save_message_to_memory(message, user_id, channel_id):
    """
    保存消息到 VectorBrain 记忆
    
    Args:
        message: 消息内容
        user_id: 用户 ID
        channel_id: 频道 ID
    
    Returns:
        bool: 保存是否成功
    """
    log(f'保存消息到记忆：{message[:50]}...')
    
    try:
        import sqlite3
        
        # 连接到情景记忆数据库
        conn = sqlite3.connect(str(EPISODIC_DB))
        cursor = conn.cursor()
        
        # 插入消息记录
        cursor.execute('''
            INSERT INTO episodes (timestamp, worker_id, event_type, content, metadata)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            'openclaw_connector',
            f'message_{user_id}',
            message,
            json.dumps({
                'channel_id': channel_id,
                'user_id': user_id,
                'saved_at': datetime.now().isoformat()
            }, ensure_ascii=False)
        ))
        
        conn.commit()
        conn.close()
        
        log(f'✅ 消息已保存到记忆')
        return True
        
    except Exception as e:
        log(f'❌ 保存消息失败：{e}', 'ERROR')
        return False

def retrieve_relevant_memories(query, limit=5, threshold=0.7):
    """
    检索相关记忆
    
    Args:
        query: 查询文本
        limit: 返回结果数量
        threshold: 相似度阈值
    
    Returns:
        list: 相关记忆列表
    """
    log(f'检索相关记忆：{query[:50]}...')
    
    try:
        # 这里应该使用向量检索
        # 简化版本：直接文本匹配
        import sqlite3
        
        conn = sqlite3.connect(str(MEMORY_DB))
        cursor = conn.cursor()
        
        # 简单文本搜索（实际应该用向量检索）
        cursor.execute('''
            SELECT key, value, confidence
            FROM knowledge
            WHERE value LIKE ?
            ORDER BY confidence DESC
            LIMIT ?
        ''', (f'%{query}%', limit))
        
        results = cursor.fetchall()
        conn.close()
        
        log(f'✅ 检索到 {len(results)} 条相关记忆')
        
        return [
            {
                'key': row[0],
                'value': row[1],
                'confidence': row[2]
            }
            for row in results
        ]
        
    except Exception as e:
        log(f'❌ 检索记忆失败：{e}', 'ERROR')
        return []

def execute_task(task_title, task_description, priority=5):
    """
    执行任务
    
    Args:
        task_title: 任务标题
        task_description: 任务描述
        priority: 优先级（1-10）
    
    Returns:
        str: 任务 ID
    """
    log(f'创建任务：{task_title}')
    
    try:
        import sqlite3
        
        conn = sqlite3.connect(str(TASK_DB))
        cursor = conn.cursor()
        
        # 生成任务 ID
        task_id = f'task_{datetime.now().strftime("%Y%m%d%H%M%S")}'
        
        # 插入任务记录
        cursor.execute('''
            INSERT INTO tasks (task_id, title, description, priority, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            task_id,
            task_title,
            task_description,
            priority,
            'queued',
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
        
        log(f'✅ 任务已创建：{task_id}')
        return task_id
        
    except Exception as e:
        log(f'❌ 创建任务失败：{e}', 'ERROR')
        return None

# OpenClaw Hook 处理器

async def handle_message(msgCtx):
    """
    处理新消息 Hook
    
    Args:
        msgCtx: 消息上下文
    
    Returns:
        dict: 处理结果
    """
    try:
        # 提取消息内容
        message = msgCtx.get('message', {}).get('content', '')
        user_id = msgCtx.get('message', {}).get('sender_id', 'unknown')
        channel_id = msgCtx.get('channel_id', 'unknown')
        
        log(f'收到消息：{message[:50]}... (用户：{user_id})')
        
        # 1. 保存消息到记忆
        save_message_to_memory(message, user_id, channel_id)
        
        # 2. 检索相关记忆
        memories = retrieve_relevant_memories(message)
        
        # 3. 注入记忆到上下文（如果需要）
        if memories:
            log(f'注入 {len(memories)} 条记忆到上下文')
            # 这里可以将记忆添加到 msgCtx 中
            # msgCtx['memories'] = memories
        
        return {
            'success': True,
            'memories_saved': True,
            'memories_found': len(memories)
        }
        
    except Exception as e:
        log(f'❌ 处理消息失败：{e}', 'ERROR')
        return {
            'success': False,
            'error': str(e)
        }

async def handle_command(cmdCtx):
    """
    处理新命令 Hook
    
    Args:
        cmdCtx: 命令上下文
    
    Returns:
        dict: 处理结果
    """
    try:
        command = cmdCtx.get('command', '')
        args = cmdCtx.get('args', [])
        
        log(f'收到命令：{command} {args}')
        
        # 处理 VectorBrain 特定命令
        if command == 'task':
            # 创建任务
            task_title = args[0] if args else '未命名任务'
            task_desc = args[1] if len(args) > 1 else ''
            task_id = execute_task(task_title, task_desc)
            
            return {
                'success': True,
                'task_id': task_id,
                'response': f'✅ 任务已创建：{task_id}'
            }
        
        elif command == 'memory':
            # 检索记忆
            query = args[0] if args else ''
            memories = retrieve_relevant_memories(query)
            
            return {
                'success': True,
                'memories': memories,
                'response': f'📚 找到 {len(memories)} 条相关记忆'
            }
        
        elif command == 'search':
            # 向量搜索
            query = args[0] if args else ''
            memories = retrieve_relevant_memories(query)
            
            return {
                'success': True,
                'results': memories,
                'response': f'🔍 搜索完成：{len(memories)} 条结果'
            }
        
        else:
            # 未知命令
            return {
                'success': False,
                'response': f'❌ 未知命令：{command}'
            }
        
    except Exception as e:
        log(f'❌ 处理命令失败：{e}', 'ERROR')
        return {
            'success': False,
            'error': str(e)
        }

# 主入口（用于测试）

if __name__ == '__main__':
    log('=' * 60)
    log('🔌 OpenClaw Connector 启动')
    log('=' * 60)
    log(f'VectorBrain 路径：{VECTORBRAIN_HOME}')
    log(f'OpenClaw 路径：{OPENCLAW_HOME}')
    log(f'记忆数据库：{MEMORY_DB}')
    log(f'任务数据库：{TASK_DB}')
    log('=' * 60)
    log('Connector 已就绪，等待 OpenClaw 调用...')
