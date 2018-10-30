import pandas as pd
from math import sqrt

class recommender: #  数据  k的邻居    方法      最后推荐数
    def __init__(self,data,k=3,metric = "pearson",n=5):
        self.k = k
        self.n = n
        self.username2id = {}
        self.userid2name = {}
        self.productid2name = {}
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

                                                                                                    # K 近邻 算法:
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

users = {"Angelica": {"Blues Traveler": 3.5, "Broken Bells": 2.0,
                      "Norah Jones": 4.5, "Phoenix": 5.0,
                      "Slightly Stoopid": 1.5, "The Strokes": 2.5,
                      "Vampire Weekend": 2.0},
         "Bill":{"Blues Traveler": 2.0, "Broken Bells": 3.5,
                 "Deadmau5": 4.0, "Phoenix": 2.0,
                 "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0},
         "Chan": {"Blues Traveler": 5.0, "Broken Bells": 1.0,
                  "Deadmau5": 1.0, "Norah Jones": 3.0,
                  "Phoenix": 5, "Slightly Stoopid": 1.0},
         "Dan": {"Blues Traveler": 3.0, "Broken Bells": 4.0,
                 "Deadmau5": 4.5, "Phoenix": 3.0,
                 "Slightly Stoopid": 4.5, "The Strokes": 4.0,
                 "Vampire Weekend": 2.0},
         "Hailey": {"Broken Bells": 4.0, "Deadmau5": 1.0,
                    "Norah Jones": 4.0, "The Strokes": 4.0,
                    "Vampire Weekend": 1.0},
         "Jordyn":  {"Broken Bells": 4.5, "Deadmau5": 4.0,
                     "Norah Jones": 5.0, "Phoenix": 5.0,
                     "Slightly Stoopid": 4.5, "The Strokes": 4.0,
                     "Vampire Weekend": 4.0},
         "Sam": {"Blues Traveler": 5.0, "Broken Bells": 2.0,
                 "Norah Jones": 3.0, "Phoenix": 5.0,
                 "Slightly Stoopid": 4.0, "The Strokes": 5.0},
         "Veronica": {"Blues Traveler": 3.0, "Norah Jones": 5.0,
                      "Phoenix": 4.0, "Slightly Stoopid": 2.5,
                      "The Strokes": 3.0}
        }


# r = recommender(users,metric = "manhattan")    #曼哈顿算法   数据稠密
# r = recommender(users,metric = "pearson")     #皮尔逊算法    分数贬值
r = recommender(users,metric = "cos")           #余弦相似度算法     数据稀疏
print('根据习惯与你最相似的%d名用户,为你推荐:'%r.k,r.recommend("Jordyn")[0][0],"平均得分为:",r.recommend("Jordyn")[0][1])      