"""
        自动生成客户基础信息
        案例：CMB
        Created By：xujian
        Created Time：2022-11-27
"""
import random
import pandas as pd
from datetime import date
from faker import Faker
from collections import OrderedDict
from time import sleep
from tqdm import tqdm

# 主函数：生成数据
def main():
    addlist = [
        110000, # 北京市
        110100, 110101, 110102, 110103, 110104, 110105, 110106, 110107, 110108, 110109, 110111, 110112, 110113,
        110200, 110221, 110224, 110226, 110227, 110228, 110229,
        120000, # 天津市
        120100, 120101, 120102, 120103, 120104, 120105, 120106, 120107, 120108, 120109, 120110, 120111, 120112, 120113,
        120200, 120221, 120222, 120223, 120224, 120225,
        310000, # 上海市
        310100,310101,310102,310103,310104,310105,310106,310107,310108,310109,310110,310112,310113,310114,310115,310116,310117,
        310200,310225,310226,310229,310230,
        500000,# 重庆市
        500100,500101,  500102, 500103,500104,500105,500106,500107,500108,500109,500110,500111,500112,500113,
        500200,500221,500222,500223,500224,500225,500226,500227,500228,500229,500230,500231,500232,500233,500234,500235,500236,500237,500238,500239,500240,500241,500242,500243,
        500300,500381,500382,500383,500384,
    ]

    ID_address = {"110000": "北京市",
                  "110100": "北京市市辖区","110101": "北京市东城区","110102": "北京市西城区","110103": "北京市崇文区","110104": "北京市宣武区","110105": "北京市朝阳区","110106": "北京市丰台区","110107": "北京市石景山区","110108": "北京市海淀区",
                  "110109": "北京市门头沟区",
                  "110111": "北京市房山区",
                  "110112": "北京市通州区",
                  "110113": "北京市顺义区",
                  "110200": "北京市县",
                  "110221": "北京市昌平县",
                  "110224": "北京市大兴县",
                  "110226": "北京市平谷县",
                  "110227": "北京市怀柔县",
                  "110228": "北京市密云县",
                  "110229": "北京市延庆县",
                  "120000": "天津市",
                  "120100": "天津市市辖区",
                  "120101": "天津市和平区",
                  "120102": "天津市河东区",
                  "120103": "天津市河西区",
                  "120104": "天津市南开区",
                  "120105": "天津市河北区",
                  "120106": "天津市红桥区",
                  "120107": "天津市塘沽区",
                  "120108": "天津市汉沽区",
                  "120109": "天津市大港区",
                  "120110": "天津市东丽区",
                  "120111": "天津市西青区",
                  "120112": "天津市津南区",
                  "120113": "天津市北辰区",
                  "120200": "天津市县",
                  "120221": "天津市宁河县",
                  "120222": "天津市武清县",
                  "120223": "天津市静海县",
                  "120224": "天津市宝坻县",
                  "120225": "天津市蓟县",
                  "310000": "上海市",
                  "310100": "上海市市辖区",
                  "310101": "上海市黄浦区",
                  "310102": "上海市南市区",
                  "310103": "上海市卢湾区",
                  "310104": "上海市徐汇区",
                  "310105": "上海市长宁区",
                  "310106": "上海市静安区",
                  "310107": "上海市普陀区",
                  "310108": "上海市闸北区",
                  "310109": "上海市虹口区",
                  "310110": "上海市杨浦区",
                  "310112": "上海市闵行区",
                  "310113": "上海市宝山区",
                  "310114": "上海市嘉定区",
                  "310115": "上海市浦东新区",
                  "310116": "上海市金山区",
                  "310117": "上海市松江区",
                  "310200": "上海市县",
                  "310225": "上海市南汇县",
                  "310226": "上海市奉贤县",
                  "310229": "上海市青浦县",
                  "310230": "上海市崇明县",
                  "500000": "重庆市",
                  "500100": "重庆市市辖区",
                  "500101": "重庆市万州区",
                  "500102": "重庆市涪陵区",
                  "500103": "重庆市渝中区",
                  "500104": "重庆市大渡口区",
                  "500105": "重庆市江北区",
                  "500106": "重庆市沙坪坝区",
                  "500107": "重庆市九龙坡区",
                  "500108": "重庆市南岸区",
                  "500109": "重庆市北碚区",
                  "500110": "重庆市万盛区",
                  "500111": "重庆市双桥区",
                  "500112": "重庆市渝北区",
                  "500113": "重庆市巴南区",
                  "500200": "重庆市县",
                  "500221": "重庆市长寿县",
                  "500222": "重庆市綦江县",
                  "500223": "重庆市潼南县",
                  "500224": "重庆市铜梁县",
                  "500225": "重庆市大足县",
                  "500226": "重庆市荣昌县",
                  "500227": "重庆市璧山县",
                  "500228": "重庆市梁平县",
                  "500229": "重庆市城口县",
                  "500230": "重庆市丰都县",
                  "500231": "重庆市垫江县",
                  "500232": "重庆市武隆县",
                  "500233": "重庆市忠县",
                  "500234": "重庆市开县",
                  "500235": "重庆市云阳县",
                  "500236": "重庆市奉节县",
                  "500237": "重庆市巫山县",
                  "500238": "重庆市巫溪县",
                  "500239": "重庆市黔江土家族苗族自治县",
                  "500240": "重庆市石柱土家族自治县",
                  "500241": "重庆市秀山土家族苗族自治县",
                  "500242": "重庆市酉阳土家族苗族自治县",
                  "500243": "重庆市彭水苗族土家族自治县",
                  "500300": "重庆市(市)",
                  "500381": "重庆市江津市",
                  "500382": "重庆市合川市",
                  "500383": "重庆市永川市",
                  "500384": "重庆市南川市",
                  }

    monthList = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']  # 随机抽取月份数组
    dayList = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17',
               '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']  # 随机抽取日的数组
    ssnSexDict = OrderedDict([('6910', 0.52), ('8823', 0.48)])
    proviceDict = {'11': '北京市', '12': '天津市', '13': '河北省', '14': '⼭西省', '15': '内蒙古⾃治区',
                   '21': '辽宁省', '22': '吉林省', '23': '⿊龙江省',
                   '31': '上海市', '32': '江苏省', '33': '浙江省', '34': '安徽省', '35': '福建省', '36': '江西省', '37': '⼭东省',
                   '41': '河南省', '42': '湖北省', '43': '湖南省', '44': '⼴东省', '45': '⼴西壮族⾃治区', '46': '海南省',
                   '50': '重庆市', '51': '四川省', '52': '贵州省', '53': '云南省', '54': '西藏⾃治区',
                   '61': '陕西省', '62': '⽢肃省', '63': '青海省', '64': '宁夏回族自治区', '65': '新疆维吾尔⾃治区',
                   '71': '台湾省',
                   '81': '⾹港', '82': '澳门'
                   }

    # 初始化设置
    fake = Faker('zh-CN')   # 指定用中文
    num = 1000                # 初始化模拟数据生成数量
    """
        初始化客户标签字段集以及字段对应的数据字典
    """
    user_id = []                                    # 1、客户ID
    ssn = []                                        # 2、身份证号
    age = []                                        # 3、年龄
    sex = []                                        # 4、性别
    province = []                                   # 5、省份
    mobile = []                                     # 6、手机号
    user_name = []                                  # 7、姓名
    is_deposit_cust = []                            # 8、存款客户
    is_financialProducts_cust = []                  # 9、理财产品客户
    is_creditCard_cust = []                         # 10、信用卡客户
    is_webBanking_cust = []                         # 11、网上银行客户
    is_digitalCNY_cust = []                         # 12、数字人民币客户：数字人民币客户也是网上银行客户
    is_mobileBanking_cust = []                      # 13、手机银行客户
    is_married = []                                 # 14、婚姻状况：已婚、未婚、未知
    house = []                                      # 15、居住状况：一居室、二居室、三居室、四居室、多居室、未知
    house_value = []                                # 16、房产总价值：小于50万、50~100万、100~300万、300~500万、500~1000万、大于1000万
    company_type = []                               # 17、公司类型：私营企业、外资企业、国营企业、个人、其他、未知
    occupation = []                                 # 18、职业：公务员、医生、工人、律师、教师、程序员、记者、其他、未知
    annual_family_income = []                       # 19、家庭年收入：1万以下、1~5万、5~10万、10~20万、20~50万、50~100万、100~200万、200万以上
    household_debt = []                             # 20、家庭负债：1万以下、1~5万、5~10万、10~20万、20~50万、50~100万、100~200万、200万以上，无
    break_times = []                                # 21、个人贷款有效违约次数：0次、1次、2次、3次、3次以上
    eBank_query_times = []                          # 22、网银月查询次数：0次、1~10次、10次以上
    bankCounter_query_times = []                    # 23、柜台月查询次数：0次、1~10次、10次以上
    ATM_query_times = []                            # 24、ATM月查询次数：0次、1~10次、10次以上
    APP_query_times = []                            # 25、APP月查询次数：0次、1~10次、10次以上
    TB_times = []                                   # 26、累计购买国债次数：0次、1~10次、10次以上
    monetaryFund_times = []                         # 27、累计购买货币基金次数：0次、1~10次、10次以上
    shares_times = []                               # 28、累计购买股票次数：0次、1~10次、10次以上
    financialProducts_times = []                    # 29、累计购买理财次数：0次、1~10次、10次以上
    pay_online = []                                 # 30、网上支付次数：0次、1~10次、10次以上
    pay_POS = []                                    # 31、POS机支付次数：0次、1~10次、10次以上
    pay_APP = []                                    # 32、APP支付次数：0次、1~10次、10次以上
    user_activity = []                              # 33、用户活跃度：沉睡客户、普通客户、活跃客户
    customer_level = []                             # 34、客户等级属性：低效客户、关注客户、无效客户、潜力客户、私人银行客户、财富客户、贵宾客户、高净值客户
    customer_loyalty = []                           # 35、客户忠诚度：低忠诚度、中忠诚度、高忠诚度
    customer_tiering = []                           # 36、客户分层：普通客户、金卡客户、白金卡客户、钻石卡客户
    deposit_balance = []                            # 37、存款余额：1万以下、1~5万、5~10万、10~20万、20~50万、50~100万、100~200万、200万以上
    loan_balance = []                               # 38、贷款余额：1万以下、1~5万、5~10万、10~20万、20~50万、50~100万、100~200万、200万以上
    financial_balance = []                          # 39、理财余额：1万以下、1~5万、5~10万、10~20万、20~50万、50~100万、100~200万、200万以上
    financial_style = []                            # 40、理财风格：谨慎型、稳健型、平衡型、进取型、激进型
    number_of_purchases = []                        # 41、最近6个月买入理财产品笔数：0次、1~10次、10次以上
    already_ordered = []                            # 42、是否已购买“引商养老理财”产品：是/否

    print("----------开始生成数据，祈祷不报错----------")

    for i in tqdm(range(0, num)):
        """  按照设定的生成数据数量，逐一生成数据  """
        # 1、客户ID
        user_id_value = fake.random_int(min=100000, max=999999, step=1)
        user_id.append(user_id_value)
        # user_id.append(fake.ssn())
        # 2、身份证号：身份证号是原始关键数据
        ssnID_p1 = ','.join([str(s) for s in random.sample(addlist, 1)])
        ssnID_p2 = str(fake.random_int(min=1960, max=1992))                 # 定义用户的年龄范围
        ssnID_p3 = ','.join([str(s) for s in random.sample(monthList, 1)])
        ssnID_p4 = ','.join([str(s) for s in random.sample(dayList, 1)])
        ssnID_p5 = str(fake.random_element(ssnSexDict))
        ssnID = ssnID_p1 + ssnID_p2 + ssnID_p3 + ssnID_p4 + ssnID_p5
        ssnValue = ssnID
        ssnResult = ssnValue[0:13] + '****'
        ssn.append(ssnResult)
        # 3、年龄：根据身份证号获得年龄
        ageValue = 2024 - eval(ssnValue[6:10])
        age.append(ageValue)
        # 4、性别：根据身份证号获得性别
        if int(ssnValue[16:17]) % 2 != 0: sexValue = '男'
        elif int(ssnValue[16:17]) % 2 == 0: sexValue = '女'
        sex.append(sexValue)
        # 5、省份
        ID_province = ssnValue[0:2]
        provinceValue = proviceDict[ID_province]
        # provinceValue = queryProvice(ssnValue[0:6])
        province.append(provinceValue)
        # 6、手机号：随机生成手机号
        mobleValue = fake.phone_number()
        mobileResult = str(mobleValue[0:3]) + '****' + str(mobleValue[7:11])
        mobile.append(mobileResult)
        # 7、姓名：根据性别生成姓名
        if sexValue == '男': user_name.append(fake.name_female())
        elif sexValue == '女': user_name.append(fake.name_male())
        # 8、存款客户
        is_deposit_cust_dict = OrderedDict([('是', 0.85), ('否', 0.15)])  # 数据字典：是否存款客户
        is_deposit_cust_value = fake.random_element(is_deposit_cust_dict)
        is_deposit_cust.append(is_deposit_cust_value)
        # 9、理财产品客户
        is_financialProducts_cust_dict = OrderedDict([('是', 0.65), ('否', 0.35)])  # 数据字典：是否理财产品客户
        is_financialProducts_cust_value = fake.random_element(is_financialProducts_cust_dict)
        is_financialProducts_cust.append(is_financialProducts_cust_value)
        # 10、信用卡客户
        is_creditCard_cust_dict = OrderedDict([('是', 0.95), ('否', 0.05)])  # 数据字典：是否信用卡客户
        is_creditCard_cust_value = fake.random_element(is_creditCard_cust_dict)
        is_creditCard_cust.append(is_creditCard_cust_value)
        # 11、网上银行客户
        is_webBanking_cust_dict = OrderedDict([('是', 0.85), ('否', 0.15)])  # 数据字典：网上银行客户
        is_webBanking_cust_value = fake.random_element(is_webBanking_cust_dict)
        is_webBanking_cust.append(is_webBanking_cust_value)
        # 12、数字人民币客户：数字人民币客户也是网上银行客户
        is_digitalCNY_cust.append(is_webBanking_cust_value)
        # 13、手机银行客户
        is_mobileBanking_cust_dict = OrderedDict([('是', 0.75), ('否', 0.25)])  # 数据字典：是否手机银行客户
        is_mobileBanking_cust_value = fake.random_element(is_mobileBanking_cust_dict)
        is_mobileBanking_cust.append(is_mobileBanking_cust_value)
        # 14、婚姻状况：已婚、未婚、未知
        is_married_dict = OrderedDict([('已婚', 0.50), ('未婚', 0.35), ('未知', 0.15)])  # 数据字典：婚姻状况
        is_married_value = fake.random_element(is_married_dict)
        is_married.append(is_married_value)
        # 15、居住状况：一居室、二居室、三居室、四居室、多居室、未知
        house_dict = OrderedDict([('一居室', 0.20), ('二居室', 0.35), ('三居室', 0.20), ('四居室', 0.15), ('多居室', 0.05), ('未知', 0.05)])  # 数据字典：居住状况
        house_value1 = fake.random_element(house_dict)
        house.append(house_value1)
        # 16、房产总价值：小于50万、50~100万、100~300万、300~500万、500~1000万、大于1000万
        if house_value1 in ['一居室']:
            house_value_dict = OrderedDict(
                [('小于50万', 0.55), ('50~100万', 0.40), ('100~300万', 0.05), ('300~500万', 0.00), ('500~1000万', 0.00), ('大于1000万', 0.00)])  # 数据字典：房产总价值
            house_value_value = fake.random_element(house_value_dict)
            #house_value.append(house_value_value)
        elif house_value1 in ['二居室', '三居室']:
            house_value_dict = OrderedDict(
                [('小于50万', 0.05), ('50~100万', 0.25), ('100~300万', 0.45), ('300~500万', 0.20), ('500~1000万', 0.05),('大于1000万', 0.00)])  # 数据字典：房产总价值
            house_value_value = fake.random_element(house_value_dict)
            #house_value.append(house_value_value)
        elif house_value1 in ['四居室', '多居室']:
            house_value_dict = OrderedDict(
                [('小于50万', 0.00), ('50~100万', 0.00), ('100~300万', 0.05), ('300~500万', 0.30), ('500~1000万', 0.45),('大于1000万', 0.20)])  # 数据字典：房产总价值
            house_value_value = fake.random_element(house_value_dict)
            #house_value.append(house_value_value)
        elif house_value1 in ['未知']:
            house_value_value = '未知'
        house_value.append(house_value_value)
        # 17、公司类型：私营企业、外资企业、国营企业、个人、其他、未知
        company_type_dict = OrderedDict(
            [('私营企业', 0.40), ('外资企业', 0.20), ('国营企业', 0.10), ('个人', 0.15), ('其他', 0.10), ('未知', 0.05)])  # 数据字典：公司类型
        company_type_value = fake.random_element(company_type_dict)
        company_type.append(company_type_value)
        # 18、职业：公务员、医生、工人、律师、教师、程序员、记者、企业家、未知
        occupation_dict = OrderedDict(
            [('公务员', 0.05), ('医生', 0.15), ('工人', 0.05), ('律师', 0.10), ('教师', 0.05), ('程序员', 0.30), ('记者', 0.05), ('企业家', 0.15), ('未知', 0.10)])  # 数据字典：职业
        occupation_value = fake.random_element(occupation_dict)
        occupation.append(occupation_value)
        # 19、家庭年收入：1万以下、1~5万、5~10万、10~20万、20~50万、50~100万、100~200万、200万以上
        if occupation_value in ['医生', '律师', '企业家']:
            annual_family_income_dict = OrderedDict(
                [('1万以下', 0.00), ('1~5万', 0.00), ('5~10万', 0.00), ('10~20万', 0.00), ('20~50万', 0.10), ('50~100万', 0.55), ('100~200万', 0.25), ('200万以上', 0.10)])  # 数据字典：家庭年收入
            annual_family_income_value = fake.random_element(annual_family_income_dict)
            annual_family_income.append(annual_family_income_value)
        elif occupation_value in ['公务员', '程序员', '记者']:
            annual_family_income_dict = OrderedDict(
                [('1万以下', 0.00), ('1~5万', 0.00), ('5~10万', 0.00), ('10~20万', 0.20), ('20~50万', 0.55), ('50~100万', 0.25), ('100~200万', 0.00), ('200万以上', 0.00)])  # 数据字典：家庭年收入
            annual_family_income_value = fake.random_element(annual_family_income_dict)
            annual_family_income.append(annual_family_income_value)
        elif occupation_value in ['工人', '教师', '未知']:
            annual_family_income_dict = OrderedDict(
                [('1万以下', 0.05), ('1~5万', 0.05), ('5~10万', 0.20), ('10~20万', 0.55), ('20~50万', 0.15), ('50~100万', 0.00), ('100~200万', 0.00), ('200万以上', 0.00)])  # 数据字典：家庭年收入
            annual_family_income_value = fake.random_element(annual_family_income_dict)
            annual_family_income.append(annual_family_income_value)
        # 20、家庭负债：1万以下、1~5万、5~10万、10~20万、20~50万、50~100万、100~200万、200万以上，无
        if occupation_value in ['医生', '律师', '企业家']:
            household_debt_dict = OrderedDict(
                [('1万以下', 0.00), ('1~5万', 0.00), ('5~10万', 0.00), ('10~20万', 0.00), ('20~50万', 0.10), ('50~100万', 0.55), ('100~200万', 0.25), ('200万以上', 0.10)])  # 数据字典：家庭负债
            household_debt_value = fake.random_element(household_debt_dict)
            household_debt.append(household_debt_value)
        elif occupation_value in ['公务员', '程序员', '记者']:
            household_debt_dict = OrderedDict(
                [('1万以下', 0.00), ('1~5万', 0.00), ('5~10万', 0.00), ('10~20万', 0.20), ('20~50万', 0.55), ('50~100万', 0.25), ('100~200万', 0.00), ('200万以上', 0.00)])  # 数据字典：家庭负债
            household_debt_value = fake.random_element(household_debt_dict)
            household_debt.append(household_debt_value)
        elif occupation_value in ['工人', '教师', '未知']:
            household_debt_dict = OrderedDict(
                [('1万以下', 0.05), ('1~5万', 0.05), ('5~10万', 0.20), ('10~20万', 0.55), ('20~50万', 0.15), ('50~100万', 0.00), ('100~200万', 0.00), ('200万以上', 0.00)])  # 数据字典：家庭负债
            household_debt_value = fake.random_element(household_debt_dict)
            household_debt.append(household_debt_value)
        # 21、个人贷款有效违约次数：0次、1次、2次、3次、3次以上
        if occupation_value in ['医生', '律师', '企业家']:
            break_times_dict = OrderedDict(
                [('0次', 0.45), ('1次', 0.25), ('2次', 0.20), ('3次', 0.10), ('3次以上', 0.10)])  # 数据字典：个人贷款有效违约次数
            break_times_value = fake.random_element(break_times_dict)
            break_times.append(break_times_value)
        elif occupation_value in ['公务员', '程序员', '记者']:
            break_times_dict = OrderedDict(
                [('0次', 0.65), ('1次', 0.25), ('2次', 0.10), ('3次', 0.00), ('3次以上', 0.00)])  # 数据字典：个人贷款有效违约次数
            break_times_value = fake.random_element(break_times_dict)
            break_times.append(break_times_value)
        elif occupation_value in ['工人', '教师', '未知']:
            break_times_dict = OrderedDict(
                [('0次', 0.65), ('1次', 0.20), ('2次', 0.10), ('3次', 0.05), ('3次以上', 0.00)])  # 数据字典：个人贷款有效违约次数
            break_times_value = fake.random_element(break_times_dict)
            break_times.append(break_times_value)
        # 22、网银月查询次数：0次、1~10次、10次以上
        eBank_query_times_dict = OrderedDict(
            [('0次', 0.20), ('1~10次', 0.60), ('10次以上', 0.20)])  # 数据字典：网银月查询次数
        eBank_query_times_value = fake.random_element(eBank_query_times_dict)
        eBank_query_times.append(eBank_query_times_value)
        # 23、柜台月查询次数：0次、1~10次、10次以上
        bankCounter_query_times_dict = OrderedDict(
            [('0次', 0.30), ('1~10次', 0.65), ('10次以上', 0.05)])  # 数据字典：柜台月查询次数
        bankCounter_query_times_value = fake.random_element(bankCounter_query_times_dict)
        bankCounter_query_times.append(bankCounter_query_times_value)
        # 24、ATM月查询次数：0次、1~10次、10次以上
        ATM_query_times_dict = OrderedDict(
            [('0次', 0.75), ('1~10次', 0.25), ('10次以上', 0.00)])  # 数据字典：ATM月查询次数
        ATM_query_times_value = fake.random_element(ATM_query_times_dict)
        ATM_query_times.append(ATM_query_times_value)
        # 25、APP月查询次数：0次、1~10次、10次以上
        APP_query_times_dict = OrderedDict(
            [('0次', 0.05), ('1~10次', 0.75), ('10次以上', 0.20)])  # 数据字典：APP月查询次数
        APP_query_times_value = fake.random_element(APP_query_times_dict)
        APP_query_times.append(APP_query_times_value)
        # 26、累计购买国债次数：0次、1~10次、10次以上
        TB_times_dict = OrderedDict(
            [('0次', 0.25), ('1~10次', 0.70), ('10次以上', 0.05)])  # 数据字典：累计购买国债次数
        TB_times_value = fake.random_element(TB_times_dict)
        TB_times.append(TB_times_value)
        # 27、累计购买货币基金次数：0次、1~10次、10次以上
        monetaryFund_times_dict = OrderedDict(
            [('0次', 0.25), ('1~10次', 0.70), ('10次以上', 0.05)])  # 数据字典：累计购买货币基金次数
        monetaryFund_times_value = fake.random_element(monetaryFund_times_dict)
        monetaryFund_times.append(monetaryFund_times_value)
        # 28、累计购买股票次数：0次、1~10次、10次以上
        shares_times_dict = OrderedDict(
            [('0次', 0.05), ('1~10次', 0.20), ('10次以上', 0.75)])  # 数据字典：累计购买股票次数
        shares_times_value = fake.random_element(shares_times_dict)
        shares_times.append(shares_times_value)
        # 29、累计购买理财次数：0次、1~10次、10次以上
        financialProducts_times_dict = OrderedDict(
            [('0次', 0.05), ('1~10次', 0.10), ('10次以上', 0.85)])  # 数据字典：累计购买理财次数
        financialProducts_times_value = fake.random_element(financialProducts_times_dict)
        financialProducts_times.append(financialProducts_times_value)
        # 30、网上支付次数：0次、1~10次、10次以上
        pay_online_dict = OrderedDict(
            [('0次', 0.00), ('1~10次', 0.10), ('10次以上', 0.90)])  # 数据字典：网上支付次数
        pay_online_value = fake.random_element(pay_online_dict)
        pay_online.append(pay_online_value)
        # 31、POS机支付次数：0次、1~10次、10次以上
        pay_POS_dict = OrderedDict(
            [('0次', 0.00), ('1~10次', 0.10), ('10次以上', 0.90)])  # 数据字典：POS机支付次数
        pay_POS_value = fake.random_element(pay_POS_dict)
        pay_POS.append(pay_POS_value)
        # 32、APP支付次数：0次、1~10次、10次以上
        pay_APP_dict = OrderedDict(
            [('0次', 0.00), ('1~10次', 0.10), ('10次以上', 0.90)])  # 数据字典：APP支付次数
        pay_APP_value = fake.random_element(pay_APP_dict)
        pay_APP.append(pay_APP_value)
        # 33、用户活跃度：沉睡客户、普通客户、活跃客户
        if pay_online_value == '1~10次' and pay_POS_value == '1~10次' and pay_APP_value == '1~10次':
            user_activity_value = '沉睡客户'
        elif pay_online_value == '10次以上' and pay_POS_value == '10次以上' and pay_APP_value == '10次以上':
            user_activity_value = '活跃客户'
        else:
            user_activity_value = '普通客户'
        user_activity.append(user_activity_value)
        # 34、客户等级属性：低效客户、关注客户、无效客户、潜力客户、私人银行客户、财富客户、贵宾客户、高净值客户
        if user_activity_value in ['沉睡客户'] and annual_family_income_value in ['1万以下']:
            customer_level_value = '无效客户'
        elif user_activity_value in ['沉睡客户'] and annual_family_income_value in ['1~5万', '10~20万']:
            customer_level_value = '低效客户'
        elif user_activity_value in ['沉睡客户'] and annual_family_income_value in ['20~50万', '50~100万', '100~200万', '200万以上']:
            customer_level_value = '潜力客户'
        elif user_activity_value in ['活跃客户', '普通客户'] and annual_family_income_value in ['5~10万', '10~20万']:
            customer_level_value = '关注客户'
        elif user_activity_value in ['活跃客户', '普通客户'] and annual_family_income_value in ['20~50万']:
            customer_level_value = '财富客户'
        elif user_activity_value in ['活跃客户', '普通客户'] and annual_family_income_value in ['50~100万']:
            customer_level_value = '贵宾客户'
        elif user_activity_value in ['活跃客户', '普通客户'] and annual_family_income_value in ['100~200万']:
            customer_level_value = '高净值客户'
        elif user_activity_value in ['活跃客户', '普通客户'] and annual_family_income_value in ['200万以上']:
            customer_level_value = '私人银行客户'
        else:
            customer_level_value = '关注客户'
        customer_level.append(customer_level_value)
        # 35、客户忠诚度：低忠诚度、中忠诚度、高忠诚度
        customer_loyalty_dict = OrderedDict(
            [('低忠诚度', 0.250), ('中忠诚度', 0.50), ('高忠诚度', 0.25)])  # 数据字典：客户忠诚度
        customer_loyalty_value = fake.random_element(customer_loyalty_dict)
        customer_loyalty.append(customer_loyalty_value)
        # 36、客户分层：普通客户、金卡客户、白金卡客户、钻石卡客户
        if annual_family_income_value in ['1万以下', '1~5万']:
            customer_tiering_value = '普通客户'
        elif annual_family_income_value in ['10~20万']:
            customer_tiering_value = '金卡客户'
        elif annual_family_income_value in ['20~50万']:
            customer_tiering_value = '白金卡客户'
        else:
            customer_tiering_value = '钻石卡客户'
        customer_tiering.append(customer_tiering_value)
        # 37、存款余额：1万以下、1~5万、5~10万、10~20万、20~50万、50~100万、100~200万、200万以上
        deposit_balance_dict = OrderedDict(
            [('1万以下', 0.05), ('1~5万', 0.05), ('5~10万', 0.20), ('10~20万', 0.55), ('20~50万', 0.15), ('50~100万', 0.00),('100~200万', 0.00), ('200万以上', 0.00)])  # 数据字典：家庭负债
        deposit_balance_value = fake.random_element(deposit_balance_dict)
        deposit_balance.append(deposit_balance_value)
        # 38、贷款余额：1万以下、1~5万、5~10万、10~20万、20~50万、50~100万、100~200万、200万以上
        if house_value in ['一居室']:
            loan_balance_dict = OrderedDict(
                [('1万以下', 0.00), ('1~5万', 0.00), ('5~10万', 0.10), ('10~20万', 0.25), ('20~50万', 0.55), ('50~100万', 0.10), ('100~200万', 0.00), ('200万以上', 0.00)])  # 数据字典：贷款余额
            loan_balance_value = fake.random_element(loan_balance_dict)
            loan_balance.append(loan_balance_value)
        elif house_value in ['二居室', '三居室']:
            loan_balance_dict = OrderedDict(
                [('1万以下', 0.00), ('1~5万', 0.00), ('5~10万', 0.00), ('10~20万', 0.00), ('20~50万', 0.05), ('50~100万', 0.30), ('100~200万', 0.40), ('200万以上', 0.25)])  # 数据字典：贷款余额
            loan_balance_value = fake.random_element(loan_balance_dict)
            loan_balance.append(loan_balance_value)
        elif house_value in ['四居室', '多居室']:
            loan_balance_dict = OrderedDict(
                [('1万以下', 0.00), ('1~5万', 0.00), ('5~10万', 0.00), ('10~20万', 0.00), ('20~50万', 0.00), ('50~100万', 0.00), ('100~200万', 0.20), ('200万以上', 0.80)])  # 数据字典：贷款余额
            loan_balance_value = fake.random_element(loan_balance_dict)
            loan_balance.append(loan_balance_value)
        else:
            loan_balance_value = '未知'
            loan_balance.append(loan_balance_value)
        # 39、理财余额：1万以下、1~5万、5~10万、10~20万、20~50万、50~100万、100~200万、200万以上
        financial_balance_dict = OrderedDict(
            [('1万以下', 0.05), ('1~5万', 0.05), ('5~10万', 0.15), ('10~20万', 0.55), ('20~50万', 0.15), ('50~100万', 0.05),('100~200万', 0.00), ('200万以上', 0.00)])  # 数据字典：理财余额
        financial_balance_value = fake.random_element(financial_balance_dict)
        financial_balance.append(financial_balance_value)
        # 40、理财风格：谨慎型、稳健型、平衡型、进取型、激进型
        financial_style_dict = OrderedDict([('谨慎型', 0.25), ('稳健型', 0.30), ('平衡型', 0.25), ('进取型', 0.15), ('激进型', 0.05)])  # 数据字典：理财风格
        financial_style_value = fake.random_element(financial_style_dict)
        financial_style.append(financial_style_value)
        # 41、最近6个月买入理财产品笔数：0次、1~10次、10次以上
        number_of_purchases_dict = OrderedDict([('0次', 0.25), ('1~10次', 0.50), ('10次以上', 0.25)])  # 数据字典：最近6个月买入理财产品笔数
        number_of_purchases_value = fake.random_element(number_of_purchases_dict)
        number_of_purchases.append(number_of_purchases_value)
        # 42、是否已购买“引商养老理财”产品：是/否
        already_ordered_dict = OrderedDict([('是', 0.05), ('否', 0.95)])  # 数据字典：是否已购买“引商养老理财”产品
        already_ordered_value = fake.random_element(already_ordered_dict)
        already_ordered.append(already_ordered_value)

        data = {
            '客户ID': user_id,                                    # 1、客户ID
            '身份证号': ssn,                                       # 2、身份证号
            '年龄': age,                                          # 3、年龄
            '性别': sex,                                          # 4、性别
            '省份': province,                                     # 5、省份
            '手机号': mobile,                                      # 6、手机号
            '姓名': user_name,                                    # 7、姓名
            '存款客户': is_deposit_cust,                           # 8、存款客户
            '理财产品客户': is_financialProducts_cust,            # 9、理财产品客户
            '信用卡客户': is_creditCard_cust,                        # 10、信用卡客户
            '网上银行客户': is_webBanking_cust,                       # 11、网上银行客户
            '数字人民币客户': is_digitalCNY_cust,                   # 12、数字人民币客户：数字人民币客户也是网上银行客户
            '手机银行客户': is_mobileBanking_cust,                # 13、手机银行客户
            '婚姻状况': is_married,                                 # 14、婚姻状况：已婚、未婚、未知
            '居住状况': house,                                      # 15、居住状况：一居室、二居室、三居室、四居室、多居室、未知
            '房产总价值': house_value,                               # 16、房产总价值：小于50万、50~100万、100~300万、300~500万、500~1000万、大于1000万
            '公司类型': company_type,                               # 17、公司类型：私营企业、外资企业、国营企业、个人、其他、未知
            '职业': occupation,                                   # 18、职业：公务员、医生、工人、律师、教师、程序员、记者、其他、未知
            '家庭年收入': annual_family_income,                      # 19、家庭年收入：1万以下、1~5万、5~10万、10~20万、20~50万、50~100万、100~200万、200万以上
            '家庭负债': household_debt,                             # 20、家庭负债：1万以下、1~5万、5~10万、10~20万、20~50万、50~100万、100~200万、200万以上，无
            '个人贷款有效违约次数': break_times,                      # 21、个人贷款有效违约次数：0次、1次、2次、3次、3次以上
            '网银月查询次数': eBank_query_times,                   # 22、网银月查询次数：0次、1~10次、10次以上
            '柜台月查询次数': bankCounter_query_times,                 # 23、柜台月查询次数：0次、1~10次、10次以上
            'ATM月查询次数': ATM_query_times,                        # 24、ATM月查询次数：0次、1~10次、10次以上
            'APP月查询次数': APP_query_times,                        # 25、APP月查询次数：0次、1~10次、10次以上
            '累计购买国债次数': TB_times,                           # 26、累计购买国债次数：0次、1~10次、10次以上
            '累计购买货币基金次数': monetaryFund_times,               # 27、累计购买货币基金次数：0次、1~10次、10次以上
            '累计购买股票次数': shares_times,                       # 28、累计购买股票次数：0次、1~10次、10次以上
            '累计购买理财次数': financialProducts_times,            # 29、累计购买理财次数：0次、1~10次、10次以上
            '网上支付次数': pay_online,                               # 30、网上支付次数：0次、1~10次、10次以上
            'POS机支付次数': pay_POS,                                # 31、POS机支付次数：0次、1~10次、10次以上
            'APP支付次数': pay_APP,                                 # 32、APP支付次数：0次、1~10次、10次以上
            '用户活跃度': user_activity,                             # 33、用户活跃度：沉睡客户、普通客户、活跃客户
            '客户等级属性': customer_level,                           # 34、客户等级属性：低效客户、关注客户、无效客户、潜力客户、私人银行客户、财富客户、贵宾客户、高净值客户
            '客户忠诚度': customer_loyalty,                              # 35、客户忠诚度：低忠诚度、中忠诚度、高忠诚度
            '客户分层': customer_tiering,                           # 36、客户分层：普通客户、金卡客户、白金卡客户、钻石卡客户
            '存款余额': deposit_balance,                            # 37、存款余额：1万以下、1~5万、5~10万、10~20万、20~50万、50~100万、100~200万、200万以上
            '贷款余额': loan_balance,                               # 38、贷款余额：1万以下、1~5万、5~10万、10~20万、20~50万、50~100万、100~200万、200万以上
            '理财余额': financial_balance,                          # 39、理财余额：1万以下、1~5万、5~10万、10~20万、20~50万、50~100万、100~200万、200万以上
            '理财风格': financial_style,                            # 40、理财风格：谨慎型、稳健型、平衡型、进取型、激进型
            '最近6个月买入理财产品笔数': number_of_purchases,           # 41、最近6个月买入理财产品笔数：0次、1~10次、10次以上
            '是否已购买产品': already_ordered                          # 42、是否已购买“引商养老理财”产品：是/否
        }

    pd.set_option('display.width', None)  # 设置字符显示无限制
    pd.set_option('display.max_rows', None)  # 设置行数显示无限制
    users = pd.DataFrame.from_dict(data)
    # print(users)
    users.to_csv("CMB_user.xlsx", index=True)
    print("\n" + "----------执行结束，万幸----------")

if __name__ == '__main__':
    main()