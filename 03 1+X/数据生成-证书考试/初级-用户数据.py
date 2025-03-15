import csv
import random
from datetime import datetime
import math

import pandas as pd

# 自定义姓名组件（确保性别关联）
surnames = ['王','李','张','刘','陈','杨','赵','黄','周','吴','徐','孙','马','朱','胡','郭','何','高','林','郑']
male_names = ['伟','强','磊','军','勇','杰','涛','明','超','斌','浩','鹏','宇','飞','鑫','波','亮','刚','平','辉']
female_names = ['芳','娜','敏','静','丽','娟','艳','玲','婷','雪','慧','莹','倩','雅','洁','琳','燕','梅','欣','雨']

# 预定义选项列表
cities = {
    '一线': ['北京', '上海', '广州', '深圳'],
    '其他': ['成都', '杭州', '武汉', '南京', '重庆', '西安', '苏州', '郑州', '长沙']
}
occupations = ['公务员', '教师', '企业员工', '自由职业者', '学生']
card_levels = ['普卡', '金卡', '白金卡', '钻石卡']
channels = ['短信', '小程序', '公众号', '官网', 'APP']
preferences = ['旅游', '购物', '餐饮', '娱乐', '其他']

def generate_gender_specific_name(gender):
    """生成符合性别特征的姓名（姓氏单字+名字1-2字）"""
    surname = random.choice(surnames)
    name_pool = male_names if gender == '男' else female_names
    name_length = random.choices([1,2], weights=[40,60])[0]
    return surname + ''.join(random.sample(name_pool, name_length))

def calculate_credit_score(card_level, overdue):
    """计算信用评分（精确到个位）"""
    base_scores = {
        '普卡': random.randint(600, 699),
        '金卡': random.randint(650, 749),
        '白金卡': random.randint(700, 800),
        '钻石卡': random.randint(720, 850)
    }
    score = base_scores.get(card_level, 650)
    penalty = overdue * random.randint(50, 100)
    final_score = max(300, score - penalty)
    
    # 强制白金/钻石卡最低700分
    if card_level in ['白金卡', '钻石卡']:
        return max(700, final_score)
    return final_score

def generate_user_data(num_records):
    data = []
    existing_names = set()
    referrers = []  # 推荐人记录列表
    
    for i in range(201, 201 + num_records):
        user = {'用户ID': i}
        
        # 生成性别和唯一姓名
        gender = random.choice(['男', '女'])
        while True:
            name = generate_gender_specific_name(gender)
            if name not in existing_names:
                existing_names.add(name)
                break
        user['性别'] = gender
        user['姓名'] = name
        
        # 手机号（符合中国运营商号段）
        prefix = random.choice(['13', '15', '17', '18', '19'])
        mid = ''.join(str(random.randint(0,9)) for _ in range(9))
        user['手机号码'] = f"{prefix}****{mid[-4:]}"
        
        # 年龄和生日（精确到日）
        age = random.randint(18, 70)
        birth_year = datetime.now().year - age
        birth_date = datetime(birth_year, random.randint(1,12), random.randint(1,28)).strftime('%Y-%m-%d 00:00:00')
        user['用户年龄'] = age
        user['生日'] = birth_date
        
        # 渠道选择
        user['渠道'] = random.choice(channels)
        
        # 信用卡逻辑
        has_card = random.choices(['是','否'], weights=[65,35])[0]
        user['是否持有信用卡'] = has_card
        
        if has_card == '是':
            # 生成符合要求的信用卡号
            card_number = 'CGB' + ''.join(str(random.randint(0,9)) for _ in range(random.randint(15,20)))
            user['信用卡号'] = card_number
            
            credit_limit = random.choice(range(1000, 100001, 1000))
            user['总额度'] = credit_limit
            
            used = round(random.uniform(100, credit_limit-100), 1)
            user['已用额度'] = used
            user['余额'] = round(credit_limit - used, 1)
            
            # 分期逻辑
            installment = '是' if used > 0 and random.random() < 0.4 else '否'
            user['是否分期'] = installment
            
            # 信用卡级别（带权重）
            level = random.choices(card_levels, weights=[35,30,20,15])[0]
            user['信用卡级别'] = level
        else:
            for field in ['信用卡号', '已用额度', '余额', '总额度', '信用卡级别']:
                user[field] = '无' if field == '信用卡号' else 0
        
        # 是否有房和是否有车
        user['是否有房'] = random.choices(['有', '无'], weights=[40, 60])[0]
        user['是否有车'] = random.choices(['有', '无'], weights=[30, 70])[0]
        
        # 经济状况
        user['月收入'] = random.randint(500, 50000)
        user['贷款金额'] = random.choices([0, random.randint(5000, 1000000)], weights=[40,60])[0]
        
        # 资产生成（考虑房产价值）
        house_value = random.randint(0, 5000000) if user['是否有房'] == '有' else 0
        car_value = random.randint(0, 1000000) if user['是否有车'] == '有' else 0
        user['资产总额'] = random.randint(house_value + car_value, 10000000)
        
        # 消费限制
        max_consumption = min(
            user['月收入'] * 12,
            math.floor(user['资产总额'] * 0.1)
        )
        user['年消费总额'] = random.randint(0, min(500000, max_consumption))
        
        # 信用评分（带逾期惩罚）
        overdue = random.choices(
            range(0,6), 
            weights=[70,15,8,4,2,1]
        )[0]
        user['信用卡逾期次数'] = overdue
        user['信用评分'] = calculate_credit_score(user.get('信用卡级别','无'), overdue)
        
        # 活跃度逻辑
        active_conditions = [
            user['贷款金额'] > 500000,
            user['年消费总额'] > 100000,
            overdue == 0
        ]
        active_prob = 0.4 if sum(active_conditions) >=2 else 0.2
        user['活跃度等级'] = random.choices(
            ['高','中','低'], 
            weights=[active_prob, 0.5, 0.5-active_prob]
        )[0]
        
        # 消费偏好（带权重）
        pref_weights = {
            '旅游': 25, '购物':25, '餐饮':20, '娱乐':20, '其他':10
        }
        if user.get('信用卡级别','无') in ['白金卡','钻石卡']:
            pref_weights.update({'旅游':35, '购物':35})
        if user['活跃度等级'] == '高':
            pref_weights['其他'] = 0
        user['消费偏好'] = random.choices(list(pref_weights.keys()), weights=pref_weights.values())[0]
        
        # 城市选择（带概率调整）
        city_type = '一线' if (user['是否有房'] == '有' or user['是否有车'] == '有') else random.choices(['一线','其他'], weights=[35,65])[0]
        user['所在城市'] = random.choice(cities[city_type])
        
        # 职业影响
        user['职业'] = random.choices(occupations, weights=[15,15,40,20,10])[0]
        if user['职业'] == '学生':
            user['贷款金额'] = min(user['贷款金额'], 50000)
            if has_card == '是':
                user['总额度'] = min(user['总额度'], 5000)
        
        # 传播者逻辑（精确25%）
        if random.random() < 0.25 and i > 201:  # 排除第一个用户
            user['传播者ID'] = random.choice(referrers) if referrers else 0
        else:
            user['传播者ID'] = 0
        
        # 推荐好友逻辑
        if user['活跃度等级'] == '高':
            user['推荐好友数量'] = random.choices([2,3,4,5], weights=[30,40,20,10])[0]
            if user['传播者ID'] != 0:
                referrers.append(i)  # 记录活跃推荐人
        
        # 生成3%异常值
        if random.random() < 0.03:
            user['月收入'] = random.randint(500, 2000)
            if has_card == '是':
                user['总额度'] = random.choice([50000, 100000])
                user['信用评分'] = max(700, user['信用评分'])  # 维持高评分异常
        
        # 子女数量生成逻辑
        user['子女数量'] = random.randint(0, 3)
        # 如果是学生，强制子女数量为0
        if user['职业'] == '学生':
            user['子女数量'] = 0
        
        data.append(user)
    
    return data

# 在生成数据后添加以下代码
fieldnames = [
    '用户ID', '性别', '姓名', '手机号码', '用户年龄', '生日', '渠道', '是否持有信用卡', '信用卡号', '已用额度', 
    '余额', '总额度', '信用卡级别', '是否分期', '是否有房', '是否有车', '月收入', '贷款金额', 
    '资产总额', '年消费总额', '信用卡逾期次数', '信用评分', '活跃度等级', '消费偏好', '所在城市', 
    '职业', '推荐好友数量', '传播者ID', '子女数量'
]

# 生成数据并保存到指定路径
desktop_path = '/Users/harmnet/Desktop/用户数据-初级.xlsx'
data = generate_user_data(200)

# 使用pandas保存为Excel文件
df = pd.DataFrame(data)
df.to_excel(desktop_path, index=False, engine='openpyxl')

print(f"数据已生成到：{desktop_path}")
