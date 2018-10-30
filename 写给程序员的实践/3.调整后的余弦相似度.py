users = {"Amy": {"Taylor Swift": 4, "PSY": 3, "Whitney Houston": 4},
          "Ben": {"Taylor Swift": 5, "PSY": 2},
          "Clara": {"PSY": 3.5, "Whitney Houston": 4},
          "Daisy": {"Taylor Swift": 5, "Whitney Houston": 3}}


# 归一化，减去数据平均值的  余弦相似度

def new_cos(singer1,singer2,users):
    from math import sqrt
    avgs = {}
    #计算用户的乐队平均评分
    for name,ratings in users.items():
        avgs[name] = (float(sum(ratings.values())) / len(ratings.values()))

    num = 0
    dem1 = 0
    dem2 = 0

    for user,ratings in users.items():           #比对每个有这两个乐队的用户,有就进行修改后的余弦相似度累加       
        if singer1 in ratings and singer2 in ratings:
            avg = avgs[user]
            num += (ratings[singer1] - avg) * (ratings[singer2] - avg)
            dem1 += (ratings[singer1] - avg)**2
            dem2 += (ratings[singer2] - avg)**2
    
    return num / (sqrt(dem1)*sqrt(dem2))

print(new_cos("PSY","Taylor Swift",users))

