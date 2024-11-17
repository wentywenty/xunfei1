#!/usr/bin/env python3
import re
import subprocess
import csv

# 定义正则表达式来匹配目标信息
goal_pattern = re.compile(
    # 填写你的正则表达式
)

# 定义正则表达式来匹配 /initialpose 信息
initialpose_pattern = re.compile(
    # 填写你的正则表达式
)

# 启动 rviz 并捕获其输出
rviz_config_path = 'sbrviz.rviz'
with open('sbrviz.txt', 'w') as rviz_output_file, open('sbrviz.csv', 'a', newline='') as csvfile:
    process = subprocess.Popen(['stdbuf', '-oL', 'rviz', '-d', rviz_config_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    csv_writer = csv.writer(csvfile)

    try:
        while True:
            # 从 rviz 捕获输出
            output = process.stdout.readline()
            if output:
                # 将输出写入文件
                rviz_output_file.write(output)
                rviz_output_file.flush()
                print(output.strip())

                # 匹配 goal_pattern
                match_goal = goal_pattern.search(output)
                if match_goal:
                    values = match_goal.groups()
                    position_x = values[0]
                    position_y = values[1]
                    orientation_z = values[5]
                    orientation_w = values[6]

                    # 构建要发送的数据
                    data = f"{position_x},{position_y},{orientation_z},{orientation_w}\n" 
                    print(f"Sent goal data: {data.strip()}")

                    # 将数据写入 CSV 文件
                    csv_writer.writerow([position_x, position_y, orientation_z, orientation_w])
                    csvfile.flush()
                    print(f"Written to CSV: {data.strip()}")

                # 匹配 initialpose_pattern
                match_initialpose = initialpose_pattern.search(output)
                if match_initialpose:
                    values = match_initialpose.groups()
                    position_x = values[0]
                    position_y = values[1]
                    orientation_z = values[2]

                    # 构建要发送的数据
                    data = f"{position_x},{position_y},{orientation_z}\n"
                    print(f"Sent initialpose data: {data.strip()}")

                    # 将数据写入 CSV 文件
                    csv_writer.writerow([position_x, position_y, orientation_z])
                    csvfile.flush()
                    print(f"Written to CSV: {data.strip()}")

    except KeyboardInterrupt:
        print("Process interrupted.")
    finally:
        process.terminate()
