#!/usr/bin/env python3
"""
VectorBrain 数据库初始化脚本

功能：
- 创建所有必需的数据库表
- 插入初始数据
- 验证数据库连接
- 检查权限

用法：
python scripts/init_databases.py
"""

import sqlite3
import os
import sys
from pathlib import Path
from datetime import datetime

# VectorBrain 路径
VECTORBRAIN_HOME = Path(os.getenv('VECTORBRAIN_HOME', Path.home() / '.vectorbrain'))

# 数据库路径
MEMORY_DIR = VECTORBRAIN_HOME / 'memory'
TASKS_DIR = VECTORBRAIN_HOME / 'tasks'
OPPORTUNITY_DIR = VECTORBRAIN_HOME / 'opportunity'
REFLECTION_DIR = VECTORBRAIN_HOME / 'reflection'
LOGS_DIR = VECTORBRAIN_HOME / 'logs'

# 确保目录存在
for dir_path in [MEMORY_DIR, TASKS_DIR, OPPORTUNITY_DIR, REFLECTION_DIR, LOGS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

def log(message):
    """打印日志"""
    print(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {message}')

def init_episodic_memory():
    """初始化情景记忆数据库"""
    db_path = MEMORY_DIR / 'episodic_memory.db'
    log(f'初始化情景记忆数据库：{db_path}')
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS episodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            worker_id TEXT NOT NULL,
            event_type TEXT NOT NULL,
            content TEXT NOT NULL,
            metadata TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 创建索引
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON episodes(timestamp)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_event_type ON episodes(event_type)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_worker ON episodes(worker_id)')
    
    conn.commit()
    conn.close()
    
    log('✅ 情景记忆数据库初始化完成')

def init_knowledge_memory():
    """初始化知识记忆数据库"""
    db_path = MEMORY_DIR / 'knowledge_memory.db'
    log(f'初始化知识记忆数据库：{db_path}')
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS knowledge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            key TEXT NOT NULL,
            value TEXT NOT NULL,
            source_worker TEXT,
            confidence REAL DEFAULT 1.0,
            embedding_vector TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(category, key)
        )
    ''')
    
    # 创建索引
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_category ON knowledge(category)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_key ON knowledge(key)')
    
    conn.commit()
    conn.close()
    
    log('✅ 知识记忆数据库初始化完成')

def init_tasks():
    """初始化任务数据库"""
    db_path = TASKS_DIR / 'task_queue.db'
    log(f'初始化任务数据库：{db_path}')
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            task_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            priority INTEGER DEFAULT 5,
            status TEXT DEFAULT 'queued',
            assigned_worker TEXT,
            created_by TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            completed_at TEXT,
            result TEXT,
            error_message TEXT
        )
    ''')
    
    # 创建索引
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_status ON tasks(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_priority ON tasks(priority)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_worker ON tasks(assigned_worker)')
    
    # 插入示例任务
    cursor.execute('''
        INSERT OR IGNORE INTO tasks (task_id, title, description, priority, status, created_by)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        'welcome_task',
        '欢迎任务',
        '恭喜你成功安装 VectorBrain 框架！这是一个示例任务。',
        1,
        'queued',
        'system'
    ))
    
    conn.commit()
    conn.close()
    
    log('✅ 任务数据库初始化完成')

def init_opportunities():
    """初始化机会数据库"""
    db_path = OPPORTUNITY_DIR / 'opportunities.db'
    log(f'初始化机会数据库：{db_path}')
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS opportunities (
            opportunity_id TEXT PRIMARY KEY,
            type TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            severity TEXT DEFAULT 'medium',
            suggested_action TEXT,
            status TEXT DEFAULT 'pending',
            detected_at TEXT DEFAULT CURRENT_TIMESTAMP,
            addressed_at TEXT
        )
    ''')
    
    # 创建索引
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_status ON opportunities(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_severity ON opportunities(severity)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_type ON opportunities(type)')
    
    conn.commit()
    conn.close()
    
    log('✅ 机会数据库初始化完成')

def init_reflections():
    """初始化反思数据库"""
    db_path = REFLECTION_DIR / 'reflections.db'
    log(f'初始化反思数据库：{db_path}')
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reflections (
            reflection_id TEXT PRIMARY KEY,
            task_id TEXT,
            goal_id TEXT,
            outcome TEXT NOT NULL,
            success BOOLEAN NOT NULL,
            analysis TEXT,
            lessons_learned TEXT,
            action_items TEXT,
            created_by TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 创建索引
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_task ON reflections(task_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_outcome ON reflections(outcome)')
    
    conn.commit()
    conn.close()
    
    log('✅ 反思数据库初始化完成')

def verify_databases():
    """验证所有数据库"""
    log('验证数据库连接...')
    
    databases = [
        MEMORY_DIR / 'episodic_memory.db',
        MEMORY_DIR / 'knowledge_memory.db',
        TASKS_DIR / 'task_queue.db',
        OPPORTUNITY_DIR / 'opportunities.db',
        REFLECTION_DIR / 'reflections.db'
    ]
    
    for db_path in databases:
        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            cursor.execute('SELECT 1')
            conn.close()
            log(f'✅ {db_path.name} - 连接正常')
        except Exception as e:
            log(f'❌ {db_path.name} - 连接失败：{e}')
            return False
    
    log('✅ 所有数据库验证通过')
    return True

def main():
    """主函数"""
    log('=' * 60)
    log('🗄️ VectorBrain 数据库初始化')
    log('=' * 60)
    log(f'VectorBrain 路径：{VECTORBRAIN_HOME}')
    log('=' * 60)
    
    # 初始化所有数据库
    init_episodic_memory()
    init_knowledge_memory()
    init_tasks()
    init_opportunities()
    init_reflections()
    
    # 验证数据库
    log('')
    if verify_databases():
        log('')
        log('=' * 60)
        log('🎉 数据库初始化完成！')
        log('=' * 60)
        log('')
        log('下一步:')
        log('1. 配置 config/config.json')
        log('2. 配置 skill.json')
        log('3. 运行：python scripts/test_integration.py')
        log('=' * 60)
        return 0
    else:
        log('')
        log('❌ 数据库验证失败，请检查错误信息')
        log('=' * 60)
        return 1

if __name__ == '__main__':
    sys.exit(main())
