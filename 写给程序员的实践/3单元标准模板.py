import codecs 
from math import sqrt

users2 = {"Amy": {"Taylor Swift": 4, "PSY": 3, "Whitney Houston": 4},
          "Ben": {"Taylor Swift": 5, "PSY": 2},
          "Clara": {"PSY": 3.5, "Whitney Houston": 4},
          "Daisy": {"Taylor Swift": 5, "Whitney Houston": 3}}

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



class recommender:

   def __init__(self, data, k=1, metric='pearson', n=5):
                """ 初始化推荐
            目前，如果数据是字典，那么推荐者将被初始化
            到它。
            对于所有其他数据类型的数据，不发生初始化
            k是k最近邻的k值
            metric是使用的距离公式
            n是建议的最大数量"""
      self.k = k
      self.n = n
      self.username2id = {}
      self.userid2name = {}
      self.productid2name = {}
      #
      #  Slope One 使用了频数和偏差两个变量
      # 
      self.frequencies = {}
      self.deviations = {}
      # 选择方法
      self.metric = metric
      if self.metric == 'pearson':
         self.fn = self.pearson
      #
      # 如果数据是字典集推荐数据给它
      #
      if type(data).__name__ == 'dict':
         self.data = data

   def convertProductID2name(self, id):
      """给定产品id号返回产品名称"""
      if id in self.productid2name:
         return self.productid2name[id]
      else:
         return id


   def userRatings(self, id, n):
      """返回带有id的用户的最高评级"""
      print ("Ratings for " + self.userid2name[id])
      ratings = self.data[id]
      print(len(ratings))
      ratings = list(ratings.items())[:n]
      ratings = [(self.convertProductID2name(k), v)
                 for (k, v) in ratings]
      # 最后排序返回
      ratings.sort(key=lambda artistTuple: artistTuple[1],
                   reverse = True)      
      for rating in ratings:
         print("%s\t%i" % (rating[0], rating[1]))


   def showUserTopItems(self, user, n):
      """为用户显示前n项"""
      items = list(self.data[user].items())
      items.sort(key=lambda itemTuple: itemTuple[1], reverse=True)
      for i in range(n):
         print("%s\t%i" % (self.convertProductID2name(items[i][0]),
                           items[i][1]))
            
   def loadMovieLens(self, path=''):
      self.data = {}
      #
      # first load movie ratings
      #
      i = 0
      #
      # First load book ratings into self.data
      #
      #f = codecs.open(path + "u.data", 'r', 'utf8')
      f = codecs.open(path + "u.data", 'r', 'ascii')
      #  f = open(path + "u.data")
      for line in f:
         i += 1
         #separate line into fields
         fields = line.split('\t')
         user = fields[0]
         movie = fields[1]
         rating = int(fields[2].strip().strip('"'))
         if user in self.data:
            currentRatings = self.data[user]
         else:
            currentRatings = {}
         currentRatings[movie] = rating
         self.data[user] = currentRatings
      f.close()
      #
      # Now load movie into self.productid2name
      # the file u.item contains movie id, title, release date among
      # other fields
      #
      #f = codecs.open(path + "u.item", 'r', 'utf8')
      f = codecs.open(path + "u.item", 'r', 'iso8859-1', 'ignore')
      #f = open(path + "u.item")
      for line in f:
         i += 1
         #separate line into fields
         fields = line.split('|')
         mid = fields[0].strip()
         title = fields[1].strip()
         self.productid2name[mid] = title
      f.close()
      #
      #  Now load user info into both self.userid2name
      #  and self.username2id
      #
      #f = codecs.open(path + "u.user", 'r', 'utf8')
      f = open(path + "u.user")
      for line in f:
         i += 1
         fields = line.split('|')
         userid = fields[0].strip('"')
         self.userid2name[userid] = line
         self.username2id[line] = userid
      f.close()
      print(i)




   def loadBookDB(self, path=''):
      """loads the BX book dataset. Path is where the BX files are
      located"""
      self.data = {}
      i = 0
      #
      # First load book ratings into self.data
      #
      f = codecs.open(path + "u.data", 'r', 'utf8')
      for line in f:
         i += 1
         # separate line into fields
         fields = line.split(';')
         user = fields[0].strip('"')
         book = fields[1].strip('"')
         rating = int(fields[2].strip().strip('"'))
         if rating > 5:
            print("EXCEEDING ", rating)
         if user in self.data:
            currentRatings = self.data[user]
         else:
            currentRatings = {}
         currentRatings[book] = rating
         self.data[user] = currentRatings
      f.close()
      #
      # Now load books into self.productid2name
      # Books contains isbn, title, and author among other fields
      #
      f = codecs.open(path + "BX-Books.csv", 'r', 'utf8')
      for line in f:
         i += 1
         # separate line into fields
         fields = line.split(';')
         isbn = fields[0].strip('"')
         title = fields[1].strip('"')
         author = fields[2].strip().strip('"')
         title = title + ' by ' + author
         self.productid2name[isbn] = title
      f.close()
      #
      #  Now load user info into both self.userid2name and
      #  self.username2id
      #
      f = codecs.open(path + "BX-Users.csv", 'r', 'utf8')
      for line in f:
         i += 1
         # separate line into fields
         fields = line.split(';')
         userid = fields[0].strip('"')
         location = fields[1].strip('"')
         if len(fields) > 3:
            age = fields[2].strip().strip('"')
         else:
            age = 'NULL'
         if age != 'NULL':
            value = location + '  (age: ' + age + ')'
         else:
            value = location
         self.userid2name[userid] = value
         self.username2id[location] = userid
      f.close()
      print(i)
                
        
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


   def slopeOneRecommendations(self, userRatings):
      recommendations = {}
      frequencies = {}
      # 为每个项目和评级在用户的建议
      for (userItem, userRating) in userRatings.items():
         # 对于数据集中用户没有打分的每一项
         for (diffItem, diffRatings) in self.deviations.items():
            if diffItem not in userRatings and userItem in self.deviations[diffItem]:
               freq = self.frequencies[diffItem][userItem]
               recommendations.setdefault(diffItem, 0.0)
               frequencies.setdefault(diffItem, 0)
               # 加上表示分子的连续和的公式
               recommendations[diffItem] += (diffRatings[userItem] +
                                             userRating) * freq
               # 保持扩散项频率的运行和
               frequencies[diffItem] += freq
      recommendations =  [(self.convertProductID2name(k),
                           v / frequencies[k])
                          for (k, v) in recommendations.items()]
      #最后排序返回
      recommendations.sort(key=lambda artistTuple: artistTuple[1],
                           reverse = True)
      #我只会返回前50条建议
      return recommendations[:50]
        
   def pearson(self, rating1, rating2):
      sum_xy = 0
      sum_x = 0
      sum_y = 0
      sum_x2 = 0
      sum_y2 = 0
      n = 0
      for key in rating1:
         if key in rating2:
            n += 1
            x = rating1[key]
            y = rating2[key]
            sum_xy += x * y
            sum_x += x
            sum_y += y
            sum_x2 += pow(x, 2)
            sum_y2 += pow(y, 2)
      if n == 0:
         return 0
      # now compute denominator
      denominator = sqrt(sum_x2 - pow(sum_x, 2) / n) * \
                    sqrt(sum_y2 - pow(sum_y, 2) / n)
      if denominator == 0:
         return 0
      else:
         return (sum_xy - (sum_x * sum_y) / n) / denominator


   def computeNearestNeighbor(self, username):
      """creates a sorted list of users based on their distance
      to username"""
      distances = []
      for instance in self.data:
         if instance != username:
            distance = self.fn(self.data[username],
                               self.data[instance])
            distances.append((instance, distance))
      # sort based on distance -- closest first
      distances.sort(key=lambda artistTuple: artistTuple[1],
                     reverse=True)
      return distances

   def recommend(self, user):
      """Give list of recommendations"""
      recommendations = {}
      # first get list of users  ordered by nearness
      nearest = self.computeNearestNeighbor(user)
      #
      # now get the ratings for the user
      #
      userRatings = self.data[user]
      #
      # determine the total distance
      totalDistance = 0.0
      for i in range(self.k):
         totalDistance += nearest[i][1]
      # now iterate through the k nearest neighbors
      # accumulating their ratings
      for i in range(self.k):
         # compute slice of pie 
         weight = nearest[i][1] / totalDistance
         # get the name of the person
         name = nearest[i][0]
         # get the ratings for this person
         neighborRatings = self.data[name]
         # get the name of the person
         # now find bands neighbor rated that user didn't
         for artist in neighborRatings:
            if not artist in userRatings:
               if artist not in recommendations:
                  recommendations[artist] = neighborRatings[artist] * \
                                            weight
               else:
                  recommendations[artist] = recommendations[artist] + \
                                            neighborRatings[artist] * \
                                            weight
      # now make list from dictionary and only get the first n items
      recommendations = list(recommendations.items())[:self.n]
      recommendations = [(self.convertProductID2name(k), v)
                         for (k, v) in recommendations]
      # finally sort and return
      recommendations.sort(key=lambda artistTuple: artistTuple[1],
                           reverse = True)
      return recommendations
