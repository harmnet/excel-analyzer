import random
import string
import pandas as pd


def generate_random_data():
    data = []
    for _ in range(1000):
        养殖数量 = random.randint(0, 500)
        圈舍面积 = int(养殖数量 * 20) if 养殖数量 > 0 else random.randint(0, 10000)

        前一年养殖收入 = random.randint(1000, 100000) + 养殖数量 * 10000
        if 前一年养殖收入 > 5000000:
            前一年养殖收入 = 5000000

        前两年养殖收入 = int(前一年养殖收入 * random.uniform(1.8, 2.2))
        前三年养殖收入 = int(前一年养殖收入 * random.uniform(2.8, 3.2))

        前一年养殖投入 = int(前一年养殖收入 * random.uniform(0.4, 0.6))
        前两年养殖投入 = int(前两年养殖收入 * random.uniform(0.4, 0.6))
        前三年养殖投入 = int(前三年养殖收入 * random.uniform(0.4, 0.6))

        是否与贷款逾期 = random.choice(["是", "否"])
        贷款余额 = random.randint(0, 1000000) if 是否与贷款逾期 == "是" else 0

        是否有民间借贷 = random.choice(["是", "否"])
        民间借贷余额 = random.randint(0, 1000000) if 是否有民间借贷 == "是" else 0

        是否有对外担保 = random.choice(["是", "否"])
        对外担保余额 = random.randint(0, 1000000) if 是否有对外担保 == "是" else 0

        是否有畜牧保险 = random.choice(["是", "否"])
        年金保险额度 = random.randint(0, 1000000) if 是否有畜牧保险 == "是" else 0

        是否享有政策补贴 = random.choice(["是", "否"])
        补贴金额 = random.randint(0, 200000) if 是否享有政策补贴 == "是" else 0

        user_data = {
            "用户姓名": ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)),
            "婚姻情况": random.choice(["已婚", "未婚"]),
            "性别": random.choice(["男", "女"]),
            "年龄": random.randint(18, 99),
            "民族": random.choice(["汉族", "满族", "回族", "藏族", "维吾尔族"]),
            "身份证号": ''.join(random.choices(string.digits, k=18)),
            "电话号": ''.join(random.choices(string.digits, k=11)),
            "家庭住址": ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
            "教育程度": random.choice(["小学", "初中", "高中", "大专", "本科", "研究生"]),
            "家庭其他收入": random.randint(0, 100000),
            "家庭其他支出": random.randint(0, 100000),
            "养殖种类": random.choice(["肉牛", "奶牛", "肉羊", "绵阳", "肉猪"]),
            "养殖数量": 养殖数量,
            "圈舍面积": 圈舍面积,
            "前一年养殖收入": 前一年养殖收入,
            "前两年养殖收入": 前两年养殖收入,
            "前三年养殖收入": 前三年养殖收入,
            "前一年养殖投入": 前一年养殖投入,
            "前两年养殖投入": 前两年养殖投入,
            "前三年养殖投入": 前三年养殖投入,
            "房屋面积": random.randint(0, 200),
            "家庭其他固定资产": random.choice(["小轿车", "摩托车", "拖拉机", "养殖设备", "货运车辆"]),
            "农机具价值": random.randint(0, 5000000),
            "贷款余额": 贷款余额,
            "是否与贷款逾期": 是否与贷款逾期,
            "是否有民间借贷": 是否有民间借贷,
            "民间借贷余额": 民间借贷余额,
            "是否有对外担保": 是否有对外担保,
            "对外担保余额": 对外担保余额,
            "是否有稳定销售渠道": random.choice(["是", "否"]),
            "是否现款结算": random.choice(["是", "否"]),
            "延期付款周期": f"{random.randint(1, 24)}个月" if random.choice([True, False]) else "0个月",
            "是否有畜牧保险": 是否有畜牧保险,
            "年金保险额度": 年金保险额度,
            "养殖年限": random.randint(0, 50),
            "家庭劳动力人数": random.randint(0, 5),
            "家庭供养人数": random.randint(0, 5),
            "是否享有政策补贴": 是否享有政策补贴,
            "补贴金额": 补贴金额
        }
        data.append(user_data)

    pd.set_option('display.width', None)  # 设置字符显示无限制
    pd.set_option('display.max_rows', None)  # 设置行数显示无限制
    users = pd.DataFrame.from_dict(data)
    # print(users)
    users.to_csv("customer_info.xlsx", index=True)  # 指定生成文件的名字和格式

    # df = pd.DataFrame(data)
    # df.to_csv('长春金专国赛数据.csv', index=False)
    # print(df.head())  # 添加此行以打印导出的数据前几行
