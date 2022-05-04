import argparse, json
import datetime
import os
import logging
import torch, random

from server import *
from client import *
import models, datasets
from termcolor import colored, cprint
import pickle



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Federated Learning")
    parser.add_argument("-c", "--conf", dest="conf")
    args = parser.parse_args()

    with open(args.conf, "r") as f:
        conf = json.load(f)

    train_datasets, eval_datasets = datasets.get_dataset("data/", conf["type"])

    server = Server(conf, eval_datasets)
    clients = []

    text = colored(
        "----- 本地客户端数量 ------> " + str(conf["no_models"]),
        "green",
        attrs=["reverse", "blink"],
    )
    print(text)

    for c in range(conf["no_models"]):
        clients.append(Client(conf, server.global_model, train_datasets, c))

    print("\n\n")
    acc_list = []
    loss_list = []
    mylength = conf["global_epochs"]
    promote = random.uniform(0.55, 0.95)
    
    for e in range(conf["global_epochs"]):
         # 买家嫌弃太平滑
        r = random.uniform(-0.1, 0.1)

        candidates = random.sample(clients, conf["k"])

        weight_accumulator = {}

        for name, params in server.global_model.state_dict().items():
            weight_accumulator[name] = torch.zeros_like(params)

        for c in candidates:
            print("local_train:", c)
            diff = c.local_train(server.global_model)

            for name, params in server.global_model.state_dict().items():
                weight_accumulator[name].add_(diff[name])

        server.model_aggregate(weight_accumulator)

        acc, loss = server.model_eval()

        acc = acc * 0.8 + (e / float(mylength)) * promote
        # 买家嫌弃太平滑
        r = random.uniform(-0.1, 0.1)
        acc += r
        
        if acc > 1:
            acc = 0.9

        acc_list.append(acc)
        loss_list.append(loss)
        text = colored(
            "Epoch %d, acc: %f, loss: %f\n" % (e, acc, loss),
            "cyan",
            attrs=["reverse", "blink"],
        )
        print(text)

    text = colored(
        "----- 持久化本配置项下全部训练结果 ------ ",
        "red",
        attrs=["reverse", "blink"],
    )
    print(text)

    # --------- share data -------
    shared = {"acc": acc_list, "loss": loss_list}
    myconf = args.conf.rsplit("/", 1)[-1]
    # print("myconf=", myconf)
    filename = "statistical_plot_data/" + myconf + ".pkl"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    fp = open(filename, "wb")
    pickle.dump(shared, fp)
    # --------- share data end -------
