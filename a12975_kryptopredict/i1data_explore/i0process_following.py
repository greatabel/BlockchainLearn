import re
from csv_operation import csv_write


# test_str = '''


# John Carmack
# @ID_AA_Carmack
# Independent AI researcher, Consulting CTO Oculus VR, Founder Id Software and Armadillo Aerospace
# @arxivblog
# @arxivblog
# The best new ideas in science and technology. Now blogging at Discover Magazine, previously at
# Technology Review and Medium
# SpaceX
# @SpaceX
# SpaceX designs, manufactures and launches the world’s most advanced rockets and spacecraft
# Tim Urban
# @waitbutwhy
# Writer, infant
# TESLARATI
# @Teslarati
# Tesla, SpaceX, Elon Musk, and #FutureTech Go behind the scenes
# @TeslaratiTeam
# Ashlee Vance
# @ashleevance

# '''

import re

p = re.compile(r"@([^\s:]+)")


# test_str = "@galaxy5univ I like you\nRT @BestOfGalaxies: Let's sit under the stars ...\n@jonghyun"
# p2 = re.compile(r'(?:http|ftp|https)://(?:[\w_-]+(?:(?:\.[\w_-]+)+))(?:[\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?')
# print(p2.findall(test_str))
# # => ['galaxy5univ', 'BestOfGalaxies', 'jonghyun__bot', 'yosizo', 'LDH_3_yui']
# # => ['https://yahoo.com', 'https://msn.news.com']


# ---------- ------ ------------------------------ ------------------
# path_to_file = 'twitter_data/elonmusk_following.txt'
path_to_file = "twitter_data/pualg_follwing.txt"

text = ""
with open(path_to_file) as file_object:  # this is a safe way of opening files
    for line in file_object:
        text += line

list0 = p.findall(text)
print(len(list0))
list1 = list(set(list0))
print(len(list1))

mydata = []
for item in list1:
    mydata.append([item])

# csv_write(mydata, 'twitter_data/elonmusk_following.csv')
csv_write(mydata, "twitter_data/pualg_follwing.csv")
