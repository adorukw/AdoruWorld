#!/bin/bash

# 前端构建
# cd /home/adorukw/AAAPAN/Project/AdoruWorld/client
npm run build

# 复制 dist 到 nginx 目录（先清空旧的再复制）
sudo rm -rf /var/www/adoru-world/*
sudo cp -r dist/* /var/www/adoru-world/

echo "✅ 部署完成！"