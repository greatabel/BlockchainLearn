from textblob import TextBlob
import tensorflow as tf
import numpy as np
from keras.preprocessing.text import Tokenizer


NB_WORDS = 10000
tk = Tokenizer(
    num_words=NB_WORDS,
    filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',
    lower=True,
    split=" ",
)


def one_hot_seq(seqs, nb_features=NB_WORDS):
    ohs = np.zeros((len(seqs), nb_features))
    for i, s in enumerate(seqs):
        ohs[i, s] = 1.0
    return ohs


def anlaysis(text):
    """
    mymodel = tf.keras.models.load_model("../i2sentiment_analysis/drop_model.h5")
    mytext = tk.texts_to_sequences(text)
    mytext = one_hot_seq(mytext)
    # 真实数据预测
    q = mymodel.predict(
        np.array(
            [
                mytext,
            ]
        )
    )
    result = np.around(q, decimals=3)
    print('result=', result)
    """

    """
    下面的方式更快
    """

    total = 0
    blob = TextBlob(text)
    blob.tags  # [('The', 'DT'), ('titular', 'JJ'),
    #  ('threat', 'NN'), ('of', 'IN'), ...]
    # print('@', blob.tags)
    blob.noun_phrases  # WordList(['titular threat', 'blob',
    #            'ultimate movie monster',
    #            'amoeba-like mass', ...])
    # print('#', blob.noun_phrases)
    for sentence in blob.sentences:
        # print(sentence.sentiment.polarity)
        total += sentence.sentiment.polarity
    return blob.noun_phrases, total


# if __name__ == "__main__":
#     anlaysis('The fox and the wolf give you New Year greetings, so terrible')
