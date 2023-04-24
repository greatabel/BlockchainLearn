import torch
from torchvision import datasets, transforms


def get_dataset(dir, name):

    if name == "mnist":

        transform_train = transforms.Compose(
            [
                transforms.Resize((224, 224)),
                transforms.Grayscale(
                    num_output_channels=3
                ),  # Add an extra channel to the input images
                transforms.ToTensor(),
                transforms.Normalize((0.1307,), (0.3081,)),
            ]
        )

        transform_test = transforms.Compose(
            [
                transforms.Resize((224, 224)),
                transforms.Grayscale(
                    num_output_channels=3
                ),  # Add an extra channel to the input images
                transforms.ToTensor(),
                transforms.Normalize((0.1307,), (0.3081,)),
            ]
        )

        train_dataset = datasets.MNIST(
            dir, train=True, download=True, transform=transform_train
        )
        eval_dataset = datasets.MNIST(dir, train=False, transform=transform_test)

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
    elif name == "fashion_mnist":
        all_transforms = transforms.Compose(
            [transforms.Resize(32), transforms.ToTensor()]
        )
        # Get train and test data
        train_dataset = datasets.FashionMNIST(
            dir, train=True, download=True, transform=all_transforms
        )
        eval_dataset = datasets.FashionMNIST(dir, train=False, transform=all_transforms)

    return train_dataset, eval_dataset
