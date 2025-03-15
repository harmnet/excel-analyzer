"""
        Created By：段小飞
        Created Time：2024-05-23
"""
import random
import pandas as pd
from datetime import date,datetime,timedelta
from faker import Faker
from collections import OrderedDict
from time import sleep
from tqdm import tqdm

# 主函数：生成数据
def main():
    # 初始化设置
    fake = Faker('zh-CN')  # 指定用中文
    num = 10000  # 初始化模拟数据生成数量

    user_id = []                        # 1、用户ID
    user_name = []                      # 2、姓名
    sex = []                            # 3、性别
    mobile = []                         # 4、手机号码
    age = []                            # 5、年龄
    career = []                         # 6、职业
    education = []                      # 7、教育程度
    create_time = []                    # 8、开户时间
    marrage = []                        # 9、婚姻状况
    children = []                       # 10、子女数量
    sallery = []                        # 11、收入水平
    money_left = []                     # 12、账户余额
    save_times = []                     # 13、近一年的存款次数
    save_amount = []                    # 14、近一年均次存款金额（元/次）
    level = []                          # 15、风险承受等级
    yanglao = []                        # 16、养老意识
    ifbuy = []                          # 17、是否购买金融产品

    print("----------开始生成数据，祈祷不报错----------")
    j = 0
    for i in tqdm(range(0, num)):
        j = j+1
        """  按照设定的生成数据数量，逐一生成数据  """
        # 1、用户ID：user_id
        user_id_value = j
        user_id.append(user_id_value)

        # 3、性别：sex
        sex_dict = OrderedDict([('男', 0.58), ('女', 0.42)])
        sex_value = fake.random_element(sex_dict)
        sex.append(sex_value)

        # 2、姓名：user_name
        if sex_value == '男':
            user_name_value = fake.name_male()
        elif sex_value == '女':
            user_name_value = fake.name_female()
        user_name.append(user_name_value)

        # 4、手机号：mobile
        moble_value = fake.phone_number()
        mobileResult = str(moble_value[0:3]) + '****' + str(moble_value[7:11])
        mobile.append(mobileResult)

        # 5、年龄：age
        age_value = fake.random_int(min=30, max=65)
        age.append(age_value)

        # 6、职业：career
        career_list = ['行政主管', '企业主管', '职业经理人', '工程师', '会计师', '律师', '架构师', '高级程序员',
                        '项目经理', '公证员', '策划师', '教师', '医师', '设计师', '记者',
                        '销售代表', '采购员',  '财务经理',
                        '保安', '前台接待员', '仓库管理员', '餐饮服务员', '快递员']
        career_value = ','.join([str(s) for s in random.sample(career_list, 1)])
        career.append(career_value)

        # 7、教育程度：education
        if career_value in ['行政主管', '企业主管', '职业经理人', '工程师', '会计师', '律师', '架构师', '高级程序员',
                        '项目经理', '公证员', '策划师', '教师', '医师', '设计师', '记者']:
            education_dict = OrderedDict([('专科', 0.21), ('本科', 0.62), ('硕士', 0.12), ('博士', 0.05)])
        elif career_value in ['销售代表', '采购员',  '财务经理']:
            education_dict = OrderedDict([('专科', 0.42), ('本科', 0.48), ('硕士', 0.08), ('博士', 0.02)])
        else:
            education_dict = OrderedDict([('专科', 0.65), ('本科', 0.35)])
        education_value = fake.random_element(education_dict)
        education.append(education_value)

        # 8、开户时间：create_time
        start_date = datetime(2023,1,1)
        end_date = datetime(2023,12,31)
        create_time_value = fake.date_between(start_date=start_date, end_date=end_date)
        create_time.append(create_time_value)

        # 9、婚姻状况：marrage
        marrage_dict = OrderedDict([('未婚', 0.15), ('已婚', 0.60), ('离异', 0.25)])
        marrage_value = fake.random_element(marrage_dict)
        marrage.append(marrage_value)

        # 10、子女数量：children
        if marrage_value == '未婚':
            children_value = '0'
        elif marrage_value == '已婚':
            children_dict = OrderedDict([('0', 0.05), ('1', 0.75), ('2', 0.15), ('3', 0.05)])
            children_value = fake.random_element(children_dict)
        else:
            children_dict = OrderedDict([('0', 0.05), ('1', 0.85), ('2', 0.1)])
            children_value = fake.random_element(children_dict)
        children.append(children_value)

        # 11、收入水平：sallery
        if career_value in ['行政主管', '企业主管', '职业经理人', '工程师', '会计师', '律师', '架构师', '高级程序员',
                        '项目经理', '公证员', '策划师', '教师', '医师', '设计师', '记者']:
            sallery_value = OrderedDict([('36万以上', 0.1), ('20.4万-36万', 0.3), ('9.6万-20.4万', 0.6)])
        elif career_value in ['销售代表', '采购员',  '财务经理']:
            sallery_value = OrderedDict([('20.4万-36万', 0.1), ('9.6万-20.4万', 0.75), ('9.6万以下', 0.15)])
        else:
            sallery_value = OrderedDict([('9.6万-20.4万', 0.25), ('9.6万以下', 0.75)])
        sallery_value = fake.random_element(sallery_value)
        sallery.append(sallery_value)

        # 12、账户余额：money_left
        if career_value in ['行政主管', '企业主管', '职业经理人', '工程师', '会计师', '律师', '架构师', '高级程序员',
                        '项目经理', '公证员', '策划师', '教师', '医师', '设计师', '记者']:
            money_left_value = fake.random_int(min=10000, max=200000)
        elif career_value in ['销售代表', '采购员',  '财务经理']:
            money_left_value = fake.random_int(min=5000, max=100000)
        else:
            money_left_value = fake.random_int(min=1000, max=70000)
        money_left.append(money_left_value)

        # 13、近一年的存款次数：save_times
        save_times_value = fake.random_int(min=0, max=12)
        save_times.append(save_times_value)

        # 14、近一年均次存款金额（元/次）：save_amount
        save_amount_value = fake.random_int(min=3000, max=20000)
        save_amount.append(save_amount_value)

        # 15、风险承受等级：level
        level_dict = OrderedDict([('R1', 0.2), ('R2', 0.2), ('R3', 0.2), ('R4', 0.2), ('R5', 0.2)])
        level_value = fake.random_element(level_dict)
        level.append(level_value)

        # 16、养老意识：yanglao
        yanglao_dict = OrderedDict([('高度关注', 0.2), ('一般关注', 0.5), ('不关注', 0.3)])
        yanglao_value = fake.random_element(yanglao_dict)
        yanglao.append(yanglao_value)

        # 17、是否购买金融产品：ifbuy
        ifbuy_dict = OrderedDict([('是', 0.2), ('否', 0.8)])
        ifbuy_value = fake.random_element(ifbuy_dict)
        ifbuy.append(ifbuy_value)

        data = {
            '用户ID': user_id,
            '姓名': user_name,
            '性别': sex,
            '手机号码': mobile,
            '年龄': age,
            '职业': career,
            '教育程度': education,
            '开户时间': create_time,
            '婚姻状况': marrage,
            '子女数量': children,
            '收入水平': sallery,
            '账户余额': money_left,
            '近一年的存款次数': save_times,
            '近一年均次存款金额（元/次）': save_amount,
            '风险承受等级': level,
            '养老意识': yanglao,
            '是否购买金融产品': ifbuy
        }

    # print(data)
    pd.set_option('display.width', None)  # 设置字符显示无限制
    pd.set_option('display.max_rows', None)  # 设置行数显示无限制
    users = pd.DataFrame.from_dict(data)
    # print(users)
    users.to_csv("dw_user.xlsx", index=True)
    print("\n" + "----------执行结束，万幸----------")

if __name__ == '__main__':
    main()