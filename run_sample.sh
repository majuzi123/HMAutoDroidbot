#!/bin/bash

HAP_FILE="orangeMall.hap"
URL="https://raw.githubusercontent.com/XixianLiang/HarmonyOS_NEXT_apps/master/orangeMall.hap"  # 使用原始链接

# 检查文件是否存在
if [ ! -f "$HAP_FILE" ]; then  # 注意这里的空格
    echo "$HAP_FILE does not exist. Downloading from $URL..."
    
    # 下载文件
    curl -L "$URL" --output "$HAP_FILE"
    
    # 检查下载是否成功
    if [ $? -eq 0 ]; then
        echo "$HAP_FILE downloaded successfully."
    else
        echo "Failed to download $HAP_FILE."
    fi
else
    echo "$HAP_FILE already exists."
fi

# 获取目标设备的序列号（假定只连接 1 个设备）
OUTPUT=$(hdc.exe list targets)
TARGET=$(echo "$OUTPUT" | grep -oP '\b[0-9A-F]{16}\b')
echo "$TARGET"

if [ -z "$TARGET" ]; then
    echo "Device not found. Exiting."
    exit 1
fi

echo "Starting droidbot with device $TARGET"
python3 -m droidbot.start -a `pwd`/$HAP_FILE -t $TARGET -o output -count 1000 -is_harmonyos
