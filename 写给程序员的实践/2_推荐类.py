import pandas as pd





class recommender:
    def __init__(self,data,k=1,metric = "pearson",n = 5):
        self.k = k
        self.n = n
        self.username2id = {}
        self.userid2name = {}
        self.productid2name = {}
#保存使用的方法
        self.metric = metric
        if self.metric == "pearson":
            self.fn = self.pearson

#如果数据是dict 
    if type(data).__name__ == "dict":
        self.data = data

 #给定产品id号返回产品名称       
    def convertprodunctID2name(self,id):
        if id in self.productid2name:
            return self.productid2name[id]
        else:
            return id

#返回带有id的用户的最高评级
    def userRatings(self,id,n):
        print("Rating for :" + self.userid2name[id])
        ratings = self.data[id]
        print(len(ratings)

        ratings = list(ratings.items())
        ratings = [(self.convertprodunctID2name(k),v for (k,v) in ratings)]

        ratings.sort(key = lambda a : a[1] ,reverse =True)
        ratings = ratings[:n]
        for rating in ratings:
            print(rating[0],rating[1])      #返回n个排好序的 用户-评价

#加载表    
    def loadBookDB(self,path =""):
        self.data = {}
        i = 0
    #加载 用户-评价表
        df = pd.read_csv( path + "BX-Book-Ratings.csv",delimiter="\;",engine='python')
        df.columns = ["user","book","rating"]


            
        