#!/bin/bash
# 智能堆肥检测系统一键部署脚本

echo "🚀 开始部署智能堆肥检测系统..."

# 1. 更新系统
sudo apt update && sudo apt upgrade -y

# 2. 安装Python和必要工具
sudo apt install python3 python3-pip nodejs npm nginx mysql-server git -y

# 3. 克隆项目
git clone https://github.com/你的用户名/smart-compost-detection.git
cd smart-compost-detection

# 4. 安装Python依赖
pip3 install -r requirements.txt
pip3 install gunicorn mysqlclient python-dotenv

# 5. 设置MySQL数据库
sudo mysql << EOF
CREATE DATABASE compost CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'compost_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON compost.* TO 'compost_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
EOF

# 6. 配置环境变量
echo "SECRET_KEY=请在这里放入你的密钥" > compost_system/.env
echo "DEBUG=False" >> compost_system/.env
echo "DB_NAME=compost" >> compost_system/.env
echo "DB_USER=compost_user" >> compost_system/.env
echo "DB_PASSWORD=your_secure_password" >> compost_system/.env

# 7. Django配置
cd compost_system
python3 manage.py migrate
python3 manage.py collectstatic --noinput

# 8. 前端构建
cd ../compost_client
npm install
npm run build

# 9. 配置Nginx
sudo tee /etc/nginx/sites-available/compost << EOF
server {
    listen 80;
    server_name 你的域名.com;

    # 前端静态文件
    location / {
        root /home/ubuntu/smart-compost-detection/compost_client/dist;
        try_files \$uri \$uri/ /index.html;
    }

    # API接口
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }

    # 文件上传
    location /upload/ {
        alias /home/ubuntu/smart-compost-detection/compost_system/upload/;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/compost /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# 10. 设置Gunicorn服务
sudo tee /etc/systemd/system/compost.service << EOF
[Unit]
Description=Compost Detection Django App
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/smart-compost-detection/compost_system
ExecStart=/usr/local/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 compost_system.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable compost
sudo systemctl start compost

echo "✅ 部署完成！请访问：http://你的域名.com"