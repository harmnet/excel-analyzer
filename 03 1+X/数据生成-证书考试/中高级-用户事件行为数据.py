import csv
import random
from datetime import datetime, timedelta
import pandas as pd

def generate_behavior_data(user_data_path, num_records):
    # 读取用户数据并过滤有信用卡的用户
    users_df = pd.read_excel(user_data_path)
    valid_users = users_df[users_df['是否持有信用卡'] == '是'].to_dict('records')
    
    # 初始化顺序计数器
    event_counter = 1
    seller_counter = 1
    
    # 事件类型金额范围配置（单位：元）
    event_type_ranges = {
        '餐饮消费': (20, 300),
        '交通出行': (5, 150),
        '电商购物': (100, 2000),
        '线下消费': (50, 1000),
        '大宗消费': (5000, 30000),
        '其他消费': (10, 500)
    }
    
    data = []
    
    # 为每个用户生成1-20条事件
    for user in valid_users:
        num_events = random.randint(1, 20)
        for _ in range(num_events):
            # 生成事件ID
            event_id = f"AC{event_counter:06d}"
            event_counter += 1
            
            # 生成收款方ID
            seller_id = f"SJ{seller_counter:04d}"
            seller_counter = seller_counter + 1 if seller_counter < 9999 else 1
            
            # 随机选择事件类型
            event_type = random.choice(list(event_type_ranges.keys()))
            
            # 计算消费金额（考虑用户信用卡额度）
            min_amount, max_amount = event_type_ranges[event_type]
            max_possible = min(max_amount, user['总额度'] * 0.8)  # 保留20%额度缓冲
            amount = round(random.uniform(min_amount, max_possible), 2)
            
            # 生成时间（2024年6月-7月）
            start_date = datetime(2024, 6, 1)
            end_date = datetime(2024, 7, 31, 23, 59, 59)
            random_seconds = random.randint(0, int((end_date - start_date).total_seconds()))
            event_time = start_date + timedelta(seconds=random_seconds)
            
            data.append({
                '事件ID': event_id,
                '客户ID': user['用户ID'],
                '事件类型': event_type,
                '事件发生时间': event_time.strftime('%Y-%m-%d %H:%M:%S'),
                '消费金额': amount,
                '收款方ID': seller_id
            })
    
    # 如果生成数量不足则补充
    while len(data) < num_records:
        user = random.choice(valid_users)
        num_events = min(random.randint(1, 20), num_records - len(data))
        
        for _ in range(num_events):
            event_id = f"AC{event_counter:06d}"
            event_counter += 1
            
            seller_id = f"SJ{seller_counter:04d}"
            seller_counter = seller_counter + 1 if seller_counter < 9999 else 1
            
            event_type = random.choice(list(event_type_ranges.keys()))
            
            min_amount, max_amount = event_type_ranges[event_type]
            max_possible = min(max_amount, user['总额度'] * 0.8)
            amount = round(random.uniform(min_amount, max_possible), 2)
            
            random_seconds = random.randint(0, int((end_date - start_date).total_seconds()))
            event_time = start_date + timedelta(seconds=random_seconds)
            
            data.append({
                '事件ID': event_id,
                '客户ID': user['用户ID'],
                '事件类型': event_type,
                '事件发生时间': event_time.strftime('%Y-%m-%d %H:%M:%S'),
                '消费金额': amount,
                '收款方ID': seller_id
            })
            
            if len(data) >= num_records:
                break
    
    return data

# 生成数据并保存
desktop_path = '/Users/harmnet/Desktop/用户事件行为数据-中高级.xlsx'
behavior_data = generate_behavior_data('/Users/harmnet/Desktop/用户数据-中高级.xlsx', 2000)

# 使用pandas直接保存为Excel文件
df = pd.DataFrame(behavior_data)
df.to_excel(desktop_path, index=False, engine='openpyxl')

print(f"事件行为数据已生成到：{desktop_path}")
