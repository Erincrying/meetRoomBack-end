#! encoding:utf-8
 
 

import flask,json,pymysql
import pandas as pd

import pymysql.cursors

from django.core.paginator import Paginator
 
# flask 一个服务
server=flask.Flask(__name__)
 
# 本地数据库方法
def Msqldb(sql):
    db = pymysql.connect(host = 'localhost', port = 3306, user = 'root', passwd = 'll961113', db='lilin', charset = 'utf8')
    cur = db.cursor()
    cur.execute(sql)
    # 判断sql语句是否select开头
    if sql.strip()[:6].upper() == 'SELECT':
        res = cur.fetchall()
    else:
        db.commit()
        res = 'OK'
    cur.close()
    db.close()
    return res
 
 # 本地数据库方法,返回字典(cursorclass=pymysql.cursors.DictCursor)
def MsqldbObject(sql):
    db = pymysql.connect(host = 'localhost', port = 3306, user = 'root', passwd = 'll961113', db='lilin',cursorclass=pymysql.cursors.DictCursor, charset = 'utf8')
    cur = db.cursor()
    cur.execute(sql)
    # 判断sql语句是否select开头
    if sql.strip()[:6].upper() == 'SELECT':
        res = cur.fetchall()
        #执行结果转化为dataframe
        # df = pd.DataFrame(list(res))
    else:
        db.commit()
        res = 'OK'
    cur.close()
    db.close()
    return res
# # 注册接口
# @server.route('/register',methods=['get','post'])
# def sigin():
#     # 获取接口传入的参数的值
#     username = flask.request.json.get("username")
#     pwd = flask.request.json.get("password")
#     sql = "select username from userinfo WHERE username=" + "'" + str(username) + "'"
#     res = Msqldb(sql)
#     name = str(res).replace("(('", "").replace("',),)", "")
#     if username and pwd:
#         if username == name:
#             res = {'Massges':'用户已存在！','ErrorCode':20300}
#         else:
#             insert_sql = "insert into userinfo(username,password) values("+ "'"+ str(username) + "'" + "," + "'" +str(pwd) + "'" + ")"
#             Msqldb(insert_sql)
#             res = {'Massges':'注册成功！','ErrorCode':0}
#     else:
#         res = {'Massges':'用户名或密码不能为空，请重新输入！','ErrorCode':20400}
#     return json.dumps(res,ensure_ascii=False)
 
# 登录接口
@server.route('/meetingRoom/login', methods=['post'])
def login():
    # print(flask.request.json, 'flask.request.json')
    # 获取接口传入的参数的值
    stuNum = flask.request.json.get("stuNum")
    password = flask.request.json.get("password")
    # print(stuNum, 'stuNum')
    # sql语句
    sqlNum = "select stuNum from userdb where stuNum=" + "'" + str(stuNum) + "'"
    sqlPwd = "select password from userdb where stuNum=" + "'" + str(stuNum) + "'"
    sqlUserId = "select userId from userdb where stuNum=" + "'" + str(stuNum) + "'"

    # print(sqlNum, 'sqlNum')
    # 数据库的值
    user = Msqldb(sqlNum)
    word =  Msqldb(sqlPwd)
    userId = Msqldb(sqlUserId)
    # print(user, 'user') # (('2021122384',),) user
    # print(word, 'word') # (('abcd1234',),) word
    # print(userId, 'userId') # (('01',),)

    # 取Value
    User = str(user).replace("(('", "").replace("',),)", "") # 2021122384
    Password = str(word).replace("(('", "").replace("',),)", "") # abcd1234
    userId = str(userId).replace("(('", "").replace("',),)", "") # 01
    # print(User, 'User')
    # print(Password, 'Password')
    
    if sqlNum and password: # 前端传了数据
        if User==stuNum and password==Password:
            user = {
              'stuNum': stuNum,
              'Password': password,
              'userId': userId
            }
            res = {
              'code': 200,
              'data': {
                'msg': '登录成功',
                'code': '0000',
                'data': {
                  'user': user,
                  'token': 'd787syv8dys8cas80d9s0a0d8f79ads56f7s4d56f879a8as89fd980s7dg'
                }
              }
            }
        elif User==stuNum and password!=Password:
            res = {
              'code': '9999',
              'message': '用户名或密码错误',
              'data': {}
            }
        # else:
        #     res = {"Massges": "用户未注册，请注册后登录！", "ErrorCode": 20022}
    else:
        res = {"Message": "用户名或密码不能为空，请重新输入！", "ErrorCode": 20032}
    return json.dumps(res, ensure_ascii=False)



# 获取用户信息接口
@server.route('/meetingRoom/getUserInfo', methods=['post'])
def getUserInfo():
    # 获取接口传入的参数的值
    userId = flask.request.json.get("userId")
    sqlUserId = "select * from userdb where userId=" + "'" + str(userId) + "'"
    # # 数据库的值
    # userInfo = Msqldb(sqlUserId) # (('李琳', '2021122384', '01', 'abcd1234'),)
    # userInfoStr = str(userInfo).replace("(", "").replace("),)", "") # '李琳', '2021122384', '01', 'abcd1234'
    # # 根据，切割出list
    # userInfoList = userInfoStr.split(',')
    # print(userInfoList, 'userInfoList') # ["'李琳'", " '2021122384'", " '01'", " 'abcd1234'"]
   
    # 数据库的值
    userInfo = MsqldbObject(sqlUserId) # [{'username': '李琳', 'stuNum': '2021122384', 'userId': '01', 'password': 'abcd1234'}]
    # print(len(userInfo), 'userInfo')
    if len(userInfo) == 1: # 查到了信息
      res = {
        'code': 200,
        'data': {
          'code': '0000',
          'message': '获取用户信息成功',
          'data': {
            'user': userInfo[0]
          }
        }
      }
    else:
      res = {
        'code': '9999',
        'message': '获取用户信息失败',
        'data': {}
      }

    return json.dumps(res, ensure_ascii=False)


# 会议室可预约列表查询
@server.route('/meetingRoom/list', methods=['post'])
def meetingRoomList():
    # 获取接口传入的参数的值
    # content = flask.request.json
    # print(content, 'content') # {'meetingRoomName': '', 'meetingRoomBuildingNum': '00', 'state': '00', 'orderTime': '2022-05-20', 'size': 10, 'page': 1}
    meetingRoomName = flask.request.json.get('meetingRoomName')
    meetingRoomBuildingNum = flask.request.json.get('meetingRoomBuildingNum')
    state = flask.request.json.get('state')
    orderTime = flask.request.json.get('orderTime')
    size = flask.request.json.get('size')
    page = flask.request.json.get('page')

    

    # sqlList语句
    # sqlList = "select * from meetingroomdb"
    sqlList = "select * from meetingroomdb where meetingRoomName like" + "'%" + str(meetingRoomName) + "%'" # 模糊查询meetingRoomName
    # sqlList = sqlList + "and meetingRoomBuildingNum=" + "'" + str(meetingRoomBuildingNum) + "'" + "and state=" + "'" + str(state) + "'"
    # 条件查询
    if state != '': # 状态不是是全部
      sqlList = sqlList + "and state=" + "'" + str(state) + "'"
    if meetingRoomBuildingNum != '00': # meetingRoomBuildingNum不是全部
      sqlList = sqlList + "and meetingRoomBuildingNum=" + "'" + str(meetingRoomBuildingNum) + "'"

    print(sqlList, 'sqlList')
    # 数据库的值
    meetingRoomList = MsqldbObject(sqlList)
    # print(meetingRoomList, 'meetingRoomList')
    # print(len(meetingRoomList), 'meetingRoomList')
    # paginator.count：返回所有记录的总数量
    # paginator.num_pages：返回分页后的总页数
    # paginator.page_range：返回分页后的页码范围，一个range对象
    paginator = Paginator(meetingRoomList, size)
    current_page_num = int(page)
    page_obj = paginator.page(current_page_num)
    currentList = page_obj.object_list
    # print(currentList, 'currentList')
    # print(type(currentList), 'type') # list

    if len(meetingRoomList) >= 0: # 查到了信息
      res = {
        'code': 200,
        'data': {
          'code': '0000',
          'message': 'success',
          'data': {
            'page': page,
            'size': size,
            'list': currentList,
            'total': paginator.count,
            'totalPages': paginator.num_pages
          }
        }
      }
    else:
      res = {
        'code': '9999',
        'message': '获取会议室列表失败',
        'data': {
          'list': [],
        }
      }

    return json.dumps(res, ensure_ascii=False)
# 本地服务端口号
server.run(port=9090,debug=True,host='localhost')