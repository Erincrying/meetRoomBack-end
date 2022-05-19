import pymysql
 
# 打开数据库连接(加入默认db，否则会找不到对应的db)
conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       passwd='ll961113',
                       db='lilin',
                       charset = 'utf8'
                       )
                
# 使用 cursor() 方法创建一个游标对象 cursor                      
cursor = conn.cursor()
 
# 使用 execute()  方法执行 SQL 查询
cursor.execute("show databases;")
sqlNum = "select stuNum from userdb where stuNum='2021122384'"
res = cursor.execute(sqlNum)
print(res, 'res')
cursor.execute("show databases;")

# cursor.execute("use database_name;")
# cursor.execute("show tables;")
# cursor.execute("select * from tables_name")
 
# 使用 fetchone() 方法获取单条数据;使用 fetchall() 方法获取所有数据
data = cursor.fetchall()
for item in data:
    print(item)
     
# 关闭数据库连接
cursor.close()