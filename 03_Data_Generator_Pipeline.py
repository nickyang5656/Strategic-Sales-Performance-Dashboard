# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd     # 数据分析神器，用来创建表格 (DataFrame)
import numpy as np      # 数学计算库，这里主要用它的 random.choice 做加权随机选择
import random           # Python自带的随机库，用于生成随机数
from datetime import datetime, timedelta # 处理日期时间的库，做时间序列必备


# --- 1. 配置参数 (Business Logic) ---
# 完整的定义所有产品，不要省略
products = {
    'P_101': {
        'Name': 'Ivy League Seminar',       # 产品名
        'Category': 'Seminar',              # 大类
        'Sub_Category': 'Professor Class',  # 子类
        'Price': 50000,                     # 单价
        'Base_Cost': 25000,                 # 直接成本
        'Agent_Prob': 0.50,                 # 50% 的概率是通过中介来的
        'Comm_Rate': 0.15                   # 如果有中介，返佣 15%
    },
    'P_102': {
        'Name': 'PhD Research Camp', 
        'Category': 'Mentorship', 
        'Sub_Category': 'PhD', 
        'Price': 30000, 
        'Base_Cost': 9000,  
        'Agent_Prob': 0.30, 
        'Comm_Rate': 0.15
    },
    'P_103': {
        'Name': 'Top 30 App Service', 
        'Category': 'Application', 
        'Sub_Category': 'Undergraduate', 
        'Price': 30000, 
        'Base_Cost': 2000,  
        'Agent_Prob': 0.30, 
        'Comm_Rate': 0.20   
    }
}

# 定义 BD 团队 (新增部分)
employees = {
    'E_001': {'Name': 'Alice (Senior BD)', 'Weight': 0.5}, # Weight=0.5 表示 Alice 能力最强，能拿一半的单
    'E_002': {'Name': 'Bob (BD)', 'Weight': 0.3},          # Bob 拿 30%
    'E_003': {'Name': 'Charlie (Junior BD)', 'Weight': 0.2}# Charlie 拿 20%
}

# 设定总目标
TARGET_REVENUE = 10000000  # 循环结束的条件：我们要生成够 1000 万流水的订单
START_DATE = datetime(2023, 1, 1) # 起始日期
END_DATE = datetime(2024, 12, 31) # 结束日期
DAYS_RANGE = (END_DATE - START_DATE).days # 算出两年总共有多少天 (730天)，用于后面随机选日期

# --- 2. 生成 Fact_Sales ---
sales_data = []      # 创建一个空列表，用来存生成的每一行订单数据
current_revenue = 0  # 计数器，记录当前生成了多少钱，初始化为0
order_id_counter = 1 # 订单编号计数器

# 准备 BD 的 ID 列表和权重列表，供 numpy 使用
bd_ids = list(employees.keys()) # ['E_001', 'E_002', 'E_003']
bd_weights = [employees[k]['Weight'] for k in bd_ids] # [0.5, 0.3, 0.2]

# 定义一个函数：生成带有“季节性”的日期
def get_weighted_date():
    # 1. 先随机选一天
    random_days = random.randint(0, DAYS_RANGE)
    date = START_DATE + timedelta(days=random_days)
    
    # 2. 判断季节性 (模拟业务逻辑：下半年是旺季)
    if date.month in [8, 9, 10, 11, 12]: 
        return date # 如果随机到了旺季，直接保留
    elif random.random() < 0.6: 
        # 如果随机到了淡季(1-7月)，有 60% 的概率“重抽”一次
        # 这是一种变相降低淡季出现概率的算法 (Rejection Sampling)
         random_days = random.randint(0, DAYS_RANGE)
         return START_DATE + timedelta(days=random_days)
    return date # 如果没被重抽，就保留这个淡季日期

print("Generating Sales Data with Employee Attribution...")

# 只要还没凑够 1000 万，就一直生成订单
while current_revenue < TARGET_REVENUE:
    # 1. 随机选产品
    # p=[0.25, 0.15, 0.60] 意思是：25%概率选P101，60%概率选P103(本科申请)
    pid = np.random.choice(['P_101', 'P_102', 'P_103'], p=[0.25, 0.15, 0.60])
    prod_info = products[pid] # 取出该产品的所有属性
    
    # 2. 生成日期 (调用上面的函数)
    date = get_weighted_date()
    
    # 3. 判断是否有中介 (模拟掷骰子)
    # random.random() 生成 0到1 的小数。如果小于 Agent_Prob (比如0.5)，就算有中介
    is_agent = 1 if random.random() < prod_info['Agent_Prob'] else 0
    
    # --- 4. 核心新增：分配归属人 ---
    if is_agent:
        # 如果是中介单，根据权重随机分给某个 BD
        # Alice 权重高，所以更有可能被选中
        emp_id = np.random.choice(bd_ids, p=bd_weights)
    else:
        # 如果是直客单，归属给市场部 (E_000)，不参与 BD 考核
        emp_id = 'E_000'

    # 5. 计算财务数据
    revenue = prod_info['Price']
    cost = prod_info['Base_Cost']
    # 只有 is_agent 为 1 时，才计算返佣金额，否则为 0
    commission = revenue * prod_info['Comm_Rate'] if is_agent else 0
    
    # 6. 把这一单的数据打包存入列表
    sales_data.append([
        f"ORD_{date.year}_{order_id_counter:04d}", # 生成格式如 ORD_2023_0001 的ID
        date.strftime('%Y-%m-%d'), # 转为字符串日期
        pid, emp_id, 1, revenue, cost, is_agent, commission 
    ])
    
    # 累加收入和订单号
    current_revenue += revenue
    order_id_counter += 1

# 循环结束后，把列表转换成 DataFrame (Excel 格式)
df_sales = pd.DataFrame(sales_data, columns=['OrderID', 'Date', 'ProductID', 'EmployeeID', 'Quantity', 'Revenue', 'Service_Cost', 'Is_Agent', 'Commission'])
# 按日期排序，看起来更像真实流水
df_sales = df_sales.sort_values(by='Date').reset_index(drop=True)

# --- 3. 生成 Fact_Targets ---
targets_data = []
current_date = START_DATE # 重置时间，从头开始遍历每一月

print("Generating KPI Targets...")

# 遍历 2023-01 到 2024-12 的每一个月
while current_date <= END_DATE:
    # 将日期格式化为当月1号 (比如 2023-01-01)，因为目标通常是按月定的
    month_str = current_date.strftime('%Y-%m-01') 
    
    # 为每个 BD 生成当月目标
    for eid, info in employees.items():
        # 基础目标逻辑：总目标(1000万) / 24个月 * 个人的权重
        # * 1.1 是为了让目标比实际业绩稍微高一点点 (Stretch Goal)
        bd_market_share = 0.4
        # 修正：考虑到 60% 的业绩是直客(Marketing)的，BD 只能分到 40% 左右
        # 所以目标要乘以 0.4，这样才公平
        base_target = (TARGET_REVENUE / 24) * info['Weight'] * 1.1
        
        # 季节性调整：如果是旺季 (9-12月)，目标要定得更高 (*1.5)
        if current_date.month in [9, 10, 11, 12]:
            monthly_target = base_target * 1.5
        else:
            monthly_target = base_target * 0.8
            
        # round(..., -2) 是把数字取整到百位 (例如 45321 -> 45300)，让目标看起来像人定的
        final_target = round(monthly_target + random.uniform(-5000, 5000), -2)
        
        targets_data.append([month_str, eid, final_target])
    
    # --- 日期推进逻辑 ---
    # 如果是12月，年份+1，月份变1；否则月份+1
    if current_date.month == 12:
        current_date = datetime(current_date.year + 1, 1, 1)
    else:
        current_date = datetime(current_date.year, current_date.month + 1, 1)

df_targets = pd.DataFrame(targets_data, columns=['TargetMonth', 'EmployeeID', 'TargetRevenue'])

# --- 4. 生成 Dim_Employee ---
# 先手动加上“市场部”，因为它不在 employees 字典里
employee_list = [['E_000', 'Marketing Team (Direct)']] 

# 遍历字典，把 BD 加进去
for eid, info in employees.items():
    employee_list.append([eid, info['Name']])

df_employee = pd.DataFrame(employee_list, columns=['EmployeeID', 'EmployeeName'])

# --- 生成 Dim_Product (原理同上) ---
# 使用列表推导式快速把 products 字典转成列表
p_list = [[pid, v['Category'], v['Sub_Category'], v['Name'], v['Price'], v['Base_Cost'], v['Comm_Rate']] for pid, v in products.items()]
df_product = pd.DataFrame(p_list, columns=['ProductID', 'Category', 'Sub_Category', 'ProductName', 'Unit_Price', 'Direct_Cost', 'Commission_Rate'])

# --- 生成 Fact_Expenses ---
expenses_data = []
d = START_DATE
while d <= END_DATE:
    # 下面这两行代码有点复杂，它的作用是：找到当月的最后一天
    # 逻辑：把日期设为28号 -> 加4天(这就到了下个月初) -> 减去那个月的天数 = 当月最后一天
    next_month = d.replace(day=28) + timedelta(days=4)
    month_end = next_month - timedelta(days=next_month.day)
    
    # 存入房租数据 (假设每月记一次账)
    expenses_data.append([month_end.strftime('%Y-%m-%d'), 'Personnel', 'Salary', 150000])
    
    # 让日期跳到下个月1号，准备下一次循环
    d = next_month - timedelta(days=next_month.day - 1)

df_expenses = pd.DataFrame(expenses_data, columns=['Date', 'Category', 'Sub_Category', 'Amount'])

# --- 6. 导出 ---
output_file = 'Erudition_KPI_Simulation.xlsx'
# 使用 ExcelWriter 可以在同一个 Excel 文件里写多个 Sheet
with pd.ExcelWriter(output_file) as writer:
    df_sales.to_excel(writer, sheet_name='Fact_Sales', index=False)   # index=False 表示不要生成 0,1,2... 的索引列
    df_targets.to_excel(writer, sheet_name='Fact_Targets', index=False) 
    df_employee.to_excel(writer, sheet_name='Dim_Employee', index=False)
    df_product.to_excel(writer, sheet_name='Dim_Product', index=False)
    df_expenses.to_excel(writer, sheet_name='Fact_Expenses', index=False)

print(f"Files saved to {output_file}")