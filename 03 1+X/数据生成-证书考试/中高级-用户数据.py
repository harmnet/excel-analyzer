import csv
import random
from datetime import datetime
import math

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
    
    if card_level in ['白金卡', '钻石卡']:
        return max(700, final_score)
    return final_score

def generate_channel(age):
    """根据年龄生成渠道偏好"""
    if 18 <= age <= 25:
        # 年轻人更倾向移动端渠道
        return random.choices(['APP', '小程序', '公众号', '官网', '短信'], weights=[30,25,20,15,10])[0]
    elif 26 <= age <= 40:
        # 中年群体渠道分布较均衡
        return random.choices(['APP', '小程序', '公众号', '官网', '短信'], weights=[20,20,20,20,20])[0]
    else:
        # 年长群体更倾向传统渠道
        return random.choices(['短信', '官网', '公众号', '小程序', 'APP'], weights=[35,30,15,10,10])[0]

def generate_rfm_fields(user):
    """生成RFM字段"""
    # 如果没有信用卡，所有相关字段为0
    if user['是否持有信用卡'] == '否':
        user['最近消费间隔'] = 999
        user['年度消费频次'] = 0
        user['单均消费金额'] = 0.0
    else:
        # 最近消费间隔
        if user['年消费总额'] == 0:
            user['最近消费间隔'] = 999
        else:
            if user['活跃度等级'] == '高':
                user['最近消费间隔'] = random.randint(1, 30)
            elif user['活跃度等级'] == '中':
                user['最近消费间隔'] = random.randint(31, 90)
            else:
                user['最近消费间隔'] = random.randint(91, 365)
        
        # 年度消费频次
        base_freq = max(1, user['年消费总额'] // max(1, int(user['月收入'] * 0.2)))
        if user['消费偏好'] in ['旅游', '购物']:
            base_freq += random.randint(1, 3)
        if user['职业'] == '学生':
            base_freq = min(base_freq, 6)
        if user.get('是否分期', '否') == '是':
            base_freq += random.randint(2, 5)
        
        # 确保年度消费频次不超过信用卡额度
        max_freq = user['总额度'] // 1000
        user['年度消费频次'] = min(base_freq, max_freq)
        
        # 单均消费金额
        if user['年度消费频次'] == 0:
            user['单均消费金额'] = 0.0
        else:
            avg = user['年消费总额'] / user['年度消费频次']
            avg = min(avg, user['总额度'])  # 确保不超过信用卡额度
            if random.random() < 0.1:  # 10%高额异常
                avg = random.uniform(1000, 2000)
            else:
                avg = random.uniform(500, 1000)  # 控制在500到1000之间
            # 确保单均消费金额有小数部分
            user['单均消费金额'] = round(avg + random.uniform(0.01, 0.99), 2)
    
    return user

def generate_user_data(num_records):
    data = []
    existing_names = set()
    referrers = []  # 存储活跃推荐人
    
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
        
        # 生成渠道信息（新增）
        user['渠道'] = generate_channel(age)
        
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
        else:
            user['推荐好友数量'] = random.randint(0,1) if user['传播者ID'] ==0 else random.randint(0,3)
        
        # 生成3%异常值
        if random.random() < 0.03:
            user['月收入'] = random.randint(500, 2000)
            if has_card == '是':
                user['总额度'] = random.choice([50000, 100000])
                user['信用评分'] = max(700, user['信用评分'])  # 维持高评分异常
        
        # 添加子女数量生成逻辑
        if user['用户年龄'] < 22:
            user['子女数量'] = 0
        elif user['用户年龄'] < 25:
            user['子女数量'] = random.choices([0, 1], weights=[80, 20])[0]
        elif user['用户年龄'] < 30:
            user['子女数量'] = random.choices([0, 1, 2], weights=[40, 50, 10])[0]
        elif user['用户年龄'] < 40:
            user['子女数量'] = random.choices([0, 1, 2, 3], weights=[20, 50, 25, 5])[0]
        else:
            user['子女数量'] = random.choices([0, 1, 2, 3], weights=[10, 40, 40, 10])[0]
        
        # 如果是学生，强制子女数量为0
        if user['职业'] == '学生':
            user['子女数量'] = 0
        
        # 生成RFM相关字段
        user = generate_rfm_fields(user)
        
        data.append(user)
    
    return data

# 生成数据并保存到指定路径
desktop_path = '/Users/harmnet/Desktop/用户数据.csv'
data = generate_user_data(200)

# 🧨 更新字段列表
fieldnames = [
    '用户ID', '性别', '手机号码', '姓名', '信用卡号', '用户年龄', '已用额度', '余额',
    '生日', '渠道', '是否持有信用卡', '是否分期', '总额度', '月收入', '信用卡级别',
    '贷款金额', '是否有房', '是否有车', '子女数量', '传播者ID', '信用评分', '活跃度等级',
    '消费偏好', '所在城市', '职业', '资产总额', '年消费总额', '信用卡逾期次数', '推荐好友数量',
    '最近消费间隔', '年度消费频次', '单均消费金额'  # 🧨 新增字段
]

desktop_path = '/Users/harmnet/Desktop/用户数据-中高级.csv'
data = generate_user_data(200)

with open(desktop_path, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)
    
print(f"数据已生成到：{desktop_path}")
