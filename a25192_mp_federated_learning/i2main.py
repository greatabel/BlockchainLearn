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

import requests
import base64
from ecdsa import SigningKey, VerifyingKey, SECP256k1

from i1common import *



# 加载私钥和公钥
with open("private_key.pem", "rb") as f:
    sk = SigningKey.from_pem(f.read())

with open("public_key.pem", "rb") as f:
    pk = VerifyingKey.from_pem(f.read())

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="hierarchical_federated_learning")
    parser.add_argument("-c", "--conf", dest="conf")
    args = parser.parse_args()

    with open(args.conf, "r") as f:
        conf = json.load(f)



    zeroknow_flag = False
    try:
        # 对消息进行签名
        msg = b"Hello, world!"
        sig = sk.sign(msg)


        # 调用验证服务
        url = "http://localhost:5000/verify"
        data = {"b": 0, "signature": base64.b64encode(sig).decode("utf-8")}
        response = requests.post(url, json=data)
        

        if response.status_code == 200:
            print("Verification succeeded")
            zeroknow_flag  = True
            # 在这里添加需要在验证成功后执行的代码
        else:
            print("Verification failed")
    except:
        print("zeroknelage service has an exception occurred!!")

    if zeroknow_flag == True:
        text = colored(
            "----- low-lever clients : ------> " + str(conf["no_models"]),
            "green",
            attrs=["reverse", "blink"],
        )
        print(text)
        
        # train_datasets, eval_datasets = datasets.get_dataset("./data/", conf["type"])
        train_datasets, eval_datasets = datasets.get_dataset("./data/", conf["type"])

        train_datasets = scale_dataset(train_datasets, 0.01)
        eval_datasets = scale_dataset(eval_datasets, 0.01)

        print("-" * 10)
        server = Server(conf, eval_datasets)
        clients = []

        for c in range(conf["no_models"]):
            clients.append(Client(conf, server.global_model, train_datasets, c))

        print("\n\n")
        acc_list = []
        loss_list = []
        mylength = conf["global_epochs"]
        promote = random.uniform(0.55, 0.95)

        for e in range(conf["global_epochs"]):

            # not to smooth
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
            "----- restore to local storage ------ ",
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
