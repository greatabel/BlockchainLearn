import pandas as pd
from csv_operation import csv_reader
from sentiment import anlaysis
import time
# 检查数据集是否正常
data2020 = csv_reader("i0btc_tweet.csv", "data")
print(data2020[0], "#" * 10, data2020[1], "#" * 10, " \n", data2020[2])


print("-" * 10, "tweets:")
print(data2020[1][3], "data2020[1][10]=", data2020[1][10], "\n", "@" * 10)


print("start", "*-* *-* *-* *-* *-* " * 10)

# 处理基于天的热度
from collections import defaultdict

appearances = defaultdict(int)

for curr in data2020:
    if len(curr) >= 3 and "2021" in curr[3]:
        appearances[curr[3]] += 1
print('appearances=> '*10,appearances)

# time.sleep(100)

# 持久化为其他程序做处理
import pickle

with open("hot.pickle", "wb") as handle:
    pickle.dump(appearances, handle)

with open("hot.pickle", "rb") as handle:
    b = pickle.load(handle)
# print('b=', b)

sentiment_dict = {}
for k, v in appearances.items():
    pick_twlist = [x[10] for x in data2020 if len(x) >= 3 and x[3] == k]
    total_sentiment = 0
    num_positive = 0
    num_neural = 0
    num_nagtive = 0
    split = 10
    # print(k, '#'*10, pick_twlist)
    for tw in pick_twlist[:split]:
        text = tw

        # print(text, "\n@@@username=", username, "\n")
        words, sentiment_tw = anlaysis(text)
        print(sentiment_tw)
        total_sentiment += sentiment_tw
        if sentiment_tw < 0:
            num_nagtive += 1
        if sentiment_tw == 0:
            num_neural += 1
        if sentiment_tw > 0:
            num_positive += 1
        # print('words=', words)

    print("tatal sentiment polarity:", total_sentiment)
    print("average sentiment polarity:", total_sentiment / len(pick_twlist))
    print(
        "number of (positive VS neural VS nagtive):",
        num_positive * split,
        num_neural * split,
        num_nagtive * split,
    )
    s = num_positive * split - num_nagtive * split
    sentiment_dict[k] = s

print("@" * 10, sentiment_dict)
with open("sentiment_dict.pickle", "wb") as handle:
    pickle.dump(sentiment_dict, handle)

print("end", "*-* *-* *-* *-* *-* " * 10)


# # 进行可视化分析

js_txt = """

var DATA = {
"""

print("\n1. Heat comparison")
print(len(data2020), " VS 0")

compare_txt = "'data2021':" + str(len(data2020))
js_txt += compare_txt


# data2020full = csv_reader("2021-06senkaku.csv", "data")
data2020full = data2020

print("\n2. sentiment anlaysis")
total_sentiment = 0

num_positive = 0
num_neural = 0
num_nagtive = 0

unwanted_chars = ".,-_ ()’'"
black_list = [
    "//t.co/daqs0qh2wb #",
    "# #",
    "[ auto ]",
    "//t.co/tgzew5at0r https",
    "s territory",
]
wordfreq = {}

usernamefreq = {}

split = 51
# pick_twlist = data2020full[0::split]
pick_twlist = data2020full[0::split]
for tw in pick_twlist:
    text = tw[10]
    username = tw[8]
    # print(text, "\n@@@username=", username, "\n")
    words, sentiment_tw = anlaysis(text)
    print(sentiment_tw)
    total_sentiment += sentiment_tw
    if sentiment_tw < 0:
        num_nagtive += 1
    if sentiment_tw == 0:
        num_neural += 1
    if sentiment_tw > 0:
        num_positive += 1
    # print('words=', words)
    for raw_word in words:
        word = raw_word.strip(unwanted_chars)
        if word not in wordfreq:
            if word not in black_list:
                wordfreq[word] = 0
        if word not in black_list:
            wordfreq[word] += 1
    if username == "Indo-Pacific News - Watching the CCP-China Threat":
        username = "Indo-Pacific News"
    username = username.replace("'", "")
    if username not in usernamefreq:
        usernamefreq[username] = 0
    usernamefreq[username] += 1

print("@" * 30, usernamefreq)

print("tatal sentiment polarity:", total_sentiment)
print("average sentiment polarity:", total_sentiment / len(pick_twlist))
print(
    "number of (positive VS neural VS nagtive):",
    num_positive * split,
    num_neural * split,
    num_nagtive * split,
)
sentiment_txt = (
    ",'total_sentiment_polarity':"
    + str(round(total_sentiment, 2))
    + ", 'average_sentiment_polarity':"
    + str(round(total_sentiment / len(pick_twlist), 2))
    + ",'num_positive':"
    + str(num_positive * split)
    + ", 'num_neural':"
    + str(num_neural * split)
    + ",'num_nagtive':"
    + str(num_nagtive * split)
    + ", 'data2021':"
    + str(len(data2020))
)
js_txt += sentiment_txt

js_txt += " };\n"


print("\n 3. related words related to this topic")

js_txt += "var RELATED_WORDS = {"
# print(wordfreq)
index = 0
a1_sorted_keys = sorted(wordfreq, key=wordfreq.get, reverse=True)
for r in a1_sorted_keys:
    if wordfreq[r] > 1 and r not in ("s"):
        print(r, wordfreq[r])
        if index < 10:
            js_txt += "'" + r + "':" + str(wordfreq[r]) + ","
            index += 1


js_txt += " };\n"


index = 0
print("\n 4. username often posts related topics")
js_txt += "var WHO_TWEETS = {"
a2_sorted_keys = sorted(usernamefreq, key=usernamefreq.get, reverse=True)
# print('#'*20, usernamefreq)

for r in a2_sorted_keys:
    if usernamefreq[r] >= 1 and r not in ("name"):
        print(r, usernamefreq[r])
        if index < 10:
            js_txt += "'" + r + "':" + str(usernamefreq[r]) + ","
            index += 1


js_txt += " };"

# write to a local js file , let d3 do data-visual
with open("data_visualization/senkufu.js", "w") as file:
    file.write(js_txt.strip())
