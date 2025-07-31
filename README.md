# 🌱 智能堆肥成熟度检测系统

基于深度学习的农业智能化解决方案，通过图像识别技术自动判断堆肥成熟度。

## 📋 项目概述

本系统采用深度学习技术，结合Web应用框架，为农业生产提供智能化的堆肥成熟度检测服务。用户只需上传堆肥图像，系统即可自动判断成熟度并给出置信度评分。

## ✨ 主要功能

- 🔍 **智能图像识别**: 基于ResNet18的深度学习模型，准确识别堆肥成熟状态
- 📊 **数据可视化**: 实时展示检测历史、用户统计等多维度数据
- 👥 **用户管理系统**: 支持管理员和普通用户角色管理
- 📱 **响应式界面**: 现代化Web界面，支持桌面端和移动端
- 📈 **检测记录**: 完整的检测历史记录和数据导出功能
- ⚡ **实时预测**: 毫秒级响应速度

## 🛠️ 技术栈

### 后端
- **Python 3.8+**
- **Django 5.2.4** - Web框架
- **PyTorch** - 深度学习框架
- **torchvision** - 计算机视觉库
- **Pillow** - 图像处理

### 前端
- **Vue.js 3** - 前端框架
- **Element Plus** - UI组件库
- **ECharts** - 数据可视化
- **Vite** - 构建工具

### AI模型
- **ResNet18** - 预训练卷积神经网络
- **数据增强** - 支持20+种增强策略
- **迁移学习** - 基于ImageNet预训练权重

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+
- CUDA (可选，用于GPU加速)

### 后端启动
```bash
cd compost_system
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 前端启动
```bash
cd compost_client
npm install
npm run dev
```

## 📁 项目结构

```
├── compost_system/          # Django后端
│   ├── api/                # API接口
│   ├── utils/              # 工具类
│   │   ├── train.py        # 模型训练
│   │   └── dataset_dispose.py  # 数据增强
│   └── upload/             # 文件上传目录
├── compost_client/         # Vue前端
│   ├── src/
│   │   ├── pages/          # 页面组件
│   │   ├── components/     # 通用组件
│   │   └── api/           # API接口
└── README.md
```

## 🔬 AI模型详情

### 数据增强策略
- **几何变换**: 随机旋转、翻转、缩放
- **颜色空间**: 亮度、对比度、饱和度调整
- **数据扩充**: 每张原图生成20个变种

### 模型架构
- 基础模型: ResNet18
- 分类类别: 2类（成熟/未成熟）
- 输入尺寸: 224×224×3
- 输出: 分类结果 + 置信度

## 📊 功能截图

- 用户登录界面
- 图像上传检测
- 数据可视化面板
- 检测历史记录

## 🤝 贡献指南

欢迎提交Issues和Pull Requests来改进项目！

## 📄 许可证

MIT License

## 👨‍💻 作者

杨盛林leo- 智能农业解决方案开发者

---

⭐ 如果这个项目对你有帮助，请给个Star支持一下！