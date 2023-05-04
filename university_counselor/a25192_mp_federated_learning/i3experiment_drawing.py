import numpy as np
import matplotlib.pyplot as plt

from i1common import get_acc_loss_by_conf

hierarchical_federate_acc1, centralized_loss1 = get_acc_loss_by_conf(
    "conf_cifar.json.pkl"
)
central_acc2, centralized_loss2 = get_acc_loss_by_conf("conf_fashion.json.pkl")
central_acc3, centralized_loss3 = get_acc_loss_by_conf("conf_mnist.json.pkl")
federate_acc1, federate_loss1 = get_acc_loss_by_conf("conf_f5.json.pkl")
federate_acc2, federate_loss2 = get_acc_loss_by_conf("conf_f10.json.pkl")

central_acc_from_f10_1, _ = get_acc_loss_by_conf("conf_cifar.json.pkl")
central_acc_from_f10_2, _ = get_acc_loss_by_conf("conf_fashion.json.pkl")
central_acc_from_f10_3, _ = get_acc_loss_by_conf("conf_mnist.json.pkl")

print("#" * 30)
print(hierarchical_federate_acc1)

labels = ["normal_hearchical3", "more_hearchical5", "central_normal_hearchical"]
men_means = [
    hierarchical_federate_acc1[-2],
    hierarchical_federate_acc1[-1],
    central_acc_from_f10_1[-1],
]
women_means = [central_acc2[-2], central_acc2[-1], central_acc_from_f10_2[-1]]
f_means = [federate_acc1[-2], federate_acc1[-1], central_acc_from_f10_3[-1]]

print(men_means, women_means)

x = np.arange(len(labels))
width = 0.25

fig, ax = plt.subplots()
rects1 = ax.bar(x - width, men_means, width, label="hierarchical_federate_cifar_acc1")
rects2 = ax.bar(x, women_means, width, label="federate_acc_fashion_acc1")
rects3 = ax.bar(x + width, f_means, width, label="federate_minist_acc1")

ax.set_ylabel("Scores")
ax.set_title("accuracy by client")
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)
ax.bar_label(rects3, padding=3)

fig.tight_layout()

plt.show()


print("-" * 30, "2rd plots of acc and loss")
font_size = 18
marker_size = 14


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
line_labels = [
    "hierarchical_federate_cifar1",
    "hierarchical_federate_fashion2",
    "hierarchical_federate_minist3",
    "normal-federate1",
]
ax1.set_xlabel("step", fontsize=font_size)
ax1.set_xticks(range(20))
# ax1.set_xticklabels(["0","-3","-5","-7","-10","-12","-15","-17","-20"], fontsize=font_size)
ax1.set_xticklabels(list(range(20)), fontsize=font_size)

ax1.set_yticks([0.3, 0.4, 0.5, 0.6, 10, 20, 30, 40])
ax1.set_yticklabels([0.3, 0.4, 0.5, 0.6, 10, 20, 30, 40], fontsize=font_size)
ax1.set_ylabel("acc", fontsize=font_size)

l1 = ax1.plot(
    hierarchical_federate_acc1,
    markersize=marker_size,
    linestyle="--",
    linewidth=3,
    label=line_labels[0],
)
l2 = ax1.plot(central_acc2, marker="v", markersize=marker_size, label=line_labels[1])
l3 = ax1.plot(central_acc3, marker="o", markersize=marker_size, label=line_labels[2])
l4 = ax1.plot(federate_acc1, marker="*", markersize=marker_size, label=line_labels[3])


ax2.set_xlabel("step", fontsize=font_size)
ax2.set_ylabel("loss", fontsize=font_size)
# ax2.set_xticks(range(9))
ax2.set_xticks(range(20))
# ax2.set_xticklabels(["0","-3","-5","-7","-10","-12","-15","-17","-20"], fontsize=font_size)
ax2.set_xticklabels(list(range(20)), fontsize=font_size)

ax2.set_yticks([1.0, 1.5, 2.0, 4, 5.0, 10])
ax2.set_yticklabels([1.0, 1.5, 2.0, 4, 5.0, 10], fontsize=font_size)

l1 = ax2.plot(centralized_loss1, markersize=marker_size, linestyle="--", linewidth=3)
l2 = ax2.plot(centralized_loss2, marker="v", markersize=marker_size)
l3 = ax2.plot(centralized_loss3, marker="o", markersize=marker_size)
l4 = ax2.plot(federate_loss1, marker="*", markersize=marker_size)


lgd = fig.legend(
    [l1, l2, l3, l4],  # The line objects
    labels=line_labels,  # The labels for each line
    loc="lower center",  # Position of legend
    ncol=3,
    fontsize=font_size,
    fancybox=True,
    bbox_to_anchor=(0.51, 1),
)
fig.artists.append(lgd)

fig.legend(labels=line_labels)
# plt.tight_layout()
# plt.savefig("compare.png", dpi=600, format="png", bbox_inches="tight")
plt.show()
