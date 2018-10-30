import pymysql

#连接数据库
db = pymysql.connect(host='127.0.0.1',user='root',passwd='root',database='sql学习',port=3306)

#获取游标执行sql
curs = db.cursor()

#sql 操作区

# 1查询所有信息
curs.execute('SELECT * from employee')

# 2插入语句
sql = "INSERT INTO employee(id, \
       name, gender, address) \
       VALUES ('%d', '%s', '%s', '%s')" % \
       (5, 'Mohan', 'man', 'beijing')


try:
   # 执行SQL语句
   curs.execute(sql)
   # 提交到数据库执行
   db.commit()
except:
   # 发生错误时回滚
   db.rollback()




    #读取执行结果

# 单条结果，元组形式返回的结果
# data = curs.fetchone()

# 所有结果，元组的元组形式返回的结果
data2 =curs.fetchall()


print(data2)
#关闭连接
db.close()