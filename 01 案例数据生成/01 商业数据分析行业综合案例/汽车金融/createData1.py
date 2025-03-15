"""
        集市区域界面中销量和渗透率指标
        Created By：段小飞
        Created Time：2022-12-16
"""
import pandas as pd
from datetime import date
from faker import Faker
from collections import OrderedDict
from tqdm import tqdm

# 主函数：生成数据
def main():
    # 初始化设置
    fake = Faker('zh-CN')  # 指定用中文
    num = 100  # 初始化模拟数据生成数量
    """ 初始化客户标签字段集以及字段对应的数据字典 """
    sale_date = []                  # 1、销售日期
    area = []                       # 2、所在区域
    channel = []                    # 3、所属渠道
    jigou = []                      # 4、所属机构
    sale_number = []                # 5、销售数量
    is_loan = []                    # 6、是否贷款销售
    chexi = []                      # 7、销售车系
    chexing = []                    # 8、销售车型
    product_type = []               # 9、产品分类
    product_childtype = []          # 10、产品分类子类
    sales_amount = []               # 11、营业收入
    down_payment_proportion = []    # 12、首付比例
    loan_amount = []                # 13、贷款/放款金额
    loan_term = []                  # 14、贷款/放款期限
    operating_profit = []           # 15、营业利润
    sale_type = []                  # 16、出售类型
    total_aset = []                 # 17、总资产
    mubiao = []                     # 18、目标融资金额
    tax = []                        # 19、所得税
    liudong_aset = []               # 20、流动资产


    print("----------开始生成数据，祈祷不报错----------")
    for i in tqdm(range(0, num)):
        """  按照设定的生成数据数量，逐一生成数据  """
        # 1、销售日期 sale_date
        sale_date_value = fake.date_time_between(start_date=date(2017, 4, 1), end_date=date(2020, 12, 31))
        sale_date.append(sale_date_value)
        # 2、所在区域 area
        area_dict = OrderedDict([('华南A', 0.10), ('东北', 0.07), ('华北A', 0.09), ('华南B', 0.10), ('华东', 0.10), ('华北B', 0.09),
                                 ('西北', 0.08), ('西南', 0.10), ('华中', 0.09), ('华南C', 0.08), ('东北黑吉', 0.05), ('东北辽宁', 0.05)
                                 ])  # 数据字典：所在区域
        areaValue = fake.random_element(area_dict)
        area.append(areaValue)
        # 3、所属渠道 channel
        channel_dict = OrderedDict([('TMCI', 0.35), ('GTMS', 0.25), ('FTMS', 0.18), ('ZG', 0.12), ('JMS', 0.10)])  # 数据字典：所属渠道
        channelValue = fake.random_element(channel_dict)
        channel.append(channelValue)
        # 4、所属机构 jigou
        jigou_dict = OrderedDict([('TMB', 0.35), ('TMA', 0.65)])  # 数据字典：所属机构
        jigouValue = fake.random_element(jigou_dict)
        jigou.append(jigouValue)
        # 5、销售数量 sale_number
        sale_number_value = '1'
        sale_number.append(sale_number_value)
        # 6、是否贷款销售 is_loan
        is_loan_dict = OrderedDict([('是', 0.25), ('否', 0.75)])  # 数据字典：所属机构
        is_loanValue = fake.random_element(is_loan_dict)
        is_loan.append(is_loanValue)
        # 7、销售车系 chexi
        chexi_dict = OrderedDict([('RAV4', 0.12), ('AVALON', 0.09), ('CAMRY', 0.12), ('C-HR', 0.10), ('COROLLA', 0.15),('ES', 0.10), ('HIGHLANDER', 0.10), ('PRADO', 0.05), ('RX', 0.08), ('NX', 0.09)])  # 数据字典：销售车系
        chexiValue = fake.random_element(chexi_dict)
        chexi.append(chexiValue)
        # 8、销售车型 chexing
        if chexiValue == 'RAV4':
            chexing_dict = OrderedDict([('RAV4', 0.90), ('RAV4 HEV', 0.05), ('RAV4 PHEV', 0.05)])  # 数据字典：销售车型
            chexing_value = fake.random_element(chexing_dict)
        elif chexiValue == 'AVALON':
            chexing_dict = OrderedDict([('AVALON', 0.65), ('AVALON HEV', 0.35)])  # 数据字典：销售车型
            chexing_value = fake.random_element(chexing_dict)
        elif chexiValue == 'CAMRY':
            chexing_dict = OrderedDict([('CAMRY', 0.55), ('CAMRY HEV', 0.45)])  # 数据字典：销售车型
            chexing_value = fake.random_element(chexing_dict)
        elif chexiValue == 'C-HR':
            chexing_dict = OrderedDict([('C-HR', 0.50), ('C-HR HEV', 0.35), ('C-HR EV', 0.15)])  # 数据字典：销售车型
            chexing_value = fake.random_element(chexing_dict)
        elif chexiValue == 'COROLLA':
            chexing_dict = OrderedDict([('COROLLA', 0.30), ('COROLLA EX', 0.10), ('COROLLA X', 0.10), ('COROLLA CROSS', 0.10), ('COROLLA HEV', 0.35), ('COROLLA PHEV', 0.05)])  # 数据字典：销售车型
            chexing_value = fake.random_element(chexing_dict)
        elif chexiValue == 'ES':
            chexing_dict = OrderedDict([('ES 200', 0.50), ('ES 250', 0.01), ('ES 260', 0.15), ('ES 350', 0.01), ('ES 300h', 0.33)])  # 数据字典：销售车型
            chexing_value = fake.random_element(chexing_dict)
        elif chexiValue == 'HIGHLANDER':
            chexing_dict = OrderedDict([('HIGHLANDER', 0.85), ('HIGHLANDER HEV', 0.15)])  # 数据字典：销售车型
            chexing_value = fake.random_element(chexing_dict)
        elif chexiValue == 'PRADO':
            chexing_dict = OrderedDict([('PRADO', 0.50), ('PRADO CBU', 0.35), ('PRADO CKD', 0.15)])  # 数据字典：销售车型
            chexing_value = fake.random_element(chexing_dict)
        elif chexiValue == 'RX':
            chexing_dict = OrderedDict([('RX 300', 0.40), ('RX 200T', 0.01), ('RX 270', 0.01), ('RX 350', 0.01), ('RX 450h', 0.33), ('RX 450hL', 0.24)])  # 数据字典：销售车型
            chexing_value = fake.random_element(chexing_dict)
        elif chexiValue == 'NX':
            chexing_dict = OrderedDict([('NX 200', 0.10), ('NX 300', 0.35), ('NX 260', 0.15), ('NX 200T', 0.01), ('NX 300h', 0.39)])  # 数据字典：销售车型
            chexing_value = fake.random_element(chexing_dict)
        else:
            chexing_value = '无'
        chexing.append(chexing_value)
        # 9、产品分类 product_type
        product_type_dict = OrderedDict([('非贴息', 0.55), ('员工产品', 0.02), ('贴息', 0.43)])  # 数据字典：产品分类
        product_typeValue = fake.random_element(product_type_dict)
        product_type.append(product_typeValue)
        # 10、产品分类子类 product_childtype
        if product_typeValue == '非贴息':
            product_childtypeValue = '非贴息'
        elif product_typeValue == '员工产品':
            product_childtypeValue = '员工产品'
        else:
            product_childtype_dict = OrderedDict([('厂商贴息', 0.35), ('承销商经销商联合贴息', 0.35), ('经销商贴息', 0.20), ('承销商贴息', 0.10)])  # 数据字典：产品分类子类
            product_childtypeValue = fake.random_element(product_childtype_dict)
        product_childtype.append(product_childtypeValue)
        # 11、营业收入 sales_amount
        if chexiValue == 'RAV4':
            if chexing_value == 'RAV4':
                sales_amount_dict = OrderedDict([('17.58', 0.20), ('19.58', 0.25), ('20.08', 0.25), ('20.68', 0.15), ('21.18', 0.10), ('22.88', 0.05)])  # 数据字典：销售金额
                sales_amount_value = fake.random_element(sales_amount_dict)
            elif chexing_value == 'RAV4 HEV':
                sales_amount_dict = OrderedDict([('22.58', 1)])  # 数据字典：销售金额
                sales_amount_value = fake.random_element(sales_amount_dict)
            elif chexing_value == 'RAV4 PHEV':
                sales_amount_dict = OrderedDict([('24.38', 0.20), ('26.08', 0.25)])  # 数据字典：销售金额
                sales_amount_value = fake.random_element(sales_amount_dict)
        elif chexiValue == 'AVALON':
            if chexing_value == 'AVALON':
                sales_amount_dict = OrderedDict(
                    [('19.98', 0.20), ('21.78', 0.25), ('22.88', 0.25), ('20.88', 0.15), ('22.68', 0.10),
                     ('24.48', 0.05)])  # 数据字典：销售金额
                sales_amount_value = fake.random_element(sales_amount_dict)
            elif chexing_value == 'AVALON HEV':
                sales_amount_dict = OrderedDict([('23.98', 0.50), ('25.78', 0.30), ('27.98', 0.20)])  # 数据字典：销售金额
                sales_amount_value = fake.random_element(sales_amount_dict)
        elif chexiValue == 'CAMRY':
            if chexing_value == 'CAMRY':
                sales_amount_dict = OrderedDict(
                    [('17.98', 0.20), ('19.98', 0.25), ('20.78', 0.25), ('21.98', 0.15), ('22.18', 0.10),
                     ('23.48', 0.05)])  # 数据字典：销售金额
                sales_amount_value = fake.random_element(sales_amount_dict)
            elif chexing_value == 'CAMRY HEV':
                sales_amount_dict = OrderedDict([('20.98', 0.50), ('23.98', 0.30), ('26.98', 0.20)])  # 数据字典：销售金额
                sales_amount_value = fake.random_element(sales_amount_dict)
        elif chexiValue == 'C-HR':
            if chexing_value == 'C-HR':
                sales_amount_dict = OrderedDict([('14.18', 0.50), ('15.18', 0.30), ('15.68', 0.20)])  # 数据字典：销售金额
                sales_amount_value = fake.random_element(sales_amount_dict)
            elif chexing_value == 'C-HR HEV':
                sales_amount_dict = OrderedDict([('16.98', 0.60), ('17.48', 0.40)])  # 数据字典：销售金额
                sales_amount_value = fake.random_element(sales_amount_dict)
            elif chexing_value == 'C-HR EV':
                sales_amount_dict = OrderedDict([('22.58', 0.40), ('22.88', 0.20), ('23.28', 0.20), ('24.58', 0.10), ('24.98', 0.10)])  # 数据字典：销售金额
                sales_amount_value = fake.random_element(sales_amount_dict)
        elif chexiValue == 'COROLLA':
            if chexing_value == 'COROLLA':
                sales_amount_dict = OrderedDict([('10.98', 0.50), ('11.98', 0.30), ('12.28', 0.20)])  # 数据字典：销售金额
                sales_amount_value = fake.random_element(sales_amount_dict)
            elif chexing_value == 'COROLLA HEV':
                sales_amount_dict = OrderedDict([('13.58', 1)])  # 数据字典：销售金额
                sales_amount_value = fake.random_element(sales_amount_dict)
            else:
                sales_amount_dict = OrderedDict([('21.48', 1)])  # 数据字典：销售金额
                sales_amount_value = fake.random_element(sales_amount_dict)
        elif chexiValue == 'ES':
            if chexing_value == 'ES 200':
                sales_amount_dict = OrderedDict([('29.69', 0.65), ('31.59', 0.35)])  # 数据字典：销售金额
                sales_amount_value = fake.random_element(sales_amount_dict)
            elif chexing_value == 'ES 250':
                sales_amount_dict = OrderedDict([('35.49', 0.20)])  # 数据字典：销售金额
                sales_amount_value = fake.random_element(sales_amount_dict)
            elif chexing_value == 'ES 260':
                sales_amount_dict = OrderedDict([('35.49', 0.50), ('39.79', 0.30), ('41.49', 0.20)])  # 数据字典：销售金额
                sales_amount_value = fake.random_element(sales_amount_dict)
            elif chexing_value == 'ES 350':
                sales_amount_dict = OrderedDict([('42.39', 0.20)])  # 数据字典：销售金额
                sales_amount_value = fake.random_element(sales_amount_dict)
            elif chexing_value == 'ES 300h':
                sales_amount_dict = OrderedDict([('37.99', 0.50), ('43.69', 0.30), ('48.89', 0.20)])  # 数据字典：销售金额
                sales_amount_value = fake.random_element(sales_amount_dict)
        elif chexiValue == 'HIGHLANDER':
            if chexing_value == 'HIGHLANDER':
                sales_amount_dict = OrderedDict(
                    [('26.88', 0.20), ('27.48', 0.25), ('31.88', 0.25), ('32.98', 0.15), ('34.88', 0.10),('36.48', 0.05)])  # 数据字典：销售金额
                sales_amount_value = fake.random_element(sales_amount_dict)
            elif chexing_value == 'HIGHLANDER HEV':
                sales_amount_dict = OrderedDict([('31.48', 0.50), ('32.58', 0.30), ('34.48', 0.20)])  # 数据字典：销售金额
                sales_amount_value = fake.random_element(sales_amount_dict)
        elif chexiValue == 'PRADO':
            if chexing_value == 'PRADO':
                sales_amount_dict = OrderedDict(
                    [('49.48', 0.55), ('50.48', 0.45)])  # 数据字典：销售金额
                sales_amount_value = fake.random_element(sales_amount_dict)
            else:
                sales_amount_dict = OrderedDict([('49.80', 0.50), ('55.88', 0.30), ('61.38', 0.20)])  # 数据字典：销售金额
                sales_amount_value = fake.random_element(sales_amount_dict)
        elif chexiValue == 'RX':
            if chexing_value == 'RX 300':
                sales_amount_dict = OrderedDict([('50.90', 0.65), ('53.60', 0.35)])  # 数据字典：销售金额
                sales_amount_value = fake.random_element(sales_amount_dict)
            elif chexing_value == 'RX 450h':
                sales_amount_dict = OrderedDict([('65.70', 0.65), ('70.20', 0.35)])  # 数据字典：销售金额
                sales_amount_value = fake.random_element(sales_amount_dict)
            elif chexing_value == 'RX 450hL':
                sales_amount_dict = OrderedDict([('75.60', 1)])  # 数据字典：销售金额
                sales_amount_value = fake.random_element(sales_amount_dict)
            else:
                sales_amount_dict = OrderedDict([('40.50', 0.50), ('44.20', 0.30), ('58.50', 0.20)])  # 数据字典：销售金额
                sales_amount_value = fake.random_element(sales_amount_dict)
        elif chexiValue == 'NX':
            if chexing_value == 'NX 260':
                sales_amount_dict = OrderedDict([('31.88', 0.65), ('40.58', 0.35)])  # 数据字典：销售金额
                sales_amount_value = fake.random_element(sales_amount_dict)
            elif chexing_value == 'NX 300h':
                sales_amount_dict = OrderedDict([('35.58', 0.65), ('48.58', 0.35)])  # 数据字典：销售金额
                sales_amount_value = fake.random_element(sales_amount_dict)
            else:
                sales_amount_dict = OrderedDict([('32.88', 0.50), ('33.58', 0.30), ('41.38', 0.20)])  # 数据字典：销售金额
                sales_amount_value = fake.random_element(sales_amount_dict)
        else:
            sales_amount_value = '0'
        sales_amount.append(sales_amount_value)
        # 12、首付比例 down_payment_proportion
        if is_loanValue == '是':
            down_payment_proportion_dict = OrderedDict([('0.3', 0.60), ('0.2', 0.30), ('0.1', 0.10)])  # 数据字典：销售金额
            down_payment_proportion_value = fake.random_element(down_payment_proportion_dict)
        else:
            down_payment_proportion_value = '0'
        down_payment_proportion.append(down_payment_proportion_value)
        # 13、贷款/放款金额 loan_amount
        if is_loanValue == '是':
            loan_amount_value = float(sales_amount_value) * (1-float(down_payment_proportion_value))
        elif is_loanValue == '否':
            loan_amount_value = '0'
        loan_amount.append(loan_amount_value)
        # 14、贷款/放款期限 loan_term
        if is_loanValue == '是':
            loan_term_dict = OrderedDict([('36', 0.60), ('24', 0.30), ('12', 0.10)])  # 数据字典：销售金额
            loan_term_value = fake.random_element(loan_term_dict)
        else:
            loan_term_value = '0'
        loan_term.append(loan_term_value)
        # 15、营业利润 operating_profit
        profit_rate = fake.random_int(min=10, max=40)
        operating_profit_value = (float(sales_amount_value)*float(profit_rate)/100-float(loan_amount_value)*0.03)
        operating_profit.append(operating_profit_value)
        # 16、出售类型 sale_type
        sale_type_dict = OrderedDict([('零售资产', 0.55), ('库存资产', 0.02), ('租赁资产', 0.43)])  # 数据字典：出售类型
        sale_typeValue = fake.random_element(sale_type_dict)
        sale_type.append(sale_typeValue)
        # 17、总资产 total_aset
        asetRate = fake.random_int(min=100, max=199)
        total_aset_value = asetRate/100 * float(sales_amount_value)
        total_aset.append(total_aset_value)
        # 18、目标融资金额 mubiao
        mubiao_value = float(sales_amount_value) * 0.7
        mubiao.append(mubiao_value)
        # 19、所得税 tax
        tax_value = float(sales_amount_value) * 0.25
        tax.append(tax_value)
        # 20、流动资产 liudong_aset
        liudongasetRate = fake.random_int(min=40, max=60)
        liudong_aset_value = total_aset_value * liudongasetRate/100
        liudong_aset.append(liudong_aset_value)

        data = {
            '销售日期': sale_date,
            '所在区域': area,
            '所属渠道': channel,
            '所属机构': jigou,
            '销售数量': sale_number,
            '是否贷款销售': is_loan,
            '销售车系': chexi,
            '销售车型': chexing,
            '产品分类': product_type,
            '产品分类子类': product_childtype,
            '营业收入': sales_amount,
            '首付比例': down_payment_proportion,
            '贷款/放款金额': loan_amount,
            '贷款/放款期限': loan_term,
            '营业利润': operating_profit,
            '出售类型': sale_type,
            '总资产': total_aset,
            '目标融资金额': mubiao,
            '所得税': tax,
            '流动资产': liudong_aset
        }
    pd.set_option('display.width', None)  # 设置字符显示无限制
    pd.set_option('display.max_rows', None)  # 设置行数显示无限制
    users = pd.DataFrame.from_dict(data)
    print(users)
    # users.to_csv("qichejinrong.xlsx", index=True)
    print("\n" + "----------执行结束，万幸----------")

if __name__ == '__main__':
    main()