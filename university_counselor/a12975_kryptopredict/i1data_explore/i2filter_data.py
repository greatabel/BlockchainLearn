from csv_operation import csv_reader, csv_write
from itertools import groupby
import json


movies = csv_reader("paulg.csv", "twitter_data")
print("1sample", movies[0], "#" * 10, movies[1][12])


# i0_2 = 0
# i2_4 = 0
# i4_6 = 0
# i6_7 = 0
# i7_8 = 0
# year_revenue = []
for movie in movies:
    time = movie[2]
    i_str = movie[12]
    # print(i_str, type(i_str))
    if i_str not in ("[]", "mentions"):
        i_str = i_str.replace("'", '"')
        t = json.loads(i_str)
        print("name=paulg,name=" + t[0]["screen_name"] + ",'" + time[:16] + "'")
        # name=elonmusk,name=@WholeMarsBlog,'2015-12-07 22:38'

# 	for t in tlist:
# 		name = t['name']
# 		if movie['vote_average'] is not None:
# 			vote_count = float(movie['vote_average'])
# 			if vote_count < 2:
# 				i0_2 += 1
# 			if vote_count >= 2 and vote_count < 4:
# 				i2_4 += 1
# 			if vote_count >= 4 and vote_count < 6:
# 				i4_6 += 1
# 			if vote_count >= 6 and vote_count < 7:
# 				i6_7 += 1
# 			if vote_count >= 7 and vote_count < 8:
# 				i7_8 += 1
# 		else:
# 			vote_count = 0
# 		# print(year, revenue)
# 		item = [name, vote_count]
# 		year_revenue.append(item)
