import pandas as pd
import random
from datetime import datetime, timedelta

# 生成随机姓名
def generate_name():
    first_names = ['张', '李', '王', '刘', '陈', '杨', '黄', '吴', '赵', '周']
    last_names = ['伟', '芳', '娜', '敏', '静', '丽', '强', '磊', '军', '洋']
    return random.choice(first_names) + random.choice(last_names)

# 生成随机性别
def generate_gender():
    return random.choice(['男', '女'])

# 生成随机年龄
def generate_age():
    return random.randint(18, 60)

# 生成随机注册时间
def generate_registration_time():
    start_date = datetime(2015, 1, 1)
    end_date = datetime(2022, 12, 31)
    return start_date + (end_date - start_date) * random.random()

# 生成随机地域
def generate_region():
    regions = ['北京', '上海', '广东', '江苏', '浙江', '山东', '河南', '四川', '湖北', '湖南']
    return random.choice(regions)

# 生成随机用户信息表
def generate_user_data(num_users):
    data = {
        '用户ID': [i for i in range(1, num_users + 1)],
        '姓名': [generate_name() for _ in range(num_users)],
        '性别': [generate_gender() for _ in range(num_users)],
        '年龄': [generate_age() for _ in range(num_users)],
        '注册时间': [generate_registration_time().strftime('%Y-%m-%d %H:%M:%S') for _ in range(num_users)],
        '地域': [generate_region() for _ in range(num_users)],
        '邮箱': [f'user{i}@example.com' for i in range(1, num_users + 1)],
        '手机号': [f'138{random.randint(10000000, 99999999)}' for _ in range(num_users)],
        '会员等级': [random.choice(['普通会员', '银卡会员', '金卡会员', '钻石会员']) for _ in range(num_users)],
        '积分': [random.randint(0, 10000) for _ in range(num_users)],
        '最近登录时间': [generate_registration_time().strftime('%Y-%m-%d %H:%M:%S') for _ in range(num_users)]
    }
    return pd.DataFrame(data)

# 生成100个用户信息示例数据
num_users = 100
user_data = generate_user_data(num_users)

# 导出到excel文件
file_path = '/Users/harmnet/Desktop/用户信息表.xlsx'  # 请将"你的用户名"替换为你的实际用户名
user_data.to_excel(file_path, index=False)

print(f"数据已成功导出到 {file_path}")

