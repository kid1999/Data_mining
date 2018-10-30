users = {"Angelica": {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0},
         "Bill":{"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0},
         "Chan": {"Blues Traveler": 5.0, "Broken Bells": 1.0, "Deadmau5": 1.0, "Norah Jones": 3.0, "Phoenix": 5, "Slightly Stoopid": 1.0},
         "Dan": {"Blues Traveler": 3.0, "Broken Bells": 4.0, "Deadmau5": 4.5, "Phoenix": 3.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 2.0},
         "Hailey": {"Broken Bells": 4.0, "Deadmau5": 1.0, "Norah Jones": 4.0, "The Strokes": 4.0, "Vampire Weekend": 1.0},
         "Jordyn":  {"Broken Bells": 4.5, "Deadmau5": 4.0, "Norah Jones": 5.0, "Phoenix": 5.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 4.0},
         "Sam": {"Blues Traveler": 5.0, "Broken Bells": 2.0, "Norah Jones": 3.0, "Phoenix": 5.0, "Slightly Stoopid": 4.0, "The Strokes": 5.0},
         "Veronica": {"Blues Traveler":3.0, "Norah Jones": 5.0, "Phoenix": 4.0, "Slightly Stoopid": 2.5, "The Strokes": 3.0}
        }

# print(users['Bill'])

#计算曼哈顿距离
def manhattan(x1,x2):
    distance = 0
    for n in x1:
        if n in x2:
            distance += abs(x1[n] - x2[n])
    return distance

# print(manhattan(users["Bill"],users['Sam']))

#定义寻找最近用户的函数

def getNeighbor(username,users):
    distances =[]
    for user in users:
        if user != username:
            distance = manhattan(users[username],users[user])
            distances.append((distance,user))
    
    distances.sort()
    return distances

# print(getNeighbor("Sam",users))

#推荐函数

def recommend(username,users):
    nearest = getNeighbor(username,users)[0][1]         #拿到最接近的邻居
    recommendations = []
    neighbor = users[nearest]
    user = users[username]

    for artist in neighbor:
        if not artist in user:
            recommendations.append((artist,neighbor[artist]))

    return sorted(recommendations, key=lambda artistTuple: artistTuple[1], reverse=True)


print('最邻近的是: ',getNeighbor("Veronica",users)[0])
print("基于他的推荐是:",recommend("Veronica",users))

#皮尔逊相关系数(-1 - 1)

def pearson(user1,user2):
    from math import sqrt
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

print("皮尔逊相关系数",pearson(users["Veronica"],users["Hailey"]))


#余弦相似度分析(-1 - 1)

def cos(user1,user2):
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

# print("余弦相似度:",cos(users["Veronica"],users["Hailey"]))




#  伪 k-近邻算法


def k_mean(username,users,k):
    from collections import Counter
    movie = []
    score = {}
    user = getNeighbor(username,users)[:k]
    for name in user:
        people = name[1]
        for k,v in users[people].items():
            if score.get(k):
                score[k] = 0
            else:
                score[k] += v
            movie.append(k)
    count = Counter(movie)
    print(count)
    print(movie)
        



        

# k_mean("Sam",users,3)