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
    db = pymysql.connect(host = 'localhost', port = 3306, user = 'root', passwd = 'll961113', db='lilin', cursorclass=pymysql.cursors.DictCursor, charset = 'utf8')
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

# 本地数据库插入方法
def insertData(data, table): # data为对应的字典
  db = pymysql.connect(host = 'localhost', port = 3306, user = 'root', passwd = 'll961113', db='lilin', cursorclass=pymysql.cursors.DictCursor, charset = 'utf8')
  cur = db.cursor()
  # 根据数据库自动配对键值对
  table = table
  keys = ', '.join(data.keys())
  values = ', '.join(['%s'] * len(data))
  sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
  try:
    cur.execute(sql, tuple(data.values()))
    # print('Successful')
    res = 'Successful'
    db.commit()
  except:
    # print('Failed')
    db.rollback()
    res = 'Failed'
  cur.close()
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


# 会议室列表查询
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

    # 判断预约的这个会议室，是否一天中的三个时间段都被预约，更新state
    # 先获取原始的会议室列表
    sqlOriginalList = "select * from meetingroomdb"
    originalList = MsqldbObject(sqlOriginalList)
    # 拿到所有数据的meetingRoomId
    meetingRoomIdList= []
    for item in originalList:
      # print(item, 'item') # {'meetingRoomId': 23, 'meetingRoomName': '506', 'meetingRoomBuildingNum': '01', 'meetingRoomBuildingName': '行政楼', 'state': '00'} item
      # #获取key值,value值
      for key, value in item.items():
        # print(key, value)
        if key == 'meetingRoomId':
          meetingRoomIdList.append(value)
          break
    # print(meetingRoomIdList, 'meetingRoomIdList') # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    for roomId in meetingRoomIdList:
      # 当前房间id对应在orderlist，在当前日期下的预约记录数目
      sqlOrderRoom = "select * from orderlist where meetingRoomId=" + "'" + str(roomId) + "'" + "and orderTime=" + "'" + str(orderTime) + "'" 
      roomOrderList = MsqldbObject(sqlOrderRoom)
      # print(len(roomOrderList), 'roomOrderList')
      if len(roomOrderList) == 3: # 当前房间在当前日期下预约了三次
        # 更新对应state
        sqlUpdate = "update meetingroomdb set state='01' where meetingRoomId=" + "'" + str(roomId) + "'"
      else:
        sqlUpdate = "update meetingroomdb set state='00' where meetingRoomId=" + "'" + str(roomId) + "'"
      updateRes = MsqldbObject(sqlUpdate)
      # print(updateRes, 'updateRes')

    # 正常条件查询
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


# 预约会议室接口
@server.route('/meetingRoom/orderRoom', methods=['post'])
def orderRoom():
    # 获取接口传入的参数的值
    content = flask.request.json
    # print(content, 'content') #{'meetingRoomId': 1, 'meetingRoomName': '202', 'meetingRoomBuildingNum': '08', 'meetingRoomBuildingName': '8号教学楼', 'state': '00', 'operator': '李琳', 'orderTime': '2022-05-20', 'orderConcreteTime': '03'}
    meetingRoomId = flask.request.json.get('meetingRoomId')
    # meetingRoomName = flask.request.json.get('meetingRoomName')
    # meetingRoomBuildingNum = flask.request.json.get('meetingRoomBuildingNum')
    # meetingRoomBuildingName = flask.request.json.get('meetingRoomBuildingName')
    orderTime = flask.request.json.get('orderTime')
    orderConcreteTime = flask.request.json.get('orderConcreteTime')
    # operator = flask.request.json.get('operator')
    # 重复时间预约会议室判断
    sqlOrderedRoom = "select orderConcreteTime from orderlist where meetingRoomId=" + "'" + str(meetingRoomId) + "'" + "and orderTime=" + "'" + str(orderTime) + "'" + "and orderConcreteTime=" + "'" + str(orderConcreteTime) + "'"
    orderedRoomList = MsqldbObject(sqlOrderedRoom)
    # print(len(orderedRoomList), 'len(orderedRoomList)')
    if (len(orderedRoomList)): # 这个时间段的会议室已经被预约
      res = {
        'code': '9999',
        'message': '您选择的时间段已经被预约过了！',
        'data': {}
      }
    else:
      content.pop('state') # 去除字典重复元素
      insertRes = insertData(content, 'orderlist') #INSERT INTO orderlist(meetingRoomId, meetingRoomName, meetingRoomBuildingNum, meetingRoomBuildingName, operator, orderTime, orderConcreteTime) VALUES (%s, %s, %s, %s, %s, %s, %s) sql 
      if insertRes == 'Successful': # 插入成功
        res = {
          'code': 200,
          'data': {
            'code': '0000',
            'message': 'success',
            'data': {}
          }
        }
      else:
        res = {
          'code': '9999',
          'message': '会议室预约失败！',
          'data': {}
        }
    return json.dumps(res, ensure_ascii=False)


# 预约记录列表
@server.route('/meetingRoom/orderlist', methods=['post'])
def orderlist():
    content = flask.request.json
    print(content, 'content') # {'meetingRoomName': '', 'meetingRoomBuildingNum': '00', 'orderTime': '2022-05-21', 'size': 10, 'page': 1, 'operator': '李琳'}
    meetingRoomName = flask.request.json.get('meetingRoomName')
    meetingRoomBuildingNum = flask.request.json.get('meetingRoomBuildingNum')
    orderTime = flask.request.json.get('orderTime')
    operator =  flask.request.json.get('operator')
    size = flask.request.json.get('size')
    page = flask.request.json.get('page')

    # sqlList语句
    sqlList = "select * from orderlist where meetingRoomName like" + "'%" + str(meetingRoomName) + "%'" # 模糊查询meetingRoomName
    

    # 条件查询（楼栋选择）
    if meetingRoomBuildingNum != '00': # meetingRoomBuildingNum不是全部
      sqlList = sqlList + "and meetingRoomBuildingNum=" + "'" + str(meetingRoomBuildingNum) + "'"
    if orderTime: # 选择了具体时间
      sqlList = sqlList + "and orderTime=" + "'" + str(orderTime) + "'" # 预约时间查询
    # 对操作人的过滤
    sqlList = sqlList + "and operator=" + "'" + str(operator) + "'"

    # print(sqlList, 'sqlList')
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
        'message': '获取会议室预约记录失败',
        'data': {
          'list': [],
        }
      }
    return json.dumps(res, ensure_ascii=False)


# 取消预约会议室接口
@server.route('/meetingRoom/cancelOrderRoom', methods=['post'])
def cancelOrderRoom():
    # 获取接口传入的参数的值
    content = flask.request.json
    print(content, 'content') # {'orderId': 5, 'meetingRoomName': '202', 'meetingRoomBuildingNum': '08', 'meetingRoomBuildingName': '8号教学楼', 'orderTime': '2022-05-21', 'orderConcreteTime': '03', 'meetingRoomId': 1, 'operator': '李琳', 'canCancelOrderFlag': True
    orderId = flask.request.json.get('orderId')
    
    sqlDelete = "delete from orderlist where orderId=" + "'" + str(orderId) + "'"
    deleteRes = MsqldbObject(sqlDelete)
    print(deleteRes, 'deleteRes')
    if deleteRes == 'OK':
      res = {
        'code': 200,
        'data': {
          'code': '0000',
          'message': 'success',
          'data': {}
        }
      }
    else:
      res = {
        'code': '9999',
        'message': '取消预约失败！',
        'data': {}
      }
    return json.dumps(res, ensure_ascii=False)



# 本地服务端口号
server.run(port=9090,debug=True,host='localhost')