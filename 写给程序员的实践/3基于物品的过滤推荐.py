import pandas as pd
from math import sqrt

class recommender(): #  数据  k的邻居    方法      最后推荐数
    def __init__(self,data,k=3,metric = "pearson",n=5):
        self.k = k
        self.n = n
        #  Slope One 使用了频数和偏差两个变量
        self.frequencies = {}
        self.deviations = {}
        #保存使用的方法
        self.metric = metric
        if self.metric == "pearson":
            self.fn = self.pearson
        elif self.metric == "manhattan":
            self.fn = self.manhattan
        else:
            self.fn = self.cos


#如果数据是dict 
        if type(data).__name__ == "dict":
            self.data = data




#推荐系统设计：

    #计算 歌手之间的偏差矩阵
    def computeDeviations(self):
      #数据中的每个人:
      # 获得他们的评分
        for ratings in self.data.values():
         # for each item & rating in that set of ratings:
            for (item, rating) in ratings.items():                                                                   #拿到一个歌手的信息
                self.frequencies.setdefault(item, {})   # 频数如果item不存在  初始化为{}
                self.deviations.setdefault(item, {})    # 偏差          
                # for each item2 & rating2 in that set of ratings:
                for (item2, rating2) in ratings.items():                                                                #和其他歌手比对
                    if item != item2:
                        self.frequencies[item].setdefault(item2, 0)      #不存在就初始化
                        self.deviations[item].setdefault(item2, 0.0)
                        self.frequencies[item][item2] += 1                #存在就累加
                        self.deviations[item][item2] += rating - rating2     #偏差值
            
            for (item, ratings) in self.deviations.items():
                for item2 in ratings:
                    ratings[item2] /= self.frequencies[item][item2]         #实际中会出现多次 歌手一 与歌手二 进行对比产生偏差值   --》 总的偏差值/频数 平均一下


#基于slopeone算法进行 推荐(多个)
    def slopeOneRecommendations(self,userRatings):
        recommendations = {}
        frequencies = {}
        # 为每个项目和评级在用户的建议
        for (userItem, userRating) in userRatings.items():      #输入用户信息的  歌手 与 评价
            # 对于数据集中用户没有打分的每一项
            for (diffItem, diffRatings) in self.deviations.items():     #所有信息  歌手 对比歌手dict
                if diffItem not in userRatings and userItem in self.deviations[diffItem]:       #一个用户所没有的乐队，并且用户的乐队在对比表里
                    freq = self.frequencies[diffItem][userItem]     #所有信息里 同时拥有两个乐队的次数
                    recommendations.setdefault(diffItem, 0.0)
                    frequencies.setdefault(diffItem, 0)
                    # 加上表示分子的连续和的公式
                    recommendations[diffItem] += (diffRatings[userItem] + userRating) * freq  #推荐用户没有的乐队 = （偏差+评价）*次数
                    # 保持扩散项频率的运行和
                    frequencies[diffItem] += freq                                             #推荐该乐队的频数 = 该乐队对比的次数
        recommendations =  [(k,v / frequencies[k]) for (k, v) in recommendations.items()]    # 推荐 不同的乐队  和他们 slopeone 推荐值
        #最后排序返回
        recommendations.sort(key=lambda artistTuple: artistTuple[1],reverse = True)
        #我只会返回前50条建议
        return recommendations[:50]

#定义寻找最近用户的函数

    def getNeighbor(self,username):
        distances =[]
        for user in self.data:
            if user != username:
                distance = self.fn(self.data[username],self.data[user])  #求相似度
                distances.append((user,distance))
        
        distances.sort(key=lambda artistTuple: artistTuple[1], reverse=True)
        # print("邻居：",distances)
        return distances


#推荐函数

    def recommend(self,username):
        #拿到排好序的用户- 平均评价list
        recommendations = {}
        nearest = self.getNeighbor(username)         #拿到最接近的邻居
        #拿到用户评价
        userRatings = self.data[username]
        #计算总距离
        totalDistance = 0.0
        for i in range(self.k):
            totalDistance += nearest[i][1]
        
        
        #判断 如果 totaldistance = 负数  表示 负相关 此时 退出推荐
        if totalDistance < 0 :
            print("没有相似的人选可以推荐！")


        #现在遍历k个最近的邻居 累积评分
        for i in range(self.k):
            weight = nearest[i][1] / totalDistance  #计算该邻居评分 所占比例
            name = nearest[i][0]
            neighborRatings = self.data[name]
#             得到这个人的名字
#             找到该邻居没有打分的乐队
            for artist in neighborRatings:          #单个邻居的 评价表
                if not artist in userRatings:       #排除当前与当前用户重复的推荐
                    if artist not in recommendations:
                        recommendations[artist] = (neighborRatings[artist]*weight)   #第一次计算
                    else:
                        recommendations[artist] = (recommendations[artist] + neighborRatings[artist]*weight)  #拿到泛化平均的评分
        #现在从字典中列出清单，只得到前n项
        recommendations = list(recommendations.items())
        recommendations = [(k,v) for (k,v) in recommendations]
        recommendations.sort(key=lambda artistTuple: artistTuple[1], reverse=True)          #按泛化评分排序
        return recommendations[:self.n]

#皮尔逊相关系数(-1 - 1)

    def pearson(self,user1,user2):
        sum_xy = 0
        sum_x = 0
        sum_y = 0
        sum_x2 = 0
        sum_y2 = 0
        n = 0
        for key in user1:
            if key in user2:
                n +=1
                sum_xy += user1[key]*user2[key]
                sum_x += user1[key]
                sum_y += user2[key]
                sum_x2 += user1[key]**2
                sum_y2 += user2[key]**2

            #计算公分母
        denominator = sqrt(sum_x2-(sum_x**2/n))*sqrt(sum_y2-(sum_y**2/n))
        if denominator == 0:
            return 0
        else:
            return (sum_xy - (sum_x*sum_y)/n)/denominator



#曼哈顿距离
    def manhattan(self,x1,x2):
        distance = 0
        for n in x1:
            if n in x2:
                distance += abs(x1[n] - x2[n])
        return distance


#余弦相似度分析(-1 - 1)

    def cos(self,user1,user2):
        from math import sqrt
        sum_x2 = 0
        sum_y2 = 0
        sum_xy = 0
        for key in user1:
            if key in user2:
                x = user1[key]
                y = user2[key]
                sum_x2 += x*x
                sum_y2 += y*y
                sum_xy += x*y
        return  sum_xy / (sqrt(sum_x2) * sqrt(sum_y2))


#模拟1：

users = {"Amy": {"Taylor Swift": 4, "PSY": 3, "Whitney Houston": 4},
          "Ben": {"Taylor Swift": 5, "PSY": 2},
          "Clara": {"PSY": 3.5, "Whitney Houston": 4},
          "Daisy": {"Taylor Swift": 5, "Whitney Houston": 3}}


r = recommender(users)            
# print(r.recommend("Ben")) 
r.computeDeviations()
# print(r.deviations)
print(r.slopeOneRecommendations(users["Ben"]))
