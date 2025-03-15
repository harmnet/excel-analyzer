"""
        自动生成客户基础信息
        Created By：duanxiaofei
        Created Time：2023-06-13
"""
import datetime
import random
import pandas as pd
from datetime import date, timedelta
from faker import Faker
from collections import OrderedDict
from time import sleep
from tqdm import tqdm
import time

# 主函数：生成数据
def main():
    # 读取地区编码
    file_path = r'01地区编码.txt'
    addlist = []
    with open(file_path, 'r', encoding='utf-8') as file: addlist = file.read().split(',')
    addlist = [line.strip() for line in addlist]
    
    # 读取月份列表数据
    monthList = []  
    file_path = r'04月份列表.txt'
    with open(file_path, 'r', encoding='utf-8') as file: monthList = file.read().split(',')
    monthList = [line.strip() for line in monthList]

    # 读取日期列表数据
    file_path = r'05日期列表.txt'
    dayList = []
    with open(file_path, 'r', encoding='utf-8') as file: dayList = file.read().split(',')
    dayList = [line.strip() for line in dayList]

    # 读取性别字典数据，这里还控制了男女性别的比例
    ssnSexDict = OrderedDict([('6910', 0.52), ('8823', 0.48)])

    # 读取省份字典数据
    proviceDict = {}
    with open("02省份名称对照表.txt", 'r', encoding='utf-8') as file:
    # 读取文件的每一行
        for line in file:
            # 去除每行的前后空白字符（包括换行符）
            line = line.strip()
            # 分割键和值，假设键和值之间用冒号和空格分隔
            if ':' in line:
                key, value = line.split(':', 1)
                # 将键和值添加到字典中
                proviceDict[key] = value
    
    # 读取地址字典数据
    addressDict = {}
    with open("03地区名称对照表.txt", 'r', encoding='utf-8') as file:
    # 读取文件的每一行
        for line in file:
            # 去除每行的前后空白字符（包括换行符）
            line = line.strip()
            # 分割键和值，假设键和值之间用冒号和空格分隔
            if ':' in line:
                key, value = line.split(':', 1)
                # 将键和值添加到字典中
                addressDict[key] = value

    """ 初始化设置 """
    fake = Faker('zh-CN')   # 指定用中文
    num = 10                # 初始化模拟数据生成数量

    """ 初始化客户标签字段集以及字段对应的数据字典 """
    order_num = []                                              # 1、订单编号
    product_name = []                                           # 2、商品
    brand = []                                                  # 3、品牌
    product_type = []                                           # 品类
    material = []                                               # 材质
    amount = []                                                 # 4、销量
    price = []                                                  # 5、单价（保留小数点后2位）
    sales_volume = []                                           # 6、销售额（销售额 = 单价*销量，保留小数点后2位）
    real_price = []                                             # 7、实际单价（保留小数点后2位）
    real_sales_volume = []                                      # 8、实际付款（实际付款 = 销售额-实际单价*销量，保留小数点后2位）
    responser = []                                              # 9、负责人
    shop_name = []                                              # 10、店铺
    satisfaction = []                                           # 11、客户满意度
    transaction_status = []                                     # 12、交易状态
    product_status = []                                         # 13、商品状态
    color = []                                                  # 14、颜色
    pay_date=[]                                                 # 15、支付时间
    estimate_arrival_date = []                                  # 16、预计到达时间
    actual_arrival_date = []                                    # 17、实际到达时间
    consignee_name = []                                         # 18、收货人姓名
    consignee_mobile = []                                       # 19、收货电话
    ship_address = []                                           # 20、发货地址
    address_province = []                                       # 21、收货省份
    address = []                                                # 21、收货地址
    logistics = []                                              # 22、物流公司
    logistics_num = []                                          # 23、运单号
    logistics_type = []                                         # 24、运送方式
    order_type = []                                             # 25、客户购买类型
    is_return = []                                              # 26、是否退货
    member_level = []                                           # 27、会员情况
    web_visitor = []                                            # 28、是否访问页面
    web_stay = []                                               # 29、页面访问时长
    birthday = []                                               # 出生日期
    customer_age = []                                           # 30、客户年龄
    customer_gender = []                                        # 31、客户性别
    is_discount = []                                            # 32、是否优惠
    discount = []                                               # 33、优惠金额
    return_reason = []                                          # 34、退款原因
    logistics_result = []                                       # 35、快递反馈

    print("----------开始生成数据，祈祷不报错----------")

    for i in tqdm(range(0, num)):
        """  按照设定的生成数据数量，逐一生成数据  """
        # 1、订单编号order_num
        order_num_value = 'A' + str(fake.random_int(min=100000, max=999999, step=1))
        order_num.append(order_num_value)
        # 3、品牌
        brand_dict = OrderedDict(
            [('ANLY', 0.081), ('TARA', 0.071), ('H&R', 0.067), ('优衣裤', 0.066), ('威兰西', 0.065), ('朝都衣舍', 0.064), ('林马', 0.063), ('太平盛世', 0.061), ('富贵人', 0.058),
             ('雅羊人', 0.056), ('丽丽', 0.051), ('伊芙莉', 0.05), ('秋水美人', 0.039), ('音儿', 0.037),('逸阳', 0.035), ('梵莉思', 0.034), ('拉夏贝尔', 0.031), ('玖姿', 0.024),
             ('艾米丽', 0.021), ('艾波儿', 0.015), ('蒂亚尼', 0.011)
             ])  # 数据字典：商品名称
        brand_value = fake.random_element(brand_dict)
        brand.append(brand_value)
        # 2、商品product_name（按照不同的品牌设置商品名称）
        if brand_value in ['ANLY','TARA','H&R','优衣裤','威兰西','朝都衣舍','林马','太平盛世','富贵人']:
            product_name_dict = OrderedDict(
                [('春夏季新款裤子', 0.061), ('复古牛仔裤', 0.041),
                 ('黑色嘻哈运动裤', 0.019), ('加绒牛仔裤', 0.017), ('卡卡收腹裤', 0.017), ('喇叭裤', 0.012), ('蕾丝安全裤', 0.01),
                  ('七分牛仔裤', 0.034),
                ('不规则T恤', 0.024), ('纯棉T恤', 0.035), ('短款露脐T恤', 0.036), ('复古小熊印花T恤', 0.021),
                 ('蓝色小熊T恤', 0.021), ('蕾丝花边T恤', 0.057), ('少女感T恤', 0.03),
                 ('网红短款T恤', 0.054), ('小个子T恤', 0.021), ('新款欧美T恤', 0.028), ('泫雅风T恤', 0.071),
                ('不规则连衣裙', 0.024), ('春季新款连衣裙', 0.031), ('春夏新款连衣裙', 0.061), ('纯棉连衣裙', 0.026), ('冬季新款连衣裙', 0.021),
                 ('复古连衣裙', 0.03), ('秋冬款连衣裙', 0.035), ('网红同款连衣裙', 0.069),
                 ('熊短款连衣裙', 0.023), ('泫雅风连衣裙', 0.081)
                ])  # 数据字典：商品名称
            product_name_value = fake.random_element(product_name_dict)
            product_name.append(product_name_value)
        elif brand_value == '威兰西':
            product_name_dict = OrderedDict(
                [('安全裤', 0.04), ('春夏季新款裤子', 0.065), ('大码牛仔裤', 0.035), ('大码运动裤', 0.028), ('复古牛仔裤', 0.031),
                 ('黑色嘻哈运动裤', 0.035), ('加绒牛仔裤', 0.042), ('卡卡收腹裤', 0.022), ('喇叭裤', 0.028), ('蕾丝安全裤', 0.025),
                 ('南极鲨鱼裤', 0.022), ('七分牛仔裤', 0.035),
                 ('不规则连衣裙', 0.05), ('春季新款连衣裙', 0.078), ('春夏新款连衣裙', 0.054), ('纯棉连衣裙', 0.035), ('冬季新款连衣裙', 0.048),
                 ('复古连衣裙', 0.05), ('黑暗风连衣裙', 0.031), ('秋冬款连衣裙', 0.046), ('网红同款连衣裙', 0.052), ('小心机连衣裙', 0.035),
                 ('熊短款连衣裙', 0.045), ('泫雅风连衣裙', 0.068)
                 ])  # 数据字典：商品名称
            product_name_value = fake.random_element(product_name_dict)
            product_name.append(product_name_value)
        else:
            product_name_dict = OrderedDict(
                [('安全裤', 0.03), ('春夏季新款裤子', 0.031), ('大码牛仔裤', 0.025), ('大码运动裤', 0.028), ('复古牛仔裤', 0.019),
                 ('黑色嘻哈运动裤', 0.02), ('加绒牛仔裤', 0.03), ('卡卡收腹裤', 0.022), ('喇叭裤', 0.019), ('蕾丝安全裤', 0.025),
                 ('南极鲨鱼裤', 0.022), ('七分牛仔裤', 0.022),
                 ('不规则T恤', 0.017), ('纯棉T恤', 0.023), ('短款露脐T恤', 0.019), ('复古小熊印花T恤', 0.017), ('古着感T恤', 0.022),
                 ('黑暗风T恤', 0.022), ('款式法式T恤', 0.019), ('蓝色小熊T恤', 0.031), ('蕾丝花边T恤', 0.022), ('少女感T恤', 0.019),
                 ('网红短款T恤', 0.022), ('小个子T恤', 0.02), ('新款欧美T恤', 0.019), ('泫雅风T恤', 0.022),
                 ('不规则连衣裙', 0.04), ('春季新款连衣裙', 0.028), ('春夏新款连衣裙', 0.027), ('纯棉连衣裙', 0.028), ('冬季新款连衣裙', 0.032),
                 ('复古连衣裙', 0.034), ('黑暗风连衣裙', 0.031), ('秋冬款连衣裙', 0.031), ('网红同款连衣裙', 0.037), ('小心机连衣裙', 0.035),
                 ('熊短款连衣裙', 0.035), ('泫雅风连衣裙', 0.034)
                 ])  # 数据字典：商品名称
            product_name_value = fake.random_element(product_name_dict)
            product_name.append(product_name_value)

        # 品类
        temp1 = '裤'
        temp2 = '连衣裙'
        temp3 = 'T恤'
        if temp1 in product_name_value:
            product_type_value = '女裤'
        elif temp2 in product_name_value:
            product_type_value = '连衣裙'
        elif temp3 in product_name_value:
            product_type_value = '上衣'
        product_type.append(product_type_value)

        # 材质
        material_dict1 = OrderedDict(
                [('棉质', 0.65), ('麻质', 0.2), ('氨纶', 0.15)])
        material_dict2 = OrderedDict(
            [('棉质', 0.15), ('麻质', 0.3), ('氨纶', 0.55)])
        material_dict3 = OrderedDict(
            [('锦纶', 0.55), ('麻质', 0.2), ('氨纶', 0.25)])
        if product_type_value == '上衣':
            material_value = fake.random_element(material_dict1)
        elif product_type_value == '连衣裙':
            material_value = fake.random_element(material_dict2)
        elif product_type_value == '女裤':
            material_value = fake.random_element(material_dict3)
        material.append(material_value)

        # 10、店铺shop_name（按照不同的品牌设置店铺名称）
        if brand_value in ['ONLY', 'ZARA', 'H&M', '优衣库', '威兰西精品', '韩都衣舍', '森马', '太平鸟', 'GAP']:
            shop_name_temp = brand_value + '旗舰店'
            shop_name_dict = OrderedDict(
                [(shop_name_temp, 0.06), ('3458服饰店', 0.01),
                 ('LOVE依族女装', 0.01), ('飞呀飞服饰', 0.01), ('金依依女装', 0.01)])  # 数据字典：店铺
            shop_name_value = fake.random_element(shop_name_dict)
            shop_name.append(shop_name_value)
        else:
            shop_name_temp = brand_value + '旗舰店'
            shop_name_dict = OrderedDict(
                [(shop_name_temp, 0.03), ('秋兰女装专卖店', 0.01),
                 ('你好呀女装店', 0.01), ('壹佰女装', 0.01), ('自由自在服饰店', 0.01),
                 ('韩派小屋', 0.01), ('COCO女装', 0.01), ('卡卡家女装', 0.01)])  # 数据字典：店铺
            shop_name_value = fake.random_element(shop_name_dict)
            shop_name.append(shop_name_value)
        # 15、支付时间pay_date
        year_dict = OrderedDict([('2019', 0.21), ('2020', 0.14), ('2021', 0.17), ('2022', 0.20), ('2023', 0.28)])
        year_value = fake.random_element(year_dict)
        if year_value == '2019':
            month_dict = OrderedDict([
                ('01', 0.039), ('02', 0.022), ('03', 0.033), ('04', 0.055),
                ('05', 0.049), ('06', 0.12), ('07', 0.066), ('08', 0.065),
                ('09', 0.069), ('10', 0.062), ('11', 0.31), ('12', 0.11)])
            month_value = fake.random_element(month_dict)
        elif year_value == '2020':
            month_dict = OrderedDict([
                ('01', 0.12), ('02', 0.11), ('03', 0.088), ('04', 0.031),
                ('05', 0.025), ('06', 0.056), ('07', 0.067), ('08', 0.075),
                ('09', 0.108), ('10', 0.098), ('11', 0.125), ('12', 0.097)])
            month_value = fake.random_element(month_dict)
        elif year_value == '2021':
            month_dict = OrderedDict([
                ('01', 0.0309), ('02', 0.0256), ('03', 0.0368), ('04', 0.0473),
                ('05', 0.0502), ('06', 0.205), ('07', 0.0628), ('08', 0.0633),
                ('09', 0.0588), ('10', 0.0363), ('11', 0.255), ('12', 0.128)])
            month_value = fake.random_element(month_dict)
        elif year_value == '2022':
            month_dict = OrderedDict([
                ('01', 0.0299), ('02', 0.0205), ('03', 0.035), ('04', 0.0406),
                ('05', 0.0455), ('06', 0.158), ('07', 0.053), ('08', 0.058),
                ('09', 0.057), ('10', 0.055), ('11', 0.035), ('12', 0.0975)])
            month_value = fake.random_element(month_dict)
        elif year_value == '2023':
            month_dict = OrderedDict([
                ('01', 0.039), ('02', 0.022), ('03', 0.033), ('04', 0.055),
                ('05', 0.049), ('06', 0.12), ('07', 0.066), ('08', 0.065),
                ('09', 0.069), ('10', 0.062), ('11', 0.31), ('12', 0.11)])
            month_value = fake.random_element(month_dict)
        if month_value == '02':
            day_value = fake.random_int(min=1, max=28, step=1)
        elif month_value in ['01', '03', '05', '07', '08', '10', '12']:
            day_value = fake.random_int(min=1, max=31, step=1)
        else:
            day_value = fake.random_int(min=1, max=30, step=1)

        pay_date_value = year_value + '-' + month_value + '-' + str(day_value)
        pay_date_value = datetime.datetime.strptime(pay_date_value, '%Y-%m-%d')

        # pay_date_value = (fake.date_between(start_date=date(2019, 1, 1), end_date=date(2022, 12, 31)))
        pay_date.append(pay_date_value)
        # 4、销量amount
        if year_value == '2019':
            amount_dict = OrderedDict(
                [('1', 0.6), ('2', 0.2), ('3', 0.1), ('4', 0.01), ('5', 0.01), ('6', 0.01), ('7', 0.01), ('8', 0.01),
                ('9', 0.01), ('10', 0.01), ('11', 0.01), ('12', 0.01), ('13', 0.01)])  # 数据字典：店铺
            amount_value = fake.random_element(amount_dict)
        elif year_value == '2020':
            amount_dict = OrderedDict(
                [('1', 0.75), ('2', 0.2), ('3', 0.03), ('4', 0.01), ('5', 0.01)])  # 数据字典：店铺
            amount_value = fake.random_element(amount_dict)
        elif year_value == '2021':
            amount_dict = OrderedDict(
                [('1', 0.7), ('2', 0.2), ('3', 0.05), ('4', 0.01), ('5', 0.01), ('6', 0.01), ('7', 0.01), ('8', 0.01)])  # 数据字典：店铺
            amount_value = fake.random_element(amount_dict)
        elif year_value == '2022':
            amount_dict = OrderedDict(
                [('1', 0.65), ('2', 0.2), ('3', 0.1), ('4', 0.01), ('5', 0.01), ('6', 0.01), ('7', 0.01), ('8', 0.01)])  # 数据字典：店铺
            amount_value = fake.random_element(amount_dict)
        elif year_value == '2023':
            amount_dict = OrderedDict(
                [('1', 0.6), ('2', 0.2), ('3', 0.1), ('4', 0.01), ('5', 0.01), ('6', 0.01), ('7', 0.01), ('8', 0.01),
                ('9', 0.01), ('10', 0.01), ('11', 0.01), ('12', 0.01), ('13', 0.01)])  # 数据字典：店铺
            amount_value = fake.random_element(amount_dict)
        amount.append(amount_value)
        # 5、单价price
        if year_value == '2019':
            price_value = fake.random_int(min=4000, max=29999, step=1) / 100
        elif year_value == '2020':
            price_value = fake.random_int(min=2000, max=19999, step=1) / 100
        elif year_value == '2021':
            price_value = fake.random_int(min=3000, max=21999, step=1) / 100
        elif year_value == '2022':
            price_value = fake.random_int(min=3000, max=29999, step=1) / 100
        elif year_value == '2023':
            price_value = fake.random_int(min=4000, max=39999, step=1) / 100
        price.append(price_value)
        # 6、销售额sales_volume
        sales_volume_value = float(price_value) * float(amount_value)
        sales_volume.append(sales_volume_value)

        # 32、是否优惠is_discount
        if month_value == '06':
            is_discount_dict = OrderedDict(
                [('无', 0.15), ('618优惠', 0.70), ('店铺活动优惠', 0.15)])  # 数据字典：是否优惠
            is_discount_value = fake.random_element(is_discount_dict)
        elif month_value == '11':
            is_discount_dict = OrderedDict(
                [('无', 0.05), ('双11优惠', 0.85), ('店铺活动优惠', 0.10)])  # 数据字典：是否优惠
            is_discount_value = fake.random_element(is_discount_dict)
        elif month_value == '12':
            is_discount_dict = OrderedDict(
                [('无', 0.25), ('双12优惠', 0.60), ('店铺活动优惠', 0.15)])  # 数据字典：是否优惠
            is_discount_value = fake.random_element(is_discount_dict)
        else:
            is_discount_dict = OrderedDict(
                [('无', 0.65), ('店铺活动优惠', 0.35)])  # 数据字典：是否优惠
            is_discount_value = fake.random_element(is_discount_dict)
        is_discount.append(is_discount_value)
        # 33、优惠金额discount
        if is_discount_value == '无':
            discount_value = '0'
        elif is_discount_value == '双11优惠':
            if sales_volume_value <= 50:
                discount_dict = OrderedDict([('5', 0.8), ('3', 0.2)])  # 数据字典：优惠金额
                discount_value = fake.random_element(discount_dict)
            elif 50 < sales_volume_value <= 200:
                discount_dict = OrderedDict([('5', 0.3), ('10', 0.5), ('20', 0.2)])  # 数据字典：优惠金额
                discount_value = fake.random_element(discount_dict)
            elif 200 < sales_volume_value <= 500:
                discount_dict = OrderedDict([('10', 0.3), ('20', 0.5), ('50', 0.2)])  # 数据字典：优惠金额
                discount_value = fake.random_element(discount_dict)
            elif 500 < sales_volume_value:
                discount_dict = OrderedDict([('50', 0.3), ('100', 0.5), ('200', 0.2)])  # 数据字典：优惠金额
                discount_value = fake.random_element(discount_dict)
        elif is_discount_value == '618优惠':
            if sales_volume_value <= 50:
                discount_dict = OrderedDict([('5', 0.8), ('3', 0.2)])  # 数据字典：优惠金额
                discount_value = fake.random_element(discount_dict)
            elif 50 < sales_volume_value <= 200:
                discount_dict = OrderedDict([('5', 0.3), ('10', 0.5), ('20', 0.2)])  # 数据字典：优惠金额
                discount_value = fake.random_element(discount_dict)
            elif 200 < sales_volume_value <= 500:
                discount_dict = OrderedDict([('10', 0.3), ('20', 0.5), ('50', 0.2)])  # 数据字典：优惠金额
                discount_value = fake.random_element(discount_dict)
            elif 500 < sales_volume_value:
                discount_dict = OrderedDict([('50', 0.3), ('100', 0.5), ('200', 0.2)])  # 数据字典：优惠金额
                discount_value = fake.random_element(discount_dict)
        elif is_discount_value == '双12优惠':
            if sales_volume_value <= 50:
                discount_dict = OrderedDict([('3', 0.8), ('5', 0.2)])  # 数据字典：优惠金额
                discount_value = fake.random_element(discount_dict)
            elif 50 < sales_volume_value <= 200:
                discount_dict = OrderedDict([('5', 0.3), ('8', 0.5), ('15', 0.2)])  # 数据字典：优惠金额
                discount_value = fake.random_element(discount_dict)
            elif 200 < sales_volume_value <= 500:
                discount_dict = OrderedDict([('10', 0.3), ('15', 0.5), ('30', 0.2)])  # 数据字典：优惠金额
                discount_value = fake.random_element(discount_dict)
            elif 500 < sales_volume_value:
                discount_dict = OrderedDict([('30', 0.3), ('800', 0.5), ('150', 0.2)])  # 数据字典：优惠金额
                discount_value = fake.random_element(discount_dict)
        elif is_discount_value == '店铺活动优惠':
            if sales_volume_value <= 50:
                discount_dict = OrderedDict([('5', 0.8), ('10', 0.2)])  # 数据字典：优惠金额
                discount_value = fake.random_element(discount_dict)
            elif 50 < sales_volume_value <= 200:
                discount_dict = OrderedDict([('8', 0.3), ('12', 0.5), ('15', 0.2)])  # 数据字典：优惠金额
                discount_value = fake.random_element(discount_dict)
            elif 200 < sales_volume_value <= 500:
                discount_dict = OrderedDict([('12', 0.3), ('15', 0.5), ('20', 0.2)])  # 数据字典：优惠金额
                discount_value = fake.random_element(discount_dict)
            elif 500 < sales_volume_value:
                discount_dict = OrderedDict([('20', 0.3), ('40', 0.5), ('100', 0.2)])  # 数据字典：优惠金额
                discount_value = fake.random_element(discount_dict)
        discount.append(discount_value)

        # 7、实际单价real_price
        real_price_value = round((float(sales_volume_value) - float(discount_value)) / float(amount_value),2)
        real_price.append(real_price_value)

        # 8、实际付款real_sales_volume
        real_sales_volume_value = float(sales_volume_value) - float(discount_value)
        real_sales_volume.append(real_sales_volume_value)

        # 25、客户购买类型order_type
        if int(amount_value) <= 3:
            order_type_value = '零售'
        else:
            order_type_value = '批发'
        order_type.append(order_type_value)

        # 14、颜色color
        color_dict = OrderedDict([('白色', 0.156), ('橙色', 0.089), ('粉色', 0.15), ('黑色', 0.05), ('红色', 0.112), ('黄色', 0.087),
                                  ('灰色', 0.067), ('蓝色', 0.098), ('青色', 0.055), ('紫色', 0.035), ('花色', 0.101)])  # 数据字典：颜色
        color_value = fake.random_element(color_dict)
        color.append(color_value)

        # 31、客户性别customer_gender
        customer_gender_dict = OrderedDict(
            [('0', 0.75), ('1', 0.25)])  # 数据字典：客户性别
        customer_gender_value = fake.random_element(customer_gender_dict)
        customer_gender.append(customer_gender_value)

        # 30、出生日期
        ssn_p2 = str(fake.random_int(min=1960, max=2004))  # 随机生成出生年份，控制用户的年龄，最大74，最小24
        ssn_p3 = ','.join([str(s) for s in random.sample(monthList, 1)])  # 随机生成出生月份
        ssn_p4 = ','.join([str(s) for s in random.sample(dayList, 1)])  # 随机生成出生日
        birthday_value = ssn_p2 + '年' + ssn_p3 + '月' + ssn_p4 + '日'
        birthday.append(birthday_value)

        # 30、客户年龄customer_age
        ageValue = 2022 - eval(ssn_p2)
        # customer_age_value = fake.random_int(min=18, max=45, step=1)
        customer_age.append(ageValue)

        # 27、会员情况member_level
        member_level_dict = OrderedDict(
            [('无会员', 0.6), ('普通会员', 0.15), ('白银会员', 0.1), ('黄金会员', 0.1), ('钻石会员', 0.05)])  # 数据字典：会员情况
        member_level_value = fake.random_element(member_level_dict)
        member_level.append(member_level_value)

        # 28、是否访问页面web_visitor
        web_visitor_dict = OrderedDict(
            [('是', 0.834), ('否', 0.166)])  # 数据字典：会员情况
        web_visitor_value = fake.random_element(web_visitor_dict)
        web_visitor.append(web_visitor_value)

        # 29、访问页面时长web_stay
        if web_visitor_value == '否':
            web_stay_value = 0
        else:
            web_stay_value = fake.random_int(min=1, max=9, step=1)
        web_stay.append(web_stay_value)

        # 12、交易状态transaction_status
        transaction_status_dict = OrderedDict(
            [('交易成功', 0.8), ('卖家已发货', 0.03), ('交易取消', 0.1), ('买家已付款', 0.05), ('等待买家付款', 0.02)])  # 数据字典：会员情况
        transaction_status_value = fake.random_element(transaction_status_dict)
        transaction_status.append(transaction_status_value)

        # 13、商品状态product_status
        if transaction_status_value == '交易成功': product_status_value = '已收货'
        elif transaction_status_value == '卖家已发货':
            product_status_dict = OrderedDict(
                [('已收货', 0.3), ('已到达', 0.4), ('已发货', 0.3)])
            product_status_value = fake.random_element(product_status_dict)
        elif transaction_status_value == '交易取消': product_status_value = '已取消'
        elif transaction_status_value == '买家已付款': product_status_value = '未发货'
        elif transaction_status_value == '等待买家付款':
            product_status_value = '未发货'
        product_status.append(product_status_value)

        # 18、收货人姓名consignee_name
        consignee_name.append(fake.name_female())

        # 19、收货人电话consignee_mobile
        consignee_mobile_value = fake.phone_number()
        consignee_mobile_value2 = str(consignee_mobile_value[0:3]) + '****' + str(consignee_mobile_value[7:11])
        consignee_mobile.append(consignee_mobile_value2)

        # 20、发货地址ship_address
        if brand_value in ['ANLY', 'TARA', 'H&R', '优衣裤', '威兰西', '朝都衣舍', '林马', '太平盛世', '富贵人']:
            ship_address_dict = OrderedDict(
                [('广东省', 0.3), ('浙江省', 0.4), ('福建省', 0.2), ('四川省', 0.1)])
            ship_address_value = fake.random_element(ship_address_dict)
        else:
            ship_address_dict = OrderedDict(
                [('广东省', 0.4), ('浙江省', 0.4), ('福建省', 0.2)])
            ship_address_value = fake.random_element(ship_address_dict)
        ship_address.append(ship_address_value)

        # 21、收货地址省份
        ssnValue = ','.join([str(s) for s in random.sample(addlist, 1)])
        ID_province = "'" + ssnValue[0:2] + "'"
        try:
            province_value = proviceDict[ID_province]
        except KeyError:
            province_value = '未知省份'
        address_province.append(province_value)

        # 3、省市县：根据身份证号获得省市县信息
        ID_add = ssnValue[0:6] 
        try:
            address_value2 = addressDict[ID_add]
        except KeyError:
            address_value2 = '未知地区'
        address.append(address_value2)

        # 9、负责人responser
        responser_dict = {
            '黑龙江省': ['卢辉', '张三', '李四'],
            '吉林省': ['赵春梅', '王五', '赵六'],
            '辽宁省': ['梁秀珍', '孙七', '周八'],
            '山东省': ['王健', '吴九', '郑十'],
            '上海市': ['秦桂香', '钱十一', '孙十二'],
            '江苏省': ['李畅', '周十三', '吴十四'],
            '福建省': ['刘浩', '郑十五', '王十六'],
            '浙江省': ['何莹', '冯十七', '陈十八'],
            '江西省': ['胡华', '褚十九', '卫二十'],
            '安徽省': ['李宁', '蒋二一', '沈二二'],
            '河南省': ['杨兰英', '韩二三', '杨二四'],
            '湖北省': ['李淑华', '朱二五', '秦二六'],
            '湖南省': ['邹勇', '尤二七', '许二八'],
            '内蒙古自治区': ['刘慧', '何二九', '吕三十'],
            '河北省': ['陈建平', '施三一', '张三二'],
            '北京市': ['张俊', '孔三三', '曹三四'],
            '天津市': ['卢丽丽', '严三五', '华三六'],
            '山西省': ['董春梅', '金三七', '魏三八'],
            '广西壮族自治区': ['王志强', '陶三九', '姜四十'],
            '广东省': ['张璐', '戚四一', '谢四二'],
            '海南省': ['路淑英', '邹四三', '喻四四'],
            '甘肃省': ['王海燕', '柏四五', '水四六'],
            '青海省': ['黄晶', '窦四七', '章四八'],
            '陕西省': ['袁英', '云四九', '苏五十'],
            '宁夏回族自治区': ['宋建华', '潘五一', '葛五二'],
            '新疆维吾尔自治区': ['季玉兰', '奚五三', '范五四'],
            '云南省': ['高雪', '彭五五', '郎五六'],
            '贵州省': ['冯凯', '鲁五七', '韦五八'],
            '四川省': ['吴帅', '昌五九', '马六十'],
            '重庆市': ['陈金凤', '苗六一', '凤六二'],
            '西藏自治区': ['张龙', '花六三', '方六四'],
            '未知省份': ['刘佳', '任六五', '袁六六']
        }
        print(province_value)
        responser_value = fake.random_element(responser_dict[province_value])
        responser.append(responser_value)

        # 22、物流公司logistics
        if brand_value in ['ANLY', 'TARA', 'H&R', '优衣裤', '威兰西', '朝都衣舍', '林马', '太平盛世', '富贵人']:
            logistics_dict = OrderedDict(
                [('顺丰快递', 0.25),  ('圆通快递', 0.18), ('韵达快递', 0.19),('中通快递', 0.18), ('申通快递', 0.20)])
            logistics_value = fake.random_element(logistics_dict)
        else:
            logistics_dict = OrderedDict(
                [('顺丰快递', 0.11), ('圆通快递', 0.11), ('韵达快递', 0.13), ('中通快递', 0.15), ('申通快递', 0.13),('百世快递', 0.13),('极兔快递', 0.19),('邮政   快递', 0.05)])
            logistics_value = fake.random_element(logistics_dict)
        logistics.append(logistics_value)

        # 23、运单号logistics_num
        logistics_num_value = 'L' + str(fake.random_int(min=100000, max=999999, step=1))
        logistics_num.append(logistics_num_value)

        # 24、运送方式logistics_type
        logistics_type_dict = OrderedDict(
            [('铁路运输', 0.15), ('公路运输', 0.75), ('航空运输', 0.1)])
        logistics_type_value = fake.random_element(logistics_type_dict)
        logistics_type.append(logistics_type_value)

        # 16、预计到达时间estimate_arrival_date
        estimate_arrival_date_value = pay_date_value + timedelta(days=(fake.random_int(min=2, max=5, step=1)))
        estimate_arrival_date.append(estimate_arrival_date_value)

        # 17、实际到达时间actual_arrival_date
        actual_arrival_date_dict = OrderedDict(
            [('-1', 0.04), ('0', 0.80), ('1', 0.1), ('2', 0.05), ('3', 0.005), ('4', 0.005)])
        actual_arrival_date_value = fake.random_element(actual_arrival_date_dict)
        actual_arrival_date_value2 = estimate_arrival_date_value + timedelta(days=(int(actual_arrival_date_value)))
        actual_arrival_date.append(actual_arrival_date_value2)

        # 35、快递反馈logistics_result
        if (actual_arrival_date_value2 - estimate_arrival_date_value).days >= 1:
            logistics_result_value = '延后'
        elif (actual_arrival_date_value2 -estimate_arrival_date_value).days < 0:
            logistics_result_value = '提前'
        else:
            logistics_result_value = '准时'
        logistics_result.append(logistics_result_value)

        # 26、是否退货is_return
        if transaction_status_value == '交易取消': is_return_value = '是'
        else: is_return_value = '否'
        is_return.append(is_return_value)

        # 34、退款原因return_reason
        if transaction_status_value == '交易取消':
            return_reason_dict = OrderedDict(
                [('大小不合适', 0.20), ('不喜欢', 0.30), ('物流太慢', 0.1), ('地址错误', 0.20), ('不想要', 0.1), ('拍错了', 0.1)])
            return_reason_value = fake.random_element(return_reason_dict)
        else:
            return_reason_value = '无'
        return_reason.append(return_reason_value)

        # 11、客户满意度satisfaction
        if transaction_status_value == '交易取消':
            satisfaction_dict = OrderedDict(
                [('无评论', 0.75), ('差评', 0.15), ('中评', 0.1)])
            satisfaction_value = fake.random_element(satisfaction_dict)
        else:
            satisfaction_dict = OrderedDict(
                [('无评论', 0.2), ('差评', 0.05), ('中评', 0.15), ('好评', 0.6)])
            satisfaction_value = fake.random_element(satisfaction_dict)
        satisfaction.append(satisfaction_value)



        data = {
            '订单编号': order_num,
            '品牌': brand,
            '店铺': shop_name,
            '负责人': responser,
            '商品': product_name,
            '颜色': color,
            '客户购买类型': order_type,
            '销量': amount,
            '单价': price,
            '销售额': sales_volume,
            '是否优惠': is_discount,
            '优惠金额': discount,
            '实际单价': real_price,
            '实际付款': real_sales_volume,
            '客户性别': customer_gender,
            '客户年龄': customer_age,
            '会员情况': member_level,
            '是否访问页面': web_visitor,
            '访问页面时长': web_stay,
            '交易状态': transaction_status,
            '商品状态': product_status,
            '收货人姓名': consignee_name,
            '收货人电话': consignee_mobile,
            '发货地址': ship_address,
            '收货地址省份': address_province,
            '收货地址': address,
            '物流公司': logistics,
            '运单号': logistics_num,
            '运送方式': logistics_type,
            '支付时间': pay_date,
            '预计到达时间': estimate_arrival_date,
            '实际到达时间': actual_arrival_date,
            '快递反馈': logistics_result,
            '是否退货': is_return,
            '退款原因': return_reason,
            '客户满意度': satisfaction,
            '出生日期': birthday,
            '品类': product_type,
            '材质': material
        }
    pd.set_option('display.width', None)  # 设置字符显示无限制
    pd.set_option('display.max_rows', None)  # 设置行数显示无限制
    users = pd.DataFrame.from_dict(data)
    # print(users)
    users.to_excel("可视化报告数据集.xlsx", index=True)
    print("\n" + "----------执行结束，万幸----------")

if __name__ == '__main__':
    main()