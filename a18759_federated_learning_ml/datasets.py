import torch
from torchvision import datasets, transforms


def get_dataset(dir, name):

    if name == "mnist":
        train_dataset = datasets.MNIST(
            dir, train=True, download=True, transform=transforms.ToTensor()
        )
        eval_dataset = datasets.MNIST(dir, train=False, transform=transforms.ToTensor())

    elif name == "cifar":
        transform_train = transforms.Compose(
            [
                transforms.RandomCrop(32, padding=4),
                transforms.RandomHorizontalFlip(),
                transforms.ToTensor(),
                transforms.Normalize(
                    (0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)
                ),
            ]
        )

        transform_test = transforms.Compose(
            [
                transforms.ToTensor(),
                transforms.Normalize(
                    (0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)
                ),
            ]
        )

        train_dataset = datasets.CIFAR10(
            dir, train=True, download=True, transform=transform_train
        )
        eval_dataset = datasets.CIFAR10(dir, train=False, transform=transform_test)

    print("len(train_dataset)=", len(train_dataset))
    print("len(eval_dataset)=", len(eval_dataset))

    print("\n")
    # 随机再从整体筛选出小批量随机到数据集，因为训练时间太长，为了演示录制视频加速，使用小批量数据集
    # 不需要时候可以关闭： 直接注释掉start 到 end的 部分
    print("Start:Fast training with small batches.")
    fast_rato = 20
    evens = list(range(0, len(train_dataset), fast_rato))
    odds = list(range(0, len(eval_dataset), fast_rato))
    train_dataset = torch.utils.data.Subset(train_dataset, evens)
    eval_dataset = torch.utils.data.Subset(eval_dataset, odds)

    print("len(train_dataset)=", len(train_dataset))
    print("len(eval_dataset)=", len(eval_dataset))
    print("End:Fast training with small batches.")

    return train_dataset, eval_dataset
