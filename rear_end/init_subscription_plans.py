#!/usr/bin/env python3
"""
初始化订阅计划数据
"""

import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rear_end.settings')
django.setup()

from users.models import SubscriptionPlan

# 订阅计划数据
plans = [
    {
        'name': '免费版',
        'price': 0.00,
        'monthly_fee': True,
        'daily_chat_limit': 5,
        'max_knowledge_bases': 1
    },
    {
        'name': '基础版',
        'price': 9.90,
        'monthly_fee': True,
        'daily_chat_limit': 50,
        'max_knowledge_bases': 5
    },
    {
        'name': '专业版',
        'price': 29.90,
        'monthly_fee': True,
        'daily_chat_limit': 200,
        'max_knowledge_bases': 20
    }
]

# 批量创建订阅计划
for plan_data in plans:
    plan, created = SubscriptionPlan.objects.get_or_create(
        name=plan_data['name'],
        defaults=plan_data
    )
    if created:
        print(f"创建订阅计划: {plan.name}")
    else:
        print(f"订阅计划已存在: {plan.name}")

print("订阅计划初始化完成!")
