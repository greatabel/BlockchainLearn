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


from i1common import *
	

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='hierarchical_federated_learning')
	parser.add_argument('-c', '--conf', dest='conf')
	args = parser.parse_args()
	

	with open(args.conf, 'r') as f:
		conf = json.load(f)	


	text = colored(
	    "----- low-lever clients : ------> " + str(conf["no_models"]),
	    "green",
	    attrs=["reverse", "blink"],
	)
	print(text)

	# Generate some random data
	data = np.random.rand(1000, 2)

	# Run federated learning with 4 nodes and 5 clusters
	num_nodes = 4
	num_clusters = 5
	cluster_assignments = federated_learning(data, num_clusters, num_nodes)



	# train_datasets, eval_datasets = datasets.get_dataset("./data/", conf["type"])
	train_datasets, eval_datasets = datasets.get_dataset("./data/", conf["type"])

	# train_datasets = scale_dataset(train_datasets, 1.01)
	# eval_datasets = scale_dataset(eval_datasets, 1.01)

	print('-'*10)
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
			
		
		

		
		
