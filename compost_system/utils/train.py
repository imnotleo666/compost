import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader, random_split
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
#os.chdir('G://2025年项目/农作物堆肥成熟度')

class CompostClassifier:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {self.device}")

        # Initialize variables
        self.train_loader = None
        self.test_loader = None
        self.model = None
        self.criterion = None
        self.optimizer = None

    def prepare_data(self, batch_size=32, test_split=0.2):
        """准备数据集并划分训练集和测试集"""
        print("Preparing data...")

        # 定义数据变换
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(10),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

        # 加载数据集
        dataset = datasets.ImageFolder(root=self.data_dir, transform=transform)

        # 划分训练集和测试集
        train_size = int((1 - test_split) * len(dataset))
        test_size = len(dataset) - train_size
        train_dataset, test_dataset = random_split(dataset, [train_size, test_size])

        # 创建DataLoader
        self.train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        self.test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

        print(f"Training set size: {len(train_dataset)}")
        print(f"Test set size: {len(test_dataset)}")
        print(f"Classes: {dataset.classes}")

    def build_model(self, learning_rate=0.001):
        """构建模型"""
        print("Building model...")

        # 使用预训练的ResNet18模型
        self.model = models.resnet18(pretrained=True)

        # 修改最后一层以适应2分类问题
        num_features = self.model.fc.in_features
        self.model.fc = nn.Linear(num_features, 2)

        # 将模型移动到指定设备
        self.model = self.model.to(self.device)

        # 定义损失函数和优化器
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)

    def train(self, num_epochs=10):
        """训练模型"""
        print("Starting training...")

        best_accuracy = 0.0
        train_losses, train_accuracies = [], []
        test_losses, test_accuracies = [], []

        for epoch in range(num_epochs):
            # 训练阶段
            self.model.train()
            running_loss = 0.0
            correct_train = 0
            total_train = 0

            for images, labels in self.train_loader:
                images, labels = images.to(self.device), labels.to(self.device)

                self.optimizer.zero_grad()
                outputs = self.model(images)
                loss = self.criterion(outputs, labels)
                loss.backward()
                self.optimizer.step()

                running_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                total_train += labels.size(0)
                correct_train += (predicted == labels).sum().item()

            train_loss = running_loss / len(self.train_loader)
            train_accuracy = 100 * correct_train / total_train
            train_losses.append(train_loss)
            train_accuracies.append(train_accuracy)

            # 测试阶段
            self.model.eval()
            running_loss = 0.0
            correct_test = 0
            total_test = 0

            with torch.no_grad():
                for images, labels in self.test_loader:
                    images, labels = images.to(self.device), labels.to(self.device)
                    outputs = self.model(images)
                    loss = self.criterion(outputs, labels)

                    running_loss += loss.item()
                    _, predicted = torch.max(outputs.data, 1)
                    total_test += labels.size(0)
                    correct_test += (predicted == labels).sum().item()

            test_loss = running_loss / len(self.test_loader)
            test_accuracy = 100 * correct_test / total_test
            test_losses.append(test_loss)
            test_accuracies.append(test_accuracy)

            print(f'Epoch [{epoch + 1}/{num_epochs}], '
                  f'Train Loss: {train_loss:.4f}, Train Acc: {train_accuracy:.2f}%, '
                  f'Test Loss: {test_loss:.4f}, Test Acc: {test_accuracy:.2f}%')

            # 保存最佳模型
            if test_accuracy > best_accuracy:
                best_accuracy = test_accuracy
                torch.save(self.model.state_dict(), 'best_model.pth')
                print(f"Best model saved with accuracy: {best_accuracy:.2f}%")

        print('Training complete.')
        return train_losses, train_accuracies, test_losses, test_accuracies

    def plot_training_history(self, train_losses, train_accuracies, test_losses, test_accuracies):
        """绘制训练历史图表"""
        print("Plotting training history...")

        plt.figure(figsize=(15, 6))

        # 损失曲线
        plt.subplot(1, 2, 1)
        plt.plot(train_losses, label='Train Loss', linewidth=2)
        plt.plot(test_losses, label='Test Loss', linewidth=2)
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.title('Training and Test Loss')
        plt.legend()
        plt.grid(True, alpha=0.3)

        # 准确率曲线
        plt.subplot(1, 2, 2)
        plt.plot(train_accuracies, label='Train Accuracy', linewidth=2)
        plt.plot(test_accuracies, label='Test Accuracy', linewidth=2)
        plt.xlabel('Epochs')
        plt.ylabel('Accuracy (%)')
        plt.title('Training and Test Accuracy')
        plt.legend()
        plt.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig('training_plots.png', dpi=300, bbox_inches='tight')
        plt.show()

        print("Training plots saved as 'training_plots.png'")

    def evaluate(self):
        """评估模型性能"""
        print("Evaluating model...")

        self.model.eval()
        correct = 0
        total = 0
        class_correct = [0, 0]
        class_total = [0, 0]

        with torch.no_grad():
            for images, labels in self.test_loader:
                images, labels = images.to(self.device), labels.to(self.device)
                outputs = self.model(images)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

                # 计算每个类别的准确率
                c = (predicted == labels).squeeze()
                for i in range(labels.size(0)):
                    label = labels[i]
                    class_correct[label] += c[i].item()
                    class_total[label] += 1

        accuracy = 100 * correct / total
        print(f'Overall Accuracy: {accuracy:.2f}%')

        # 打印每个类别的准确率
        dataset = datasets.ImageFolder(root=self.data_dir)
        for i in range(2):
            if class_total[i] > 0:
                class_acc = 100 * class_correct[i] / class_total[i]
                print(f'Accuracy of {dataset.classes[i]}: {class_acc:.2f}%')

        return accuracy

    def load_model(self, model_path='best_model.pth'):
        """加载训练好的模型"""
        print(f"Loading model from {model_path}...")

        if self.model is None:
            self.build_model()  # 如果模型未创建，先创建

        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.eval()
        print("Model loaded successfully!")

    def predict(self, image_path):
        """对单张图片进行预测"""
        # 定义与训练时相同的变换（除了数据增强）
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

        # 加载并预处理图片
        image = Image.open(image_path).convert('RGB')
        image = transform(image).unsqueeze(0)  # 添加batch维度
        image = image.to(self.device)

        # 进行预测
        with torch.no_grad():
            output = self.model(image)
            probabilities = torch.nn.functional.softmax(output[0], dim=0)
            predicted_class = torch.argmax(output, dim=1).item()
            confidence = probabilities[predicted_class].item()

        # 获取类别名称
        dataset = datasets.ImageFolder(root=self.data_dir)
        class_names = dataset.classes

        return class_names[predicted_class], confidence, probabilities.cpu().numpy()

    def predict_from_folder(self, folder_path):
        """对文件夹中的所有图片进行预测"""
        results = []
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(folder_path, filename)
                try:
                    prediction, confidence, probabilities = self.predict(image_path)
                    results.append({
                        'filename': filename,
                        'prediction': prediction,
                        'confidence': confidence,
                        'probabilities': probabilities
                    })
                except Exception as e:
                    print(f"Error processing {filename}: {str(e)}")

        return results


classifier = CompostClassifier(data_dir='images')
classifier.build_model(learning_rate=0.001)
classifier.load_model('best_model.pth')
# 使用示例
def main():
    # 初始化分类器
    classifier = CompostClassifier(data_dir='images')  # 替换为你的数据路径

    # 准备数据
    #classifier.prepare_data(batch_size=32, test_split=0.2)

    # 构建模型
    classifier.build_model(learning_rate=0.001)

    # 训练模型
    #train_losses, train_accuracies, test_losses, test_accuracies = classifier.train(num_epochs=20)

    # 绘制训练历史
    #classifier.plot_training_history(train_losses, train_accuracies, test_losses, test_accuracies)

    # 评估模型
    #accuracy = classifier.evaluate()

    # 加载最佳模型进行推理
    classifier.load_model('best_model.pth')

    # 对单张图片进行预测
    prediction, confidence, probabilities = classifier.predict('images/0/1_19.png')
    print(f"Prediction: {prediction}, Confidence: {confidence:.4f}")
    print(f"Probabilities: Mature={probabilities[0]:.4f}, Immature={probabilities[1]:.4f}")

    # 对文件夹中的图片进行批量预测
    # results = classifier.predict_from_folder('path/to/test/folder')
    # for result in results:
    #     print(f"{result['filename']}: {result['prediction']} ({result['confidence']:.4f})")


if __name__ == "__main__":
    main()