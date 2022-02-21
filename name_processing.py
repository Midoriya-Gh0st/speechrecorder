import os
import sys

dir_path = sys.argv[1]
print("Dir Path:", dir_path)

files = []
for f in os.listdir(dir_path):
    files.append(f)

print("files name:", files)

for f in files:
    forename = f.split('.')[0][0: -2]  # 获取后缀名前的名字, 并去掉"标号"
    name = forename + ".wav"  # 新的名字
    file_path = dir_path + "\\"
    os.rename(file_path + f, file_path + name)
