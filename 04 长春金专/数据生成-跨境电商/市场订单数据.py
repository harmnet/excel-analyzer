"""
    随机生成市场订单数据
    Created By: 段小飞
    Creation Date: 2024-4-23
"""
import random
import pandas as pd
import datetime
from datetime import date
from faker import Faker
from collections import OrderedDict
from time import sleep
from tqdm import tqdm

def main():
    # 初始化设置
    fake = Faker('zh-CN')  # 指定用中文
    num = 100000  # 初始化模拟数据生成数量

    # 申明字段
    order_num = []              # 1、订单编号
    company_name = []           # 2、竞争者公司
    product_name = []           # 3、商品名称
    product_type = []           # 4、商品类型
    order_date = []             # 5、订单日期
    order_year = []             # 6、订单年份
    order_quarterly = []        # 7、订单季度
    order_day = []              # 8、订单天数
    order_type = []             # 9、订单类型
    price = []                  # 10、商品单价
    discount = []               # 11、优惠金额
    quantity = []               # 12、销量
    sales_amount = []           # 13、销售额
    cost = []                   # 14、成本
    profitability_rate = []     # 15、利润率
    hwc = []                    # 16、海外仓
    shipping_fee = []           # 17、运费
    ASIN = []                   # 18、ASIN
    customer_id = []            # 19、消费者ID
    shipping_country = []       # 20、运送国家
    purchasing_power = []       # 21、消费能力
    customer_type = []          # 22、消费者类型
    age = []                    # 23、年龄
    sex = []                    # 24、性别

    print("----------开始生成数据，祈祷不报错----------")
    j = 0
    for i in tqdm(range(0, num)):
        j = j+1
        """
            这里是写每条数据生成的逻辑
        """
        # 1、订单编号order_num（生成规则为：DSK2024+6位序列号），支持最多100万条数据
        order_num_value = 'DSK2024' + str(j)     # 拼装order_num的值
        order_num.append(order_num_value)   # 给order_num赋值
        # 2、竞争者公司company_name（按照4：3：3的比例，三家公司：爱宠宠物用品公司、华佩宠物用品公司、金华宠物用品公司）
        company_name_dict = OrderedDict([('爱宠宠物用品公司', 0.4), ('华佩宠物用品公司', 0.3), ('金华宠物用品公司', 0.3)])
        company_name_value = fake.random_element(company_name_dict)
        company_name.append(company_name_value)
        # 4、商品类型product_type（按照的比例0.18：0.15：0.25：0.14：0.12:0.16生成，分别有：宠物咀嚼玩具、宠物粮、宠物如厕训练垫、宠物洗发露、伸缩式狗绳、自动宠物饮水机）
        product_type_dict = OrderedDict([('宠物咀嚼玩具', 0.18), ('宠物粮', 0.15), ('宠物如厕训练垫', 0.25), ('宠物洗发露', 0.14), ('伸缩式狗绳', 0.12), ('自动宠物饮水机', 0.16)])
        product_type_value = fake.random_element(product_type_dict)
        product_type.append(product_type_value)
        # 3、商品名称product_name（按照不同的商品类型分别生成）
        product_name_value = ''
        if product_type_value == '宠物咀嚼玩具':
            product_name_dict = OrderedDict(
                [('15cm绿色玉米磨牙棒', 0.25), ('20cm红色苹果磨牙棒', 0.42), ('25cm黄色香蕉磨牙棒', 0.33)])
            product_name_value = fake.random_element(product_name_dict)
        elif product_type_value == '宠物粮':
            product_name_dict = OrderedDict(
                [('10kg鸡肉配方宠物粮', 0.45), ('20kg鱼肉配方宠物粮', 0.55)])
            product_name_value = fake.random_element(product_name_dict)
        elif product_type_value == '宠物如厕训练垫':
            product_name_dict = OrderedDict(
                [('100片XL经典宠物尿垫', 0.35), ('500片S码宠物尿垫', 0.15), ('20片M码经济款宠物尿垫', 0.5)])
            product_name_value = fake.random_element(product_name_dict)
        elif product_type_value == '宠物洗发露':
            product_name_dict = OrderedDict(
                [('500ml除虱去痒抑菌玫瑰香宠物沐浴露', 0.35), ('200ml除虱去痒抑菌桂花香宠物沐浴露', 0.15), ('201ml除虱去痒抑菌茉莉香宠物沐浴露', 0.5)])
            product_name_value = fake.random_element(product_name_dict)
        elif product_type_value == '伸缩式狗绳':
            product_name_value = '3m蓝色常规版自动伸缩狗绳'
        elif product_type_value == '自动宠物饮水机':
            product_name_value = '宠物智能饮水机'
        product_name.append(product_name_value)
        # 5、订单日期order_date：在2023年1月1日～2023年12月31日之间随机生成
        start_date = datetime.date(2023, 1, 1)  # 随机生成日期的开始节点
        end_date = datetime.date(2023, 12, 31)   # 随机生成日期的结束节点
        order_date_value = fake.date_between(start_date=start_date, end_date=end_date)  # 随机生成日期
        order_date.append(order_date_value)
        # 6、订单年份order_year：根据订单日期计算得来
        order_year_value = order_date_value.year
        order_year.append(order_year_value)
        # 7、订单季度order_quarterly：根据订单日期计算得来
        order_month = order_date_value.month
        order_quarterly_value = '空'
        if order_month in [1, 2, 3]:
            order_quarterly_value = '一季度'
        elif order_month in [4, 5, 6]:
            order_quarterly_value = '二季度'
        elif order_month in [7, 8, 9]:
            order_quarterly_value = '三季度'
        elif order_month in [10, 11, 12]:
            order_quarterly_value = '四季度'
        order_quarterly.append(order_quarterly_value)
        # 8、订单天数：根据订单日期计算得来
        order_day_value = order_date_value.day
        order_day.append(order_day_value)
        # 9、订单类型：按照正常购买15%，限时折扣33%，优惠券52%的比例随机生成
        order_type_dict = OrderedDict([('正常购买', 0.15), ('限时折扣', 0.33), ('优惠券', 0.52)])
        order_type_value = fake.random_element(order_type_dict)
        order_type.append(order_type_value)
        # 10、商品单价price：根据不同的产品，随机生成单价，精确到小数点后2位
        price_value = 0
        if product_name_value == '15cm绿色玉米磨牙棒':
            price_value = fake.random_int(min=1400, max=2000) / 100
        elif product_name_value == '20cm红色苹果磨牙棒':
            price_value = fake.random_int(min=1500, max=2200) / 100
        elif product_name_value == '25cm黄色香蕉磨牙棒':
            price_value = fake.random_int(min=1800, max=2500) / 100
        elif product_name_value == '10kg鸡肉配方宠物粮':
            price_value = fake.random_int(min=8800, max=15000) / 100
        elif product_name_value == '20kg鱼肉配方宠物粮':
            price_value = fake.random_int(min=15200, max=31000) / 100
        elif product_name_value == '100片XL经典宠物尿垫':
            price_value = fake.random_int(min=1100, max=3200) / 100
        elif product_name_value == '500片S码宠物尿垫':
            price_value = fake.random_int(min=3500, max=10500) / 100
        elif product_name_value == '20片M码经济款宠物尿垫':
            price_value = fake.random_int(min=400, max=1500) / 100
        elif product_name_value == '500ml除虱去痒抑菌玫瑰香宠物沐浴露':
            price_value = fake.random_int(min=1000, max=5400) / 100
        elif product_name_value == '200ml除虱去痒抑菌桂花香宠物沐浴露':
            price_value = fake.random_int(min=800, max=2500) / 100
        elif product_name_value == '201ml除虱去痒抑菌茉莉香宠物沐浴露':
            price_value = fake.random_int(min=800, max=2500) / 100
        elif product_name_value == '3m蓝色常规版自动伸缩狗绳':
            price_value = fake.random_int(min=2500, max=9900) / 100
        elif product_name_value == '宠物智能饮水机':
            price_value = fake.random_int(min=6000, max=16000) / 100
        price.append(price_value)
        # 12、销量quantity：在1～20之间随机生成
        quantity_value = fake.random_int(min=1, max=20)
        quantity.append(quantity_value)
        # 11、优惠金额discount：如果是正常购买，则没有优惠金额，如果是限时折扣或者优惠券，则为单价*折扣*数量，折扣在0.7～0.95之间随机生成
        discount_value = 0
        if order_type_value == '正常购买':
            discount_value = 0
        elif order_type_value == '限时折扣':
            discount_rate = fake.random_int(min=70, max=95) / 100
            discount_value = price_value * (1 - discount_rate) * quantity_value
        elif order_type_value == '优惠券':
            discount_rate = fake.random_int(min=70, max=95) / 100
            discount_value = price_value * (1 - discount_rate) * quantity_value
        discount.append(discount_value)
        # 13、销售额sales_amount：销售额=销售单价*数量 -优惠金额
        sales_amount_value = quantity_value * price_value - discount_value
        sales_amount.append(sales_amount_value)
        # 14、成本cost：按照销售价格的50%～70%随机生成成本
        cost_rate = fake.random_int(min=50, max=70) / 100
        cost_value = price_value * cost_rate * quantity_value
        cost.append(cost_value)
        # 15、利润率profitability_rate，利润率=利润/成本*100%
        profitability = sales_amount_value - cost_value
        profitability_rate_value = profitability / cost_value
        profitability_rate.append(profitability_rate_value)
        # 16、海外仓
        hwc_dict = OrderedDict([('3号仓', 0.55), ('1号仓', 0.32), ('2号仓', 0.13)])
        hwc_value = fake.random_element(hwc_dict)
        hwc.append(hwc_value)
        # 20、运送国家
        shipping_country_dict = OrderedDict([('美国', 0.15), ('法国', 0.23), ('意大利', 0.32), ('澳大利亚', 0.22), ('俄罗斯', 0.08)])
        shipping_country_value = fake.random_element(shipping_country_dict)
        shipping_country.append(shipping_country_value)
        # 17、运费
        if shipping_country_value == '美国':
            shipping_fee_value = fake.random_int(min=500, max=1000) / 100
        elif shipping_country_value == '法国':
            shipping_fee_value = fake.random_int(min=400, max=800) / 100
        elif shipping_country_value == '意大利':
            shipping_fee_value = fake.random_int(min=350, max=800) / 100
        elif shipping_country_value == '澳大利亚':
            shipping_fee_value = fake.random_int(min=300, max=700) / 100
        elif shipping_country_value == '俄罗斯':
            shipping_fee_value = fake.random_int(min=200, max=500) / 100
        shipping_fee.append(shipping_fee_value)
        # 18、ASIN
        ASIN_value = 'ASIN' + fake.credit_card_number()
        ASIN.append(ASIN_value)
        # 19、消费者ID
        customer_id_value = 'CID' + fake.credit_card_number()
        customer_id.append(customer_id_value)
        # 21、消费能力
        purchasing_power_dict = OrderedDict([('50~100美元', 0.55), ('100～200美元', 0.32), ('200美元以上', 0.13)])
        purchasing_power_value = fake.random_element(purchasing_power_dict)
        purchasing_power.append(purchasing_power_value)
        # 22、消费者类型
        customer_type_dict = OrderedDict([('综合评价', 0.55), ('注重品牌', 0.32), ('犹豫不定', 0.13)])
        customer_type_value = fake.random_element(customer_type_dict)
        customer_type.append(customer_type_value)
        # 23、年龄
        age_value = fake.random_int(min=20, max=50)
        age.append(age_value)
        # 24、性别
        sex_dict = OrderedDict([('男', 0.55), ('女', 0.45)])
        sex_value = fake.random_element(sex_dict)
        sex.append(sex_value)

        # 把前面根据逻辑生成的数据，赋值到data这个临时的数据集里面
        data = {
            '订单编号': order_num,
            '竞争者公司': company_name,
            '商品名称': product_name,
            '商品类型': product_type,
            '订单日期': order_date,
            '订单年份': order_year,
            '订单季度': order_quarterly,
            '订单天数': order_day,
            '订单类型': order_type,
            '商品单价': price,
            '优惠金额': discount,
            '销量': quantity,
            '销售额': sales_amount,
            '成本': cost,
            '利润率': profitability_rate,
            '海外仓': hwc,
            '运费': shipping_fee,
            'ASIN': ASIN,
            '消费者ID': customer_id,
            '运送国家': shipping_country,
            '消费能力': purchasing_power,
            '消费者类型': customer_type,
            '年龄': age,
            '性别': sex
        }

    # 把生成的data的数据集，导出成Excel文件
    pd.set_option('display.width', None)  # 设置字符显示无限制
    pd.set_option('display.max_rows', None)  # 设置行数显示无限制
    users = pd.DataFrame.from_dict(data)
    # print(users)
    users.to_csv("ccjz_ddsj.xlsx", index=True) # 指定生成文件的名字和格式
    print("\n" + "----------执行结束，万幸----------")

if __name__ == '__main__':
    main()