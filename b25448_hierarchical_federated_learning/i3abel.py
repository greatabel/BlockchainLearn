import numpy as np
from scipy.optimize import linear_sum_assignment
from sklearn.metrics import adjusted_rand_score
import matplotlib.pyplot as plt


def k_means(data, k, max_iter=100):
    centroids = data[np.random.choice(len(data), k, replace=False)]
    for _ in range(max_iter):
        distances = np.linalg.norm(data[:, None] - centroids, axis=2)
        cluster_assignments = np.argmin(distances, axis=1)
        for i in range(k):
            centroids[i] = data[cluster_assignments == i].mean(axis=0)
    print('k_means :', centroids)
    return centroids



def ring_allreduce(data, num_nodes):
    # Compute the chunk size
    chunk_size = len(data) // num_nodes

    # Split the data into chunks
    chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]

    # Initialize the send and receive buffers
    send_buf = np.zeros_like(data)
    recv_buf = np.zeros_like(data)

    # Copy the data to the send buffer
    send_buf[:len(chunks[0])] = chunks[0]

    # Perform the ring allreduce
    for i in range(num_nodes - 1):
        # Send the current chunk to the next node
        dest = (i + 1) % num_nodes
        send_data = send_buf[i*chunk_size:(i+1)*chunk_size]
        recv_data = np.zeros_like(send_data)
        # Simulate the send and receive operations
        recv_data = chunks[dest] + send_data
        send_data = recv_data
        # Copy the received data to the receive buffer
        recv_buf[dest*chunk_size:(dest+1)*chunk_size] = recv_data

    # Copy the final result from the receive buffer to the send buffer
    send_buf = recv_buf

    # Perform the final reduction
    for i in range(num_nodes - 1):
        # Send the current chunk to the next node
        dest = (i + 1) % num_nodes
        send_data = send_buf[i*chunk_size:(i+1)*chunk_size]
        recv_data = np.zeros_like(send_data)
        # Simulate the send and receive operations
        recv_data = chunks[dest] + send_data
        send_data = recv_data
        # Copy the received data to the receive buffer
        recv_buf[dest*chunk_size:(dest+1)*chunk_size] = recv_data

    # Compute the final result
    result = np.sum(recv_buf, axis=0)
    print('result', '#'*20,result)
    return result


def jonker(data, centroids):
    print('jonker')
    cluster_assignments = np.zeros(len(data), dtype=int)
    distances = np.linalg.norm(data[:, None] - centroids, axis=2)
    row_idx, col_idx = linear_sum_assignment(distances)
    cluster_assignments[row_idx] = col_idx
    return cluster_assignments

def federated_learning(data, num_clusters, num_nodes):
    # Split the data into num_nodes partitions
    data_partitions = np.array_split(data, num_nodes)

    # Run k-means on each partition to find local centroids
    local_centroids = []
    for partition in data_partitions:
        local_centroids.append(k_means(partition, num_clusters))

    # Use the ring allreduce algorithm to compute the global centroids
    global_centroids = ring_allreduce(local_centroids, num_nodes)

    # Use the Jonker algorithm to assign each data point to a cluster
    cluster_assignments = jonker(data, global_centroids)

    return cluster_assignments



from sklearn.datasets import load_iris

def main():
    # Load the iris dataset
    iris = load_iris()
    data = iris.data

    # Run federated learning with 4 nodes and 5 clusters
    num_nodes = 4
    num_clusters = 5
    cluster_assignments = federated_learning(data, num_clusters, num_nodes)


    # Print the cluster assignments
    print("Cluster assignments:", cluster_assignments)

    # Evaluate the clustering performance
    true_labels = iris.target
    ari = adjusted_rand_score(true_labels, cluster_assignments)
    print("Adjusted Rand Index:", ari)

    # Visualize the clustering results
    plt.figure(figsize=(8, 6))
    plt.scatter(data[:, 0], data[:, 1], c=cluster_assignments)
    plt.title("Federated K-Means Clustering Results")
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")
    plt.show()


if __name__ == '__main__':
    main()

