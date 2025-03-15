"""
    随机生成产品特征数据，需要和市场订单数据的结果关联匹配
    Created By: 段小飞
    Creation Date: 2024-4-24
"""
import random
import pandas as pd
import datetime
from datetime import date
from faker import Faker
from collections import OrderedDict
from time import sleep
from datetime import datetime, timedelta
from tqdm import tqdm
from openpyxl import load_workbook
import re

def main():
    addlist = [110101, 110102, 110105, 110106, 110107, 110108, 110109, 110111, 110112, 110113,110221, 110224, 110226, 110227, 110228, 110229]
    proviceDict = {'11': '北京市'}
    ID_address = {"110000": "北京市",
                  "110100": "市辖区", "110101": "东城区", "110102": "西城区", "110103": "崇文区", "110104": "宣武区",
                  "110105": "朝阳区", "110106": "丰台区", "110107": "石景山区", "110108": "海淀区","110109": "门头沟区",
                  "110111": "房山区","110112": "通州区","110113": "顺义区","110200": "北京市县","110221": "昌平区",
                  "110224": "大兴区","110226": "平谷区","110227": "怀柔区","110228": "密云区","110229": "延庆区"}
    monthList = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']  # 随机抽取月份数组
    dayList = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17',
               '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28']  # 随机抽取日的数组
    ssnSexDict = OrderedDict([('6111', 0.585), ('8822', 0.415)])
    communityList = ['海淀区-绿洲花园', '海淀区-金色阳光', '海淀区-青山雅居', '海淀区-蓝天家园',
                     '朝阳区-明珠广场', '朝阳区-河畔人家', '朝阳区-森林绿苑', '朝阳区-翠湖名邸',
                     '丰台区-龙湖湾', '丰台区-银河新村', '丰台区-丽景小区', '丰台区-紫荆花城',
                     '石景山区-和谐佳园', '石景山-碧水云天', '石景山-金辉名都', '石景山-晨曦花园',
                     '门头沟区-翡翠华庭', '门头沟-梦想家园', '门头沟-逸景雅筑', '门头沟-星辰广场',
                     '大兴区-雅仕居', '大兴区-悦景轩', '大兴区-江南春色', '大兴区-红叶山庄',
                     '房山区-馨悦家园', '房山区-瑞景华府', '房山区-书香门第', '房山区-金色海岸',
                     '通州区-梦幻家园', '通州区-悦景名邸', '通州区-碧波花园', '通州区-青云直上',
                     '顺义区-东湖明珠', '顺义区-玉兰雅居', '顺义区-明珠新城', '顺义区-绿野仙踪',
                     '昌平区-海滨花园', '昌平区-景云小区', '昌平区-梅花香里', '昌平区-青竹雅苑',
                     '平谷区-紫藤花园', '平谷区-玉带华庭', '平谷区-翠竹园',
                     '怀柔区-金色年华', '怀柔区-雅韵名居', '怀柔区-梦想小镇',
                     '密云区-青山绿水', '密云区-玫瑰园',
                     '延庆区-明珠丽景', '延庆区-花香满庭']

    # 初始化设置
    fake = Faker('zh-CN')  # 指定用中文
    num = 2000  # 初始化模拟数据生成数量

    # 申明字段
    customer_id = []            # 1、用户D
    customer_name = []          # 2、用户姓名
    birthday = []               # 3、生日
    age = []                    # 4、年龄
    sex = []                    # 5、性别
    income_year = []            # 6、个人年收入
    income_year_family = []     # 51、家庭年收入
    Loan_amount_available = []  # 7、可贷款金额
    province = []               # 8、所在省份
    city = []                   # 9、所在城市
    district = []               # 10、所在区
    married = []                # 11、是否已婚
    have_children = []          # 12、子女数量
    have_car = []               # 13、车数量
    main_madia = []             # 14、主要媒体
    buy_date = []               # 15、购房日期
    delivery_date = []          # 16、收房日期
    first_house = []            # 17、是否首套房
    community_name = []         # 18、小区名称
    district_community = []     # 19、小区所在区
    unit_type = []              # 20、户型
    house_attributes = []       # 21、房屋属性（现房/期房）
    house_type = []             # 22、房屋类型（商品房/共有产权房）
    direction = []              # 23、房屋朝向（南向/西向/东向）
    building_area = []          # 24、建筑面积
    use_area = []               # 25、使用面积
    common_area = []            # 26、公摊面积
    num_flours = []             # 27、楼层总数
    flour = []                  # 28、房屋所在楼层
    renovation_status = []      # 29、装修情况（毛坯/简装/精装）
    elevator = []               # 30、有无电梯
    price = []                  # 31、房屋单价
    total_price = []            # 43、房屋总价
    kindergarten = []           # 32、周边1公里幼儿园数量
    primary_school= []          # 33、周边1公里小学数量
    classA_hospital= []         # 34、周边1公里三甲医院数量
    metro = []                  # 35、周边1公里地铁站数量
    market = []                 # 36、周边1公里超市数量
    mall = []                   # 37、周边1公里大型商场数量
    bank = []                   # 38、周边1公里银行网点数量
    restaurant = []             # 39、周边1公里餐饮店数量
    park = []                   # 40、周边1公里公园数量
    gas_station = []            # 41、周边1公里加油站数量
    training = []               # 42、周边1公里教培机构数量
    loan_type = []              # 44、贷款类型
    loan_rate = []              # 45、贷款比例
    loan_amount = []            # 46、贷款金额
    loan_year = []              # 47、贷款年限
    loan_interest_rate = []     # 48、贷款利率
    loan_bank = []              # 49、贷款银行
    monthly_repayment = []      # 50、每月还款金额



    print("----------开始生成数据，祈祷不报错----------")
    j = 0
    for i in tqdm(range(0, num)):
        j = j + 1
        """这里是写每条数据生成的逻辑"""
        # 身份证号，身份证号由5个部分组成。第一个部分为前面6位的地址码。第二个部分为出生年份，主要是控制用户的年龄区间。第三个部分为出生月份。第四个部分为出生日。第五个部分为性别。
        ssn_p1 = ','.join([str(s) for s in random.sample(addlist, 1)])  # 随机生成前面6位地址码
        ssn_p2 = str(fake.random_int(min=1950, max=2000))  # 随机生成出生年份，控制用户的年龄，最大74，最小24
        ssn_p3 = ','.join([str(s) for s in random.sample(monthList, 1)])  # 随机生成出生月份
        ssn_p4 = ','.join([str(s) for s in random.sample(dayList, 1)])  # 随机生成出生日
        ssn_p5 = str(fake.random_element(ssnSexDict))  # 随机生成性别，按照男性58.5%，女性41.5%的比例生成
        ssnValue = ssn_p1 + ssn_p2 + ssn_p3 + ssn_p4 + ssn_p5
        ssnResult = ssnValue[0:13] + '****'

        customer_id.append(j)                                   # 1、用户ID：和生成的数据的序号保持一致，从1开始，到最后一条数据的序号结束
        # 5、性别：根据身份证号获得性别
        if int(ssnValue[16:17]) % 2 != 0:
            sexValue = '1'
        elif int(ssnValue[16:17]) % 2 == 0:
            sexValue = '0'
        sex.append(sexValue)
        # 2、用户姓名
        if sexValue == '1':
            customer_name_value = fake.name_male()
        else:
            customer_name_value = fake.name_female()
        customer_name.append(customer_name_value)
        # 3、生日
        birthday_value = ssn_p2 + '年' + ssn_p3 + '月' + ssn_p4 + '日'
        birthday.append(birthday_value)
        # 4、年龄：根据身份证号获得年龄
        ageValue = 2022 - eval(ssn_p2)
        ageValue_true = 2024 - eval(ssn_p2)
        age.append(ageValue)
        # 6、年收入
        if 23 < ageValue_true < 35:
            income_year_value = fake.random_int(min=500, max=5000)/100
        elif 34 < ageValue_true < 45:
            income_year_value = fake.random_int(min=1000, max=6000) / 100
        elif 44 < ageValue_true :
            income_year_value = fake.random_int(min=1200, max=7000) / 100
        income_year_value_new = str(income_year_value) + '万元'
        income_year.append(income_year_value_new)
        # 7、可贷款金额
        random_rate = fake.random_int(min=18, max=25)/10
        Loan_amount_available_value = round(income_year_value/12*0.3*12*30, 2)
        Loan_amount_available.append(Loan_amount_available_value)
        # 8、所在省份
        provinceValue = '北京市'
        province.append(provinceValue)
        # 9、所在城市
        city_value = '北京市'
        city.append(city_value)
        # 10、所在区
        ID_province = ssnValue[0:6]
        address_value = ID_address[ID_province]
        district.append(address_value)
        # 11、婚姻状态
        marry_dict = OrderedDict(
            [('已婚', 0.4), ('未婚', 0.4), ('离异', 0.2)])
        married_value = fake.random_element(marry_dict)
        married.append(married_value)
        # 12、子女数量
        if married_value in ['已婚', '离异']:
            have_children_value = fake.random_int(min=0, max=3)
        else:
            have_children_value = 0
        have_children.append(have_children_value)
        # 13、名下车数量
        have_car_value = fake.random_int(min=0, max=2)
        have_car.append(have_car_value)
        # 14、主要媒体
        main_madia_dict = OrderedDict([('公众号', 0.12), ('短信', 0.13), ('抖音', 0.2), ('快手', 0.15), ('视频号', 0.2), ('朋友圈', 0.25)])
        main_madia_value = fake.random_element(main_madia_dict)
        main_madia.append(main_madia_value)
        # 21、房屋属性（现房/期房） house_attributes = []
        house_attributes_dict = OrderedDict([('期房', 0.85), ('现房', 0.15)])
        house_attributes_value = fake.random_element(house_attributes_dict)
        house_attributes.append(house_attributes_value)
        # 15、购房日期 buy_date = []
        start_date = datetime.strptime('2021-01-01', "%Y-%m-%d")
        end_date = datetime.strptime('2021-12-31', "%Y-%m-%d")
        buy_date_value = fake.date_between(start_date=start_date, end_date=end_date)
        buy_date.append(buy_date_value)
        # 16、收房日期 delivery_date = []
        if house_attributes_value == '现房':
            days_addition = random.randint(1, 90)
        else:
            days_addition = random.randint(365, 730)
        delivery_date_value = buy_date_value + timedelta(days=days_addition)
        delivery_date.append(delivery_date_value)
        # 17、是否首套房 first_house = []
        first_house_dict = OrderedDict([('是', 0.85), ('否', 0.15)])
        first_house_value = fake.random_element(first_house_dict)
        first_house.append(first_house_value)
        # 18、小区名称 community_name = []
        community_name_temp = ','.join([str(s) for s in random.sample(communityList, 1)])  # 随机生成前面6位地址码
        community_name_value = community_name_temp[community_name_temp.index('-')+1:]
        community_name.append(community_name_value)
        # 19、小区所在区 district_community = []
        district_community_value = community_name_temp[:community_name_temp.index('-')]
        district_community.append(district_community_value)
        # 24、建筑面积 building_area = []
        building_area_value = fake.random_int(min=5000, max=15000)/100
        building_area.append(building_area_value)
        # 25、使用面积 use_area = []
        use_area_rate = fake.random_int(min=7, max=15)/100
        use_area_value = round(building_area_value * use_area_rate,2)
        use_area.append(use_area_value)
        # 26、公摊面积 common_area = []
        common_area_value = building_area_value - use_area_value
        common_area.append(common_area_value)
        # 20、户型 unit_type = []
        if 50 <= building_area_value < 70:
            unit_type_dict = OrderedDict([('一室一厅', 0.35), ('两室一厅', 0.65)])
            unit_type_value = fake.random_element(unit_type_dict)
        elif 70 <= building_area_value < 90:
            unit_type_dict = OrderedDict([('两室一厅', 0.45), ('三室一厅', 0.55)])
            unit_type_value = fake.random_element(unit_type_dict)
        elif 90 <= building_area_value < 120:
            unit_type_dict = OrderedDict([('两室一厅', 0.15), ('三室一厅', 0.65), ('四室一厅', 0.2)])
            unit_type_value = fake.random_element(unit_type_dict)
        else:
            unit_type_dict = OrderedDict([('三室一厅', 0.65), ('四室一厅', 0.35)])
            unit_type_value = fake.random_element(unit_type_dict)
        unit_type.append(unit_type_value)
        # 22、房屋类型（商品房/共有产权房） house_type = []
        if 50 <= building_area_value < 70:
            house_type_dict = OrderedDict([('商品房', 0.45),('共有产权房', 0.55)])
            house_type_value = fake.random_element(house_type_dict)
        else:
            house_type_value = '商品房'
        house_type.append(house_type_value)
        # 23、房屋朝向（南向/西向/东向） direction = []
        direction_dict = OrderedDict([('南向', 0.55), ('东向', 0.3), ('西向', 0.15)])
        direction_value = fake.random_element(direction_dict)
        direction.append(direction_value)
        # 27、楼层总数 num_flours = []
        num_flours_value = fake.random_int(min=6, max=30)
        num_flours.append(num_flours_value)
        # 28、房屋所在楼层 flour = []
        flour_value = fake.random_int(min=1, max=num_flours_value)
        flour.append(flour_value)
        # 29、装修情况（毛坯/简装/精装） renovation_status = []
        renovation_status_dict = OrderedDict([('毛坯', 0.8), ('简装', 0.1), ('精装', 0.1)])
        renovation_status_value = fake.random_element(renovation_status_dict)
        renovation_status.append(renovation_status_value)
        # 30、有无电梯 elevator = []
        if num_flours_value <=6:
            elevator_value = 1
        else:
            elevator_value = 0
        elevator.append(elevator_value)
        # 31、房屋单价 price = []
        if district_community_value == '海淀区':
            price_value = generate_fluctuated_data(71060)
        elif district_community_value == '朝阳区':
            price_value = generate_fluctuated_data(99202)
        elif district_community_value == '丰台区':
            price_value = generate_fluctuated_data(79830)
        elif district_community_value == '石景山区':
            price_value = generate_fluctuated_data(66340)
        elif district_community_value == '门头沟区':
            price_value = generate_fluctuated_data(58884)
        elif district_community_value == '大兴区':
            price_value = generate_fluctuated_data(55880)
        elif district_community_value == '房山区':
            price_value = generate_fluctuated_data(39260)
        elif district_community_value == '通州区':
            price_value = generate_fluctuated_data(48198)
        elif district_community_value == '顺义区':
            price_value = generate_fluctuated_data(45304)
        elif district_community_value == '昌平区':
            price_value = generate_fluctuated_data(51717)
        elif district_community_value == '平谷区':
            price_value = generate_fluctuated_data(30196)
        elif district_community_value == '怀柔区':
            price_value = generate_fluctuated_data(20800)
        elif district_community_value == '密云区':
            price_value = generate_fluctuated_data(26660)
        elif district_community_value == '延庆区':
            price_value = generate_fluctuated_data(24500)
        price.append(round(price_value, 2))
        # 43、房屋总价 total_price
        total_price_value = round(price_value * building_area_value/10000,2)
        total_price.append(total_price_value)
        # 32、周边1公里幼儿园数量 kindergarten = []
        kindergarten_value = fake.random_int(min=0, max=3)
        kindergarten.append(kindergarten_value)
        # 33、周边1公里小学数量 primary_school = []
        primary_school_value = fake.random_int(min=0, max=2)
        primary_school.append(primary_school_value)
        # 34、周边1公里三甲医院数量 classA_hospital = []
        classA_hospital_value = fake.random_int(min=0, max=1)
        classA_hospital.append(classA_hospital_value)
        # 35、周边1公里地铁站数量 metro = []
        metro_value = fake.random_int(min=0, max=1)
        metro.append(metro_value)
        # 36、周边1公里超市数量 market = []
        market_value = fake.random_int(min=1, max=3)
        market.append(market_value)
        # 37、周边1公里大型商场数量 mall = []
        mall_value = fake.random_int(min=0, max=1)
        mall.append(mall_value)
        # 38、周边1公里银行网点数量 bank = []
        bank_value = fake.random_int(min=0, max=3)
        bank.append(bank_value)
        # 39、周边1公里餐饮店数量 restaurant = []
        restaurant_value = fake.random_int(min=1, max=10)
        restaurant.append(restaurant_value)
        # 40、周边1公里公园数量 park = []
        park_value = fake.random_int(min=1, max=3)
        park.append(park_value)
        # 41、周边1公里加油站数量 gas_station = []
        gas_station_value = fake.random_int(min=0, max=2)
        gas_station.append(gas_station_value)
        # 42、周边1公里教培机构数量 training = []
        training_value = fake.random_int(min=0, max=4)
        training.append(training_value)
        # 44、贷款类型 loan_type = []
        loan_type_dict = OrderedDict([('公积金贷款', 0.22), ('商业贷款', 0.78)])
        loan_type_value = fake.random_element(loan_type_dict)
        loan_type.append(loan_type_value)
        # 45、贷款比例 loan_rate = []
        if house_type_value == '商品房':
            values = [20, 25, 30, 35]
            loan_rate_value = random.choice(values)
        else:
            if loan_type_value == '公积金贷款':
                values = [20, 25, 30, 35]
                loan_rate_value = random.choice(values)
            else:
                values = [30, 35]
                loan_rate_value = random.choice(values)
        loan_rate.append(loan_rate_value)
        # 46、贷款金额 loan_amount = []
        loan_amount_value = round(loan_rate_value/100 * price_value * building_area_value, 2)
        loan_amount.append(loan_amount_value)
        # 47、贷款年限 loan_year = []
        values = [20, 25, 30]
        loan_year_value = random.choice(values)
        loan_year.append(loan_year_value)
        # 48、贷款利率 loan_interest_rate = []
        if loan_type_value == '公积金贷款':
            loan_interest_rate_value = 0.0285
        else:
            loan_interest_rate_value = 0.0355
        loan_interest_rate.append(loan_interest_rate_value)
        # 49、贷款银行 loan_bank
        loan_bank_dict = OrderedDict([('工商银行', 0.25), ('农业银行', 0.21), ('中国银行', 0.18), ('建设银行', 0.15), ('北京银行', 0.12), ('招商银行', 0.06), ('浦发银行', 0.03)])
        loan_bank_value = fake.random_element(loan_bank_dict)
        loan_bank.append(loan_bank_value)
        # 50、每月还款金额 monthly_repayment = []
        monthly_repayment_value = calculate_monthly_payment(loan_amount_value,loan_interest_rate_value,loan_year_value)
        monthly_repayment.append(monthly_repayment_value)
        # 51、家庭年收入 income_year_family
        income_year_family_value = loan_amount_value / (0.3 * 30)
        if income_year_value*10000 > income_year_family_value:
            income_year_family_rate = fake.random_int(min=10, max=20)/10
            income_year_family_value = round(income_year_value * income_year_family_rate, 2)
        else:
            income_year_family_value = round(income_year_family_value/10000, 2)
        income_year_family.append(income_year_family_value)
        # 把前面根据逻辑生成的数据，赋值到data这个临时的数据集里面
        data = {
            '用户ID': customer_id,
            '用户姓名': customer_name,
            '生日': birthday,
            '年龄': age,
            '性别': sex,
            '个人年收入（万元）': income_year,
            '家庭年收入（万元）': income_year_family,
            '可贷款金额（万元）': Loan_amount_available,
            '所在省份': province,
            '所在城市': city,
            '所在区': district,
            '是否已婚': married,
            '子女数量': have_children,
            '名下汽车数量': have_car,
            '主要使用媒体': main_madia,
            '购房日期': buy_date,
            '收房日期': delivery_date,
            '是否首套房': first_house,
            '小区名称': community_name,
            '小区所在区': district_community,
            '户型': unit_type,
            '房屋属性': house_attributes,
            '房屋类型': house_type,
            '房屋朝向': direction,
            '建筑面积': building_area,
            '使用面积': use_area,
            '公摊面积': common_area,
            '楼层总数': num_flours,
            '房屋所在楼层': flour,
            '装修情况': renovation_status,
            '有无电梯': elevator,
            '房屋单价': price,
            '房屋总价（万元）': total_price,
            '周边1公里幼儿园数量': kindergarten,
            '周边1公里小学数量': primary_school,
            '周边1公里三甲医院数量': classA_hospital,
            '周边1公里地铁站数量': metro,
            '周边1公里超市数量': market,
            '周边1公里大型商场数量': mall,
            '周边1公里银行网点数量': bank,
            '周边1公里餐饮店数量': restaurant,
            '周边1公里公园数量': park,
            '周边1公里加油站数量': gas_station,
            '周边1公里教培机构数量': training,
            '贷款类型': loan_type,
            '贷款比例': loan_rate,
            '贷款金额': loan_amount,
            '贷款年限': loan_year,
            '贷款利率': loan_interest_rate,
            '贷款银行': loan_bank,
            '每月还款金额': monthly_repayment
        }

    # 把生成的data的数据集，导出成Excel文件
    pd.set_option('display.width', None)  # 设置字符显示无限制
    pd.set_option('display.max_rows', None)  # 设置行数显示无限制
    users = pd.DataFrame.from_dict(data)
    # print(users)
    users.to_csv("customer_info.xlsx", index=True) # 指定生成文件的名字和格式
    print("\n" + "----------执行结束，万幸----------")


def generate_fluctuated_data(base_value, fluctuation_percentage=20):
    """
    在给定的基础值基础上上下浮动指定百分比生成随机数据。

    参数:
    base_value (float): 基础值。
    fluctuation_percentage (int): 上下浮动的百分比，默认为20%。

    返回:
    float: 生成的随机数值。
    """
    # 计算上下限
    lower_bound = base_value * (1 - fluctuation_percentage / 100)
    upper_bound = base_value * (1 + fluctuation_percentage / 100)

    # 生成随机数
    fluctuated_value = random.uniform(lower_bound, upper_bound)

    return fluctuated_value


def calculate_monthly_payment(principal, annual_interest_rate, years):
    """
    计算等额本息还款方式下的每月还款金额。

    参数:
    principal (float): 贷款本金。
    annual_interest_rate (float): 年利率（例如：5 表示 5%）。
    years (int): 贷款年限。

    返回:
    float: 每月还款金额。
    """
    monthly_interest_rate = annual_interest_rate / 100 / 12  # 将年利率转换为月利率
    total_months = years * 12  # 总共的还款期数

    # 计算每月还款金额
    monthly_payment = principal * (monthly_interest_rate * (1 + monthly_interest_rate) ** total_months) / (
                (1 + monthly_interest_rate) ** total_months - 1)

    return round(monthly_payment, 2)  # 四舍五入保留两位小数

if __name__ == '__main__':
    main()