import os
from torchvision import transforms, utils, datasets
from torch.utils.data import DataLoader
from PIL import Image
import os
os.chdir('G://2025年项目/农作物堆肥成熟度')
# 定义图像变换的方式
transformations = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.2),
    transforms.ToTensor()  # 转换为tensor并归一化至[0,1]
])

# 图像位于'images'文件夹下
dataset = datasets.ImageFolder(root='images', transform=transformations)

output_dir = 'augmented_images'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


def save_augmented_images(dataset, output_dir):
    to_pil = transforms.ToPILImage()
    # 获取原始图像路径
    original_dataset = datasets.ImageFolder(root='images', transform=None)

    for idx in range(len(original_dataset)):
        original_image, _ = original_dataset[idx]
        # 为每个变种重新应用变换
        for j in range(20):
            # 重新应用变换
            transformed_tensor = dataset.transform(original_image)
            augmented_image_path = os.path.join(output_dir, f'image_{idx}_variant_{j}.jpg')

            # 转换并保存
            pil_image = to_pil(transformed_tensor)
            pil_image.save(augmented_image_path)


# 保存增强后的图片
save_augmented_images(dataset, output_dir)

print("图片增强与保存完成")