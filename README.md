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

## 🛠️ Tech Stack

### Backend
- **Python 3.8+**
- **Django 5.2.4** - Web framework
- **PyTorch** - Deep learning framework
- **torchvision** - Computer vision library
- **Pillow** - Image processing

### Frontend
- **Vue.js 3** - Progressive JavaScript framework
- **Element Plus** - Vue 3 UI component library
- **ECharts** - Data visualization library
- **Vite** - Next-generation build tool

### AI Model
- **ResNet18** - Pre-trained Convolutional Neural Network
- **Data Augmentation** - 20+ augmentation strategies supported
- **Transfer Learning** - Based on ImageNet pre-trained weights

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

### 🎥 Demo Video

#### Complete Feature Demonstration
<!-- Replace the link below with your actual video link -->

https://github.com/user-attachments/assets/your-demo-video.mp4

> 📹 Demo Content: User Login → Image Upload → AI Detection → Result Display → Data Analytics

#### Quick Preview GIF
<!-- Optional: Add GIF animation for quick preview -->
![Smart Compost Detection Demo](https://github.com/imnotleo666/compost/assets/demo.gif)

### 📸 Feature Screenshots
- User login interface
- Image upload and detection  
- Data visualization dashboard
- Detection history records

## 🤝 Contributing

We welcome Issues and Pull Requests to improve this project!

## 📄 License

MIT License

## 👨‍💻 Author

**Yang Shenglin (Leo)** - Smart Agricultural Solutions Developer

- 🎓 Computer Science Student
- 🌱 Passionate about AI in Agriculture  
- 💻 Full-Stack Developer & ML Engineer

---

⭐ If this project helps you, please give it a Star to support us!