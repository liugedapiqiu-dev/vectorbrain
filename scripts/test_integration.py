#!/usr/bin/env python3
"""
集成测试脚本 - 测试 VectorBrain 是否正常工作

功能：
- 测试数据库连接
- 测试记忆保存
- 测试记忆检索
- 测试任务创建
- 测试 OpenClaw 集成

用法：
python scripts/test_integration.py
"""

import sqlite3
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

# 测试结果
test_results = {
    'passed': 0,
    'failed': 0,
    'tests': []
}

def log(message):
    """打印日志"""
    print(f'\033[94m[{datetime.now().strftime("%H:%M:%S")}]\033[0m {message}')

def test_passed(name):
    """记录测试通过"""
    test_results['passed'] += 1
    test_results['tests'].append({'name': name, 'status': 'passed'})
    log(f'✅ {name}')

def test_failed(name, error):
    """记录测试失败"""
    test_results['failed'] += 1
    test_results['tests'].append({'name': name, 'status': 'failed', 'error': str(error)})
    log(f'❌ {name}: {error}')

def test_database_connection():
    """测试数据库连接"""
    log('')
    log('=' * 60)
    log('测试 1: 数据库连接')
    log('=' * 60)
    
    try:
        # 测试知识记忆数据库
        conn = sqlite3.connect(str(MEMORY_DB))
        cursor = conn.cursor()
        cursor.execute('SELECT 1')
        conn.close()
        test_passed('知识记忆数据库连接')
    except Exception as e:
        test_failed('知识记忆数据库连接', e)
    
    try:
        # 测试情景记忆数据库
        conn = sqlite3.connect(str(EPISODIC_DB))
        cursor = conn.cursor()
        cursor.execute('SELECT 1')
        conn.close()
        test_passed('情景记忆数据库连接')
    except Exception as e:
        test_failed('情景记忆数据库连接', e)
    
    try:
        # 测试任务数据库
        conn = sqlite3.connect(str(TASK_DB))
        cursor = conn.cursor()
        cursor.execute('SELECT 1')
        conn.close()
        test_passed('任务数据库连接')
    except Exception as e:
        test_failed('任务数据库连接', e)

def test_memory_save():
    """测试记忆保存"""
    log('')
    log('=' * 60)
    log('测试 2: 记忆保存')
    log('=' * 60)
    
    try:
        conn = sqlite3.connect(str(MEMORY_DB))
        cursor = conn.cursor()
        
        # 插入测试数据
        test_key = f'test_{datetime.now().strftime("%Y%m%d%H%M%S")}'
        test_value = '这是一条测试记忆'
        
        cursor.execute('''
            INSERT OR REPLACE INTO knowledge (category, key, value, source_worker, confidence)
            VALUES (?, ?, ?, ?, ?)
        ''', ('test', test_key, test_value, 'test_script', 1.0))
        
        conn.commit()
        conn.close()
        
        test_passed('保存测试记忆')
        
    except Exception as e:
        test_failed('保存测试记忆', e)

def test_memory_retrieve():
    """测试记忆检索"""
    log('')
    log('=' * 60)
    log('测试 3: 记忆检索')
    log('=' * 60)
    
    try:
        conn = sqlite3.connect(str(MEMORY_DB))
        cursor = conn.cursor()
        
        # 检索测试数据
        cursor.execute('''
            SELECT key, value FROM knowledge WHERE category = 'test' ORDER BY created_at DESC LIMIT 1
        ''')
        
        result = cursor.fetchone()
        conn.close()
        
        if result and '测试' in result[1]:
            test_passed('检索测试记忆')
        else:
            test_failed('检索测试记忆', '未找到测试记忆')
        
    except Exception as e:
        test_failed('检索测试记忆', e)

def test_task_create():
    """测试任务创建"""
    log('')
    log('=' * 60)
    log('测试 4: 任务创建')
    log('=' * 60)
    
    try:
        conn = sqlite3.connect(str(TASK_DB))
        cursor = conn.cursor()
        
        # 插入测试任务
        task_id = f'test_{datetime.now().strftime("%Y%m%d%H%M%S")}'
        
        cursor.execute('''
            INSERT INTO tasks (task_id, title, description, priority, status, created_by)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (task_id, '测试任务', '这是一个测试任务', 5, 'queued', 'test_script'))
        
        conn.commit()
        conn.close()
        
        test_passed('创建测试任务')
        
    except Exception as e:
        test_failed('创建测试任务', e)

def test_openclaw_integration():
    """测试 OpenClaw 集成"""
    log('')
    log('=' * 60)
    log('测试 5: OpenClaw 集成')
    log('=' * 60)
    
    # 检查 OpenClaw 路径
    openclaw_home = Path.home() / '.openclaw'
    
    if openclaw_home.exists():
        test_passed('OpenClaw 安装目录存在')
    else:
        test_failed('OpenClaw 安装目录存在', '未找到 OpenClaw 安装目录')
        return
    
    # 检查技能目录
    skills_dir = openclaw_home / 'skills'
    
    if skills_dir.exists():
        test_passed('OpenClaw 技能目录存在')
    else:
        test_failed('OpenClaw 技能目录存在', '未找到技能目录')
    
    # 检查 VectorBrain 技能
    vectorbrain_skill = skills_dir / 'vectorbrain'
    
    if vectorbrain_skill.exists():
        test_passed('VectorBrain 技能已安装')
    else:
        test_failed('VectorBrain 技能已安装', 'VectorBrain 技能未安装')
        log('提示：运行以下命令安装技能:')
        log('  cp -r * ~/.openclaw/skills/vectorbrain/')
        log('  cd ~/.openclaw/skills/vectorbrain')
        log('  openclaw skills enable vectorbrain')

def print_summary():
    """打印测试摘要"""
    log('')
    log('=' * 60)
    log('📊 测试摘要')
    log('=' * 60)
    log(f'总测试数：{test_results["passed"] + test_results["failed"]}')
    log(f'✅ 通过：{test_results["passed"]}')
    log(f'❌ 失败：{test_results["failed"]}')
    log('')
    
    if test_results['failed'] > 0:
        log('失败的测试:')
        for test in test_results['tests']:
            if test['status'] == 'failed':
                log(f'  ❌ {test["name"]}: {test.get("error", "未知错误")}')
        log('')
        log('⚠️  部分测试失败，请检查错误信息并修复')
        log('=' * 60)
        return 1
    else:
        log('🎉 所有测试通过！')
        log('')
        log('下一步:')
        log('1. 配置 config/config.json')
        log('2. 配置 skill.json')
        log('3. 重启 OpenClaw: openclaw gateway restart')
        log('4. 测试消息处理：发送一条消息')
        log('=' * 60)
        return 0

def main():
    """主函数"""
    log('')
    log('=' * 60)
    log('🧪 VectorBrain 集成测试')
    log('=' * 60)
    log(f'VectorBrain 路径：{VECTORBRAIN_HOME}')
    log(f'时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    log('=' * 60)
    
    # 运行所有测试
    test_database_connection()
    test_memory_save()
    test_memory_retrieve()
    test_task_create()
    test_openclaw_integration()
    
    # 打印摘要
    return print_summary()

if __name__ == '__main__':
    sys.exit(main())
