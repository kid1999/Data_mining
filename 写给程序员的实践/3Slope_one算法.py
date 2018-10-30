users = {"Amy": {"Taylor Swift": 4, "PSY": 3, "Whitney Houston": 4},
          "Ben": {"Taylor Swift": 5, "PSY": 2},
          "Clara": {"PSY": 3.5, "Whitney Houston": 4},
          "Daisy": {"Taylor Swift": 5, "Whitney Houston": 3}}


#利用 乐队之间的偏差 推荐
def Slope_One(singer1,singer2,users):
    num = 0
    dev = 0
    for user,ratings in users.items():           #比对每个有这两个乐队的用户,有就进行偏差累加  最后求平均偏差    
        if singer1 in ratings and singer2 in ratings:
            num +=1
            dev += users[user][singer1] - users[user][singer2]
    print("偏差值:",dev/num)
    return dev/num

# print(Slope_One("PSY","Taylor Swift",users))


#  加权预测
def commender(username,data):
    singer1 = list(users["Amy"].keys())[0]    #将user的第一个歌手作为已知项  求其他未知
    singer1_value = list(users["Amy"].values())[0]
    ratings = {}
    for name in data:
        if name != username:
            for singer in data[name]:
                if not singer in data[username]:
                    ratings[singer] = Slope_One(singer1,singer,data) + singer1_value
    return ratings

print(commender("Ben",users))  


 