# 1983年 David Chaum 提出加密技术用于现金的想法
# 拿到此纸条的人来我这里领取1美元， 人们如果相信我不会食言
# 并且我的签名不可伪造，就可以像银行汇票一样流通

import string
import random


def id_generator(size=10):
    chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
    return "".join(random.choice(chars) for _ in range(size))


def generate_tickes():
    given_away_tickets = []
    for i in range(3):
        given_away_tickets.append(id_generator())
    for ticket in given_away_tickets:
        print(ticket, " 拿着这个来我这里换1$")
    return given_away_tickets


def main():
    ticktes = generate_tickes()


if __name__ == "__main__":
    main()
