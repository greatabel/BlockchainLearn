import argparse, json
import datetime
import os
import logging
import torch, random

from server import *
from client import *
import models, datasets

from i1common import *
	

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='hierarchical_federated_learning')
	parser.add_argument('-c', '--conf', dest='conf')
	args = parser.parse_args()
	

	with open(args.conf, 'r') as f:
		conf = json.load(f)	
	

	# Generate some random data
	data = np.random.rand(1000, 2)

	# Run federated learning with 4 nodes and 5 clusters
	num_nodes = 4
	num_clusters = 5
	cluster_assignments = federated_learning(data, num_clusters, num_nodes)



	train_datasets, eval_datasets = datasets.get_dataset("./data/", conf["type"])
	print('-'*10)
	server = Server(conf, eval_datasets)
	clients = []
	
	for c in range(conf["no_models"]):
		clients.append(Client(conf, server.global_model, train_datasets, c))
		
	print("\n\n")
	for e in range(conf["global_epochs"]):
	
		candidates = random.sample(clients, conf["k"])
		
		weight_accumulator = {}
		
		for name, params in server.global_model.state_dict().items():
			weight_accumulator[name] = torch.zeros_like(params)
		
		for c in candidates:
			diff = c.local_train(server.global_model)
			
			for name, params in server.global_model.state_dict().items():
				weight_accumulator[name].add_(diff[name])
				
		
		server.model_aggregate(weight_accumulator)
		
		acc, loss = server.model_eval()
		
		print("Epoch %d, acc: %f, loss: %f\n" % (e, acc, loss))
				
			
		
		
	
		
		
	