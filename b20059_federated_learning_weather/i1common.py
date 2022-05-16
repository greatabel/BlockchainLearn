import pickle


def get_acc_loss_by_conf(conf):
    print("\nconf=", conf, "\n")
    print("-" * 20, "\n")

    fp = open("statistical_plot_data/" + conf, "rb")
    shared = pickle.load(fp)
    acc = shared["acc"]
    loss = shared["loss"]
    print("GUI back thread is receving:", acc, "\n", "loss=", loss)
    return acc, loss


if __name__ == "__main__":
    get_acc_loss_by_conf("conf_centralized1_1.json.pkl")
    get_acc_loss_by_conf("conf_centralized1_2.json.pkl")
    get_acc_loss_by_conf("conf_centralized1_3.json.pkl")
    get_acc_loss_by_conf("conf_f5.json.pkl")
    get_acc_loss_by_conf("conf_f10.json.pkl")
