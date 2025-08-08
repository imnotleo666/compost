# 🌱 Smart Compost Maturity Detection System

An AI-powered agricultural solution that automatically determines compost maturity through advanced image recognition technology.

## 📋 Project Overview

This system leverages deep learning technology combined with modern web frameworks to provide intelligent compost maturity detection services for agricultural production. Users simply upload compost images, and the system automatically determines maturity levels with confidence scores.

## ✨ Key Features

- 🔍 **AI Image Recognition**: ResNet18-based deep learning model for accurate compost maturity classification
- 📊 **Data Visualization**: Real-time display of detection history, user statistics, and multi-dimensional analytics
- 👥 **User Management**: Comprehensive role-based access control for administrators and regular users
- 📱 **Responsive Interface**: Modern web interface optimized for both desktop and mobile devices
- 📈 **Detection Records**: Complete detection history tracking with data export capabilities
- ⚡ **Real-time Prediction**: Millisecond-level response time for instant results

## 🤖 AI Technology

This system uses **ResNet18**, a pre-trained Convolutional Neural Network, with transfer learning based on ImageNet weights to accurately classify compost maturity. The model supports 20+ data augmentation strategies to improve accuracy and robustness.

## 📁 Project Structure

```
├── compost_system/          # Django Backend
│   ├── api/                # API endpoints
│   ├── utils/              # Utility modules
│   │   ├── train.py        # Model training
│   │   └── dataset_dispose.py  # Data augmentation
│   └── upload/             # File upload directory
├── compost_client/         # Vue Frontend
│   ├── src/
│   │   ├── pages/          # Page components
│   │   ├── components/     # Reusable components
│   │   └── api/           # API interfaces
├── requirements.txt        # Python dependencies
├── deploy.sh              # Deployment script
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- CUDA (optional, for GPU acceleration)

### Backend Setup
```bash
cd compost_system
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend Setup
```bash
cd compost_client
npm install
npm run dev
```


## 🔬 AI Model Details

### Data Augmentation Strategy
- **Geometric Transformations**: Random rotation, flipping, scaling
- **Color Space Adjustments**: Brightness, contrast, saturation modifications
- **Data Multiplication**: Generate 20 variants per original image

### Model Architecture
- **Base Model**: ResNet18
- **Classification Classes**: 2 classes (Mature/Immature)
- **Input Size**: 224×224×3
- **Output**: Classification result + Confidence score

## 📊 Project Demo

### 🎥 Demo Videos

#### 🌟 Website Features Demo


https://github.com/user-attachments/assets/b3c3618b-4aae-4e06-9b25-560be1b5e6e0


> 📹 Features Demo: User Interface → Image Upload → AI Detection → Results Display → Data Analytics Dashboard

#### 🚀 Project Setup & Startup Process

https://github.com/user-attachments/assets/aa228cba-a0d3-48c2-a478-b7a915727221

> 🛠️ Startup Demo: Backend Launch → Frontend Launch → System Testing



## 🤝 Contributing

We welcome Issues and Pull Requests to improve this project!


## 👨‍💻 Author

**Yang Shenglin (Leo)** - Smart Environmental Solutions Developer

- 🎓 High School Student
- 🌱 Passionate about AI in Environment  

---

⭐ If this project helps you, please give it a Star to support us!
