import os
import time
from datetime import datetime
import subprocess
import not_def
import pandas as pd
path1 = r"C:\Users\User\Desktop\Test\\" # 图、数据处理
path2 = r"C:\Users\User\Desktop\HK tick data\\" # 市场数据
if os.path.exists(path1) == False:
    path1 = r"F:\Notification Program\Notification Program\\"
if os.path.exists(path2) == False:
    path2 = r"F:\HKex tick data\\"
print('path1', path1)
print('path2', path2)
# input()

# 默认情况下，在交易日运行程序，只存最近一个交易日数据。
# 在非交易日运行，检测缺失数据然后保存
save_mode = 'save latest'
# 可以手动调成保存历史数据
# save_mode = 'save history'

# 定义一个函数来检查今天是否是交易日
def is_trading_day():
    # 周六和周日是非交易日
    # 其他交易日无法自动检测
    return (datetime.today().weekday()+1) <= 5  

if is_trading_day():
    # 设置开始时间为今天的16:01以后
    target_time = datetime.now().replace(
        hour=16, minute=1, second=0, microsecond=0)
    # 循环检查当前时间，如果未到16:09则让程序暂停
    while datetime.now() < target_time:
        # 暂停一段时间
        time.sleep(30)

# Save 'observe' plot output
script_path2 = path1 + r"Observe save output multi 20230904.py"
scripts = [script_path2] # 想要同时运行的脚本列表
for script in scripts:
    print('running', script)
    # 使用subprocess在新的cmd窗口中运行脚本
    subprocess.Popen(f'start cmd /k python "{script}"', shell=True)

# Start
directory = path2 + "09999"  # Check path
hsi_day1 = not_def.hk_index_kline('HSI', period='6', selected_date='')
HSI_df = pd.DataFrame(hsi_day1,columns=[
    "date","open","high","low","close",
    "vol","amount","turnover","last_price"])
HSI_df_2 = HSI_df.copy()[-50:]
HSI_df_2 = HSI_df_2.reset_index(drop=True)
HSI_df_2 = HSI_df_2[HSI_df_2.amount != 0]  # 缺失处理

if save_mode == 'save latest':

    # Save tick data
    script_path1 = path2+ r"savelatest 20230816.py"
    # os.system(f'start cmd /k "python \"{script_path1}\""')
    subprocess.run(f'start cmd /k python "{script_path1}"', shell=True)
    print('running', script_path1)
    time.sleep(360)  # Wait for today's tick data
    last_trade_day = HSI_df_2.date.iloc[-1]
    # Check if today's 09999 data file exist
    def check_exist(directory):
        # 获取今日日期
        ltd = datetime.strptime(last_trade_day, '%Y%m%d').strftime('%Y-%m-%d')
        
        # 构建完整的文件路径
        file_path = os.path.join(directory, f"{ltd}.xlsx")
        
        # 检查文件是否存在
        return os.path.exists(file_path)
        
    while True:
        # 使用函数检查文件
        file_exists = check_exist(directory)
        if file_exists == True:
            break
        else:
            print('最近交易日 %s 数据保存未完成...'%last_trade_day,
                  datetime.now())
            time.sleep(120)

elif save_mode == 'save history': # 不在交易日内
    # 自动保存缺失的历史数据
    script_path3 = path2+ r"savehistory multi.py"
    subprocess.run(f'start cmd /k python "{script_path3}"', shell=True)
    print('running', script_path3)

    date_list = HSI_df_2['date']

    def check_exist(directory, day):
        # 获取今日日期
        check_day = datetime.strptime(day, '%Y%m%d').strftime('%Y-%m-%d')
        
        # 构建完整的文件路径
        file_path = os.path.join(directory, f"{check_day}.xlsx")
        
        # 检查文件是否存在
        return os.path.exists(file_path)
    

    for dat in date_list: # 使用从早向晚的日期顺序，检查到09999数据文件存在为止
        # 使用函数检查文件
        while True:
            file_exists = check_exist(directory, dat)
            if file_exists == True:
                start_date2 = dat
                break
            else:
                print('正在保存历史数据...', datetime.now())
                time.sleep(100)
    
# Run all path2 scripts below
scripts_to_run = [
    
    path2 + r"market cash flow unweighted 20231222.py",
    path2 + r"market cash flow weighted 20231222.py",
    path1 + r"Observe HSTECH 5 lines 230911.py",
    path1 + r"Observe HSI 4 lines 230911.py",
    path1 + r"Observe HSI 4 lines 60 230911.py",
    path1 + r"CbCs BsvV 20230911.py"
    
]

# 使用Spyder runfile指令运行其他脚本
for script_path in scripts_to_run:
    try:
        print('running', script_path)
        subprocess.Popen(f'start cmd /k python "{script_path}"', shell=True)
        time.sleep(10)
    except Exception as e:
        print(script_path)
        print(e)
        # continue

# Run all other scripts
scripts_to_run = [
    path2 + r"stock cash flow 20231103.py",
    path2 + r"stock cash flow 20231103 bs.py",
]

# 使用Spyder runfile指令运行其他脚本
# for script_path in scripts_to_run:
#     try:
#         runfile(script_path)
#     except Exception as e:
#         print(script_path)
#         print(e)
#         continue

for script2 in scripts_to_run:
    # 使用start cmd命令通过subprocess在新的cmd窗口中运行脚本
    subprocess.Popen(f'start cmd /k python "{script2}"', shell=True)
    print('running', script2)
time.sleep(200)

#
scripts_to_run = [
    path1 + r"Observe for BsvV 20231204.py",
]
for script4 in scripts_to_run:
    # 使用start cmd命令通过subprocess在新的cmd窗口中运行脚本
    subprocess.Popen(f'start cmd /k python "{script4}"', shell=True)
    print('running', script4)
