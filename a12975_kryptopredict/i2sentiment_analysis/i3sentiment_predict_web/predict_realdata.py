import numpy as np

from tensorflow.keras import models
import tensorflow as tf

import pickle


def flow_predict(i):
    i = int(i)
    print("i=", i)
    MyX_test_oh = None
    # identical to the previous one
    mymodel = tf.keras.models.load_model("drop_model.h5")
    with open("test.pkl", "rb") as f:
        MyX_test_oh = pickle.load(f)
    print(i, MyX_test_oh[i],len(MyX_test_oh[i]), '#'*20)
    # 真实数据预测
    q = mymodel.predict(
        np.array(
            [
                MyX_test_oh[i],
            ]
        )
    )
    result = np.around(q, decimals=3)
    print('result=', result)
    return result


if __name__ == "__main__":
    flow_predict(1)
