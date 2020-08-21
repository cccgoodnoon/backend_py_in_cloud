# coding:utf-8
import psycopg2
from flask import Flask, jsonify, request, send_file, send_from_directory, make_response, Response, json, session
from flask_cors import CORS
import uuid
import psycopg2.extras
import flask_excel as excel
from pyexcel_xlsx import save_data
import os
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, func
from sqlalchemy.dialects.postgresql import Any
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Date, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base
from model import TiSecModel
from model import TiNodeModel
from model import TiTaskModel
import jwt, datetime, time
import urllib.request
from werkzeug.utils import secure_filename

SECRET_KEY = "users"

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'

CORS(app)

host = '47.111.234.116'
port = '5432'
username = 'postgres'
password = 'tongji2020'
database = 'postgres'
dd = 'postgresql://{}:{}@{}:{}/{}'.format(username, password, host, port, database)

UPLOAD_FOLDER = 'D:/uploads'
# UPLOAD_FOLDER = '/var/upload'

ALLOWED_EXTENSIONS = set(
    ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'mp4', 'zip', 'rar'])

conn = psycopg2.connect(
    database="postgres", user="postgres", password="tongji2020", host="47.111.234.116", port="5432")


engine = create_engine(dd)
Base = declarative_base(engine)
Session = sessionmaker(bind=engine)
ss = Session()


# ---------------------------------------------------------------------------------------------------
#
#  活动 增删改查
#
# ---------------------------------------------------------------------------------------------------

@app.route('/api/u/activity', methods=['POST'])
def create_activity():
    psycopg2.extras.register_uuid()
    cur = conn.cursor()
    data = request.get_json()
    print(data)
    print(data['objectvalue'])
    data['timeValue'] = time.strftime('%Y-%m-%d %H:%M:%S')
    cur.execute(
        "insert into appl1011(uuid, courseid, credit, memberid, begintime, objectstate) values(%s,%s,%s,%s,%s,%s)",
        (uuid.uuid1(), data['course_uuid'], data['course_credit'], data['member_uuid'], data['timeValue'],
         data['objectvalue']))
    conn.commit()
    return "1"


@app.route('/api/u/activity/<mid>', methods=['GET'])
def read_one_activity(mid):
    cur = conn.cursor()
    tmp_mid = "'" + mid + "'"
    print(mid)
    cur.execute(
        "select id,uuid,courseid,objectstate from appl1011 where memberid={}".format(tmp_mid))
    rows = cur.fetchall()
    print("该老师有这些课", rows)
    l = []
    # course =[]
    for i, row in enumerate(rows):
        # dic= {'courseid': str(rows[i][0]),'objectstate': int(rows[i][1])}
        id = str(rows[i][0])
        uuid = str(rows[i][1])
        courseid = str(rows[i][2])
        objectstate = int(rows[i][3])
        print(courseid, objectstate)  # ok
        a = "'" + courseid + "'"
        cur.execute("select code,name from mast1014 where uuid={}".format(a))
        courses = cur.fetchall()
        print(courses, 111)
        code = str(courses[0][0])
        name = str(courses[0][1])
        print(code, name)
        cour = {'id': id, 'uuid': uuid, 'code': code, 'name': name, 'objectstate': objectstate}
        print(cour)
        l.append(cour)
        print("----------------")
    print(l)
    return jsonify(l)


@app.route('/api/u/activity/<uuid>', methods=['DELETE'])
def delete_act(uuid):
    cur = conn.cursor()
    # cur.execute("select uuid from mast1014 where name='{}'".format(name))
    # course_uuid = cur.fetchall()
    # print(str(course_uuid[0][0]))
    # course_id = "'"+ str(course_uuid[0][0]) +"'"
    tmp_uuid = "'" + uuid + "'"
    cur.execute("DELETE from appl1011 where uuid={}".format(tmp_uuid))
    conn.commit()
    return "1"


@app.route('/api/u/activity/state/<string:id>', methods=['PUT'])
def update_one_activity_state(id):
    cur = conn.cursor()
    data = request.get_json()
    print(data)
    cur.execute("UPDATE appl1011 SET objectstate = '{}' WHERE id = {}"
                .format(data['state'], id))
    conn.commit()
    return "1"


@app.route('/api/u/activity/<string:id>', methods=['PUT'])
def update_one_activity(id):
    cur = conn.cursor()
    data = request.get_json()

    cur.execute(
        "UPDATE APPL1011 SET uuid = '{}', memberid = '{}', courseid = '{}', begintime = '{}', endtime = '{}', workday = '{}' ,workpoint = '{}' WHERE id = {}"
            .format(data['uuid'], data['memberid'], data['courseid'], data['begintime'], data['endtime'],
                    data['workday'],
                    data['workpoint'], id))

    conn.commit()
    return "1"


@app.route('/api/u/activity/<string:id>', methods=['DELETE'])
def delete_one_activity(id):
    cur = conn.cursor()
    # cur.execute("DELETE from tasktwo where id=%s", id)
    cur.execute("DELETE from APPL1011 where id=" + id)
    conn.commit()
    return "1"


# ---------------------------------------------------------------------------------------------------
#
#  人员 增删改查
#
# ------------------------------------------------------------------------------------------------------------

@app.route('/api/u/member', methods=['GET'])
def read_member():
    cur = conn.cursor()
    cur.execute(
        "select * from mast0501")
    rows = cur.fetchall()
    l = []
    for row in rows:
        # print(row)
        dic = {'id': str(row[0]), 'employeeid': str(row[14]), 'firstname': str(row[5]), 'uuid': str(row[1]),
               'objectstate': str(row[27])}
        l.append(dic)
    return jsonify(l)


@app.route('/api/u/member/<id>', methods=['GET'])
def read_one_member(id):
    cur = conn.cursor()
    cur.execute(
        "select * from mast0501 where id = {}".format(id))
    rows = cur.fetchall()
    l = []
    for row in rows:
        # print(row)
        dic = {'id': str(row[0]), 'employeeid': str(row[14]), 'firstname': str(row[5]), 'uuid': str(row[1]),
               'objectstate': str(row[27])}
        l.append(dic)
    return jsonify(l)


# ---------------------------------------------------------------------------------------------------
#
#  课程 增删改查
#
# ---------------------------------------------------------------------------------------------------


@app.route('/api/u/course', methods=['GET'])
def read_course():
    cur = conn.cursor()
    cur.execute(
        "select * from mast1014")
    rows = cur.fetchall()
    l = []
    for row in rows:
        # print(row)
        dic = {'id': str(row[0]), 'code': str(row[3]), 'name': str(row[5]), 'uuid': str(row[22]), 'credit': str(row[9]),
               'objectstate': str(row[16])}
        l.append(dic)
    return jsonify(l)


@app.route('/api/u/course/<id>', methods=['GET'])
def read_one_course(id):
    cur = conn.cursor()
    cur.execute(
        "select * from mast1014 where id = {}".format(id))
    rows = cur.fetchall()
    l = []
    for row in rows:
        # print(row)
        dic = {'id': str(row[0]), 'code': str(row[3]), 'name': str(row[5]), 'uuid': str(row[22]), 'credit': str(row[9])}
        l.append(dic)
    return jsonify(l)


# ---------------------------------------------------------------------------------------------------------------
#
# 任务 增删改查
#
# ---------------------------------------------------------------------------------------------------------------


@app.route('/api/admin/task/tasks', methods=['GET'])
def read_all_admin_tasks():
    # cur = conn.cursor()
    # cur.execute(
    #     "select * from taskthree")
    # rows = cur.fetchall()
    # l = []
    # for row in rows:
    #     print(row)
    #     dic= {'id': str(row[0]),'description': str(row[1]),'begintime':str(row[2]),'endtime':str(row[3]),'performer':str(row[4]),'state':str(row[5]),'title':str(row[6])}
    #     l.append(dic)
    # return jsonify(l)
    selected_list = []
    result = ss.query(TiTaskModel).all()
    for i in result:
        expbegindate = i.expbegindate.strftime('%Y-%m-%d')
        expenddate = i.expenddate.strftime('%Y-%m-%d')
        t = {'id': i.id, 'uuid': i.uuid, 'description': i.description, 'begintime': expbegindate, 'endtime': expenddate,
             'performer': i.executorname, 'title': i.title, 'state': i.objectstate, 'nodeid': i.nodeid}
        # nodeid 是 parent ,传到前端
        selected_list.append(t)
    # return jsonify(selected_list)
    return Response(json.dumps(selected_list), mimetype='application/json')


@app.route('/api/admin/task/tasks/<string:id>', methods=['GET'])
def read_one_admin_task(id):
    cur = conn.cursor()
    cur.execute(
        "select * from tran0823 where id=" + id)
    rows = cur.fetchall()
    l = []
    for row in rows:
        # print(row)
        dic = {'id': str(row[0]), 'description': str(row[14]), 'begintime': str(row[23]), 'endtime': str(row[24]),
               'performer': str(row[7]), 'state': str(row[18]), 'title': str(row[13]), 'nodeid': str(row[15])}
        l.append(dic)
    return jsonify(dic)
    # o = ss.query(TiTaskModel).get(id)
    # ss.close()
    # return o


#  select * from taskthree where begintime >=  and endtime < '2015-08-15';
# @app.route('/api/admin/task/tasks/new',methods=['POST'])
# def create_task():
#     data = request.get_json()
#     print(data)
#     task_uuid = uuid.uuid1()
#     task = [data['description'],data['begintime'],data['endtime'],data['performer'],data['state'],data['title']]
#     if data['isFile']== 1:
#         last_data= ss.query(TiNodeModel).order_by(TiNodeModel.crtdate.desc()).first()
#         print(last_data.uuid)
#         nodeid = last_data.uuid
#         o =TiTaskModel(task_uuid, description=task[0], expbegindate=task[1], expenddate=task[2], executorname=task[3], objectstate=task[4], title=task[5], nodeid=nodeid)
#     if data['isFile']== 0:
#         o =TiTaskModel(task_uuid, description=task[0], expbegindate=task[1], expenddate=task[2], executorname=task[3], objectstate=task[4], title=task[5])
#     try:
#         ss.add(o)
#         ss.commit()
#     except Exception as e:
#         print("TiTaskService.addnew() encounter unexpected exception")
#         print(e)
#         raise e
#     else:
#         try:
#             ss.rollback()
#             ss.close()
#         except:
#             ss.rollback()
#             print('')
#     finally:
#         ss.close()
#     return task_uuid   
@app.route('/api/admin/task/tasks/new', methods=['POST'])
def create_task():
    print("开始创建任务")
    data = request.get_json()
    print(data)
    task_uuid = uuid.uuid1().hex

    cur = conn.cursor()
    cur.execute("select uuid,children from node")
    results = cur.fetchall()
    temp_uuid = []
    for val in data['nodeid']:
        for i in range(len(results)):
            if results[i][1] == [val]:
                temp_uuid.append(results[i][0])
    for val in temp_uuid:
        parent_array = []
        parent_array.append(task_uuid)
        cur.execute("update node set parent=%s where uuid = %s", (parent_array, val))
        conn.commit()
        print(parent_array)
        print(val)
        print("更新1条parent")
    # task = [data['description'],data['begintime'],data['endtime'],data['performer'],data['state'],data['title']]
    # if data['isFile']== 1:
    # last_data= ss.query(TiNodeModel).order_by(TiNodeModel.crtdate.desc()).first()
    # print(last_data.uuid)
    # nodeid = last_data.uuid

    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(round(time.time() * 1000)) / 1000))
    o = TiTaskModel(uuid=task_uuid, description=data['description'], expbegindate=data['begintime'],
                    expenddate=data['endtime'], executorname=data['performer'], objectstate=data['state'],
                    title=data['title'], nodeid=task_uuid, parentid=task_uuid)
    # if data['isFile']== 0:
    # o =TiTaskModel(task_uuid, description=task[0], expbegindate=task[1], expenddate=task[2], executorname=task[3], objectstate=task[4], title=task[5])
    try:
        print("任务提交到数据库执行")
        ss.add(o)
        ss.commit()
    except Exception as e:
        print("TiTaskService.addnew() encounter unexpected exception")
        print(e)
        raise e
    else:
        try:
            ss.rollback()
            ss.close()
        except:
            ss.rollback()
            print('')
    finally:
        ss.close()
    return "1"


@app.route('/api/admin/task/tasks/<string:title>', methods=['GET'])
def read_one_detail(title):
    cur = conn.cursor()
    cur.execute(
        "select * from taskthree where title=" + title)
    rows = cur.fetchall()
    l = []
    for row in rows:
        dic = {'id': str(row[0]), 'description': str(row[1]), 'begintime': str(row[2]), 'endtime': str(row[3]),
               'performer': str(row[4]), 'state': str(row[5]), 'title': str(row[6])}
        l.append(dic)
    return jsonify(dic)


@app.route('/api/admin/task/tasks/v/<string:id>', methods=['PUT'])
def update_one_task(id):
    # cur = conn.cursor()
    print("开始更新任务")
    data = request.get_json()
    form = request.form.to_dict()
    file_list = request.files.to_dict()
    print(file_list)
    print(form)
    print(data)
    # cur.execute("UPDATE taskthree SET performer = '{}', title = '{}', description = '{}', state = '{}', begintime = '{}', endtime = '{}'  WHERE id = {}"
    #     .format(data['performer'],data['title'],data['description'],data['state'],data['begintime'],data['endtime'], id))
    # conn.commit()
    # return "1"
    if data['nodeid'] == 'None':
        task = [data['description'], data['begintime'], data['endtime'], data['performer'], data['state'],
                data['title'], id]
        origin = ss.query(TiTaskModel).filter_by(id=task[-1]).first()
    else:
        task = [data['description'], data['begintime'], data['endtime'], data['performer'], data['state'],
                data['title'], data['nodeid'], id]
        origin = ss.query(TiTaskModel).filter_by(id=task[-1]).first()
        origin.nodeid = task[6]
    origin.description = task[0]
    origin.expbegindate = task[1]
    origin.expenddate = task[2]
    origin.executorname = task[3]
    origin.objectstate = task[4]
    origin.title = task[5]
    ss.add(origin)
    print('修改成功')
    ss.commit()
    ss.close()
    return "1"


@app.route('/api/admin/task/tasks/e/<string:id>', methods=['DELETE'])
def delete_one_task(id):
    print("开始删除任务和附件")
    nodeid = ss.query(TiTaskModel).filter(TiTaskModel.id == id).first().nodeid
    temp_nodeid = str(nodeid).split('-')
    nodeid = ''.join(temp_nodeid)
    cur = conn.cursor()
    cur.execute("select id,parent from node")
    results = cur.fetchall()
    temp_node_id = []

    for i in range(len(results)):
        if results[i][1]:
            if results[i][1][0] == nodeid:
                temp_node_id.append(results[i][0])
    print(temp_node_id)
    for val in temp_node_id:
        ss.query(TiNodeModel).filter(TiNodeModel.id == val).delete()
        ss.commit()
    ss.query(TiTaskModel).filter(TiTaskModel.id == id).delete()

    print('成功删除！')
    ss.commit()
    return "1"


# ---------------------------------------------------------------------------------------------------------------

@app.route('/api/anon/task/tasks', methods=['GET'])
def read_all_anon_tasks():
    # cur = conn.cursor()
    # cur.execute(
    #     "select * from taskthree")
    # rows = cur.fetchall()
    # l = []
    # for row in rows:
    #     print(row)
    #     dic = {'id': str(row[0]), 'description': str(row[1]), 'begintime': str(row[2]), 'endtime': str(row[3]),
    #            'performer': str(row[4]), 'state': str(row[5]), 'title': str(row[6])}
    #     l.append(dic)
    # return jsonify(l)

    selected_list = []
    result = ss.query(TiTaskModel).all()
    for i in result:
        expbegindate = i.expbegindate.strftime('%Y-%m-%d')
        expenddate = i.expenddate.strftime('%Y-%m-%d')
        t = {'id': i.id, 'uuid': i.uuid, 'description': i.description, 'begintime': expbegindate, 'endtime': expenddate,
             'performer': i.executorname, 'title': i.title, 'state': i.objectstate, 'nodeid': i.nodeid}
        # nodeid 是 parent ,传到前端
        selected_list.append(t)
    # return jsonify(selected_list)
    return Response(json.dumps(selected_list), mimetype='application/json')


@app.route('/api/anon/task/tasks/<string:id>', methods=['GET'])
def read_one_anon_task(id):
    # cur = conn.cursor()
    # cur.execute(
    #     "select * from taskthree where id=" + id)
    # rows = cur.fetchall()
    # l = []
    # for row in rows:
    #     # print(row)
    #     dic = {'id': str(row[0]), 'description': str(row[1]), 'begintime': str(row[2]), 'endtime': str(row[3]),
    #            'performer': str(row[4]), 'state': str(row[5]), 'title': str(row[6])}
    #     l.append(dic)
    # return jsonify(dic)
    cur = conn.cursor()
    cur.execute(
        "select * from tran0823 where id=" + id)
    rows = cur.fetchall()
    l = []
    for row in rows:
        # print(row)
        dic = {'id': str(row[0]), 'description': str(row[14]), 'begintime': str(row[23]), 'endtime': str(row[24]),
               'performer': str(row[7]), 'state': str(row[18]), 'title': str(row[13]), 'nodeid': str(row[15])}
        l.append(dic)
    return jsonify(dic)

# ---------------------------------------------------------------------------------------------------------------
#
#   用户的登录与登出
#
# ---------------------------------------------------------------------------------------------------------------


@app.route('/api/anon/login', methods=['POST'])
def login():
    # cur = conn.cursor()
    data = request.get_json()
    username = data['username']
    password = data['password']
    print(username, '用户名')
    print(password, '密码')
    result = ss.query(TiSecModel).filter(TiSecModel.username == username).first()
    if (TiSecModel.check_password(TiSecModel, result.password, password)):
        if (result == None):
            print("出错")
            return "出错"
        else:
            print("进入登录")
            if (not username or not password):
                return falseReturn('', '用户名和密码不能为空')
            else:
                return authenticate(username, password)


@app.route('/api/anon/user/info', methods=['GET'])
def get_info():
    # auth_header = request.headers.get('Authorization')
    # print(auth_header,"请求头")    
    result = identify(request)  # ok
    print(result)
    if (result['status'] and result['token']):
        id = result['token']
        user = ss.query(TiSecModel).filter(TiSecModel.id == id).first()
        print(user, "用户")
        returnUser = {
            'id': user.id,
            'username': user.username,
            # 'login_time': user.login_time
        }
        result = trueReturn(returnUser, "请求成功")
    return result


@app.route('/api/anon/logout', methods=['GET'])
def logout():
    return "1"


def authenticate(username, password):
    """
    用户登录，登录成功返回token，写将登录时间写入数据库；登录失败返回失败原因
    :param password:
    :return: json
    """
    try:
        userInfo = ss.query(TiSecModel).filter(TiSecModel.username == username).first()
        print(userInfo)
    except:
        return "登录失败"
    if (userInfo is None):
        return falseReturn('', '找不到用户')
    else:
        if (TiSecModel.check_password(TiSecModel, userInfo.password, password)):
            login_time = int(time.time())
            user = userInfo
            user.login_time = login_time
            # self.ss.add(user)
            ss.commit()
            token = encode_auth_token(userInfo.id, login_time)
            # token = self.encode_auth_token(userInfo.id)

            return trueReturn(token.decode(), '登录成功')
        else:
            return falseReturn('', '密码不正确')


def encode_auth_token(user_id, login_time):
    """
    生成认证Token
    :param user_id: int
    :param login_time: int(timestamp)
    :return: string
    """
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=10),
        'iat': datetime.datetime.utcnow(),
        'iss': 'ken',
        'data': {
            'id': user_id,
            'login_time': login_time
        }
    }
    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm='HS256'
    )


def decode_auth_token(auth_token):
    """
    验证Token
    :param auth_token:
    :return: integer|string
    """
    try:
        # payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), leeway=datetime.timedelta(seconds=10))
        # 取消过期时间验证
        payload = jwt.decode(auth_token, SECRET_KEY, options={'verify_exp': False})
        if ('data' in payload and 'id' in payload['data']):
            return payload
        else:
            raise jwt.InvalidTokenError
    except jwt.ExpiredSignatureError:
        return 'Token过期'
    except jwt.InvalidTokenError:
        return '无效Token'


def identify(request):
    """
    用户鉴权
    :return: list
    """
    auth_header = request.headers.get('Authorization')
    print("hhhhh")
    print(auth_header)
    if (auth_header):
        auth_tokenArr = auth_header.split(" ").pop()
        print(auth_tokenArr)
        if (not auth_tokenArr):
            # if (not auth_tokenArr or auth_tokenArr[0] != 'JWT' or len(auth_tokenArr) != 2):
            result = falseReturn('', '请传递正确的验证头信息')
        else:
            auth_token = auth_tokenArr
            print("--------------")  # ok
            print(auth_token)  # ok
            payload = decode_auth_token(auth_token)
            if not isinstance(payload, str):
                id = payload['data']['id']
                user = ss.query(TiSecModel).filter(TiSecModel.id == id).first()
                print(user, "当前用户")
                # user = Users.get(Users, payload['data']['id'])
                if (user is None):
                    print("用户不存在")
                    result = falseReturn('', '找不到该用户信息')
                else:
                    if (user.login_time == payload['data']['login_time']):
                        result = trueReturn(user.id, '请求成功')
                    else:
                        result = falseReturn('', 'Token已更改，请重新登录获取')
            else:
                result = falseReturn('', payload)
    else:
        result = falseReturn('', '没有提供认证token')
    return result


def trueReturn(data, msg):
    return {
        "status": True,
        "token": data,
        "msg": msg
    }


def falseReturn(data, msg):
    return {
        "status": False,
        "token": data,
        "msg": msg
    }


# ------------------------------------------------------------------------------------------------------
#
#  文件的上传下载
#
# ---------------------------------------------------------------------------------------------------------------


@app.route('/api/u/fdb/task', methods=['GET'])
def user_fdb_find():
    cur = conn.cursor()
    cur.execute("select uuid,originname,curname,upddate,crtdate from node")  # rows is list
    rows = cur.fetchall()
    l = []
    for row in rows:
        # d = dict(row.items())
        dic = {'uuid': str(row[0]), 'originname': str(row[1]), 'curname': str(row[2]), 'upddate': str(row[3]),
               'crtdate': str(row[4])}
        l.append(dic)
    conn.commit()
    return jsonify(l)


@app.route('/api/u/fdb/task/getFilename/<uuid>', methods=['GET'])
def getFilenameByTask(uuid):
    temp_nodeid = str(uuid).split('-')
    nodeid = ''.join(temp_nodeid)
    cur = conn.cursor()
    cur.execute("select uuid, originname,parent from node")
    results = cur.fetchall()
    file_list = []
    print(results)
    for i in range(len(results)):
        if results[i][2]:
            if results[i][2][0] == nodeid:
                file_list.append({'uuid': results[i][0], 'filename': results[i][1]})
    print(file_list)
    return jsonify(file_list)


@app.route('/api/u/fdb/task/updatefile/<nodeid>', methods=['POST'])
def updateTaskFile(nodeid):
    print('开始上传更新文件')
    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        originname = secure_filename(file.filename)
        curname = change_filename(originname)
        try:
            file.save(os.path.join(UPLOAD_FOLDER, curname))
            file = {'originname': originname, 'curname': curname}

            cur = conn.cursor()
            now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(round(time.time() * 1000)) / 1000))
            node_uuid = uuid.uuid1().hex
            temp_nodeid = nodeid.split('-')
            nodeid = ''.join(temp_nodeid)
            cur.execute(
                "insert into node(uuid, originname, curname, upddate, crtdate,children,parent) values(%s,%s,%s,%s,%s,%s,%s)",
                (node_uuid, file['originname'], file['curname'], now, now, [node_uuid], [nodeid]))
            conn.commit()

            resp = jsonify({'message': 'File successfully uploaded', 'status': 201, 'nodeid': nodeid})
            resp.status_code = 201
            return resp
        except Exception as e:
            print('upload failed --> {}'.format(str(e)))
            raise e
    else:
        resp = jsonify(
            'Allowed file types are txt, pdf, png, jpg, jpeg, gif, doc, docx, xls, xlsx, ppt, pptx, mp4, rar')
        resp.status_code = 400
        return resp


@app.route('/api/u/fdb/task/1/<uuid>', methods=['GET'])
def user_fdb_getfilename(uuid):
    cur = conn.cursor()
    tmp_uuid = "'" + uuid + "'"
    cur.execute("select * from node WHERE uuid = {}".format(tmp_uuid))
    rows = cur.fetchone()
    # print(rows,1111111111)
    if rows != None:
        try:
            # a = TiNodeModel(**rows)
            # dic= {'filename': a.originname}  
            filename = rows[6]
            # filename = a.originname
            print(filename)
            return filename
        except Exception as e:
            print('download failed --> {}'.format(str(e)))
            raise e
    else:
        return "没有附件"


@app.route('/api/u/fdb/task', methods=['POST'])
def user_fdb_uploadinto():
    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp
    print('开始上传文件')
    file = request.files['file']
    try:
        if session['nodeid']:
            print('seesion不为空：' + session['nodeid'])
    except:
        session['nodeid'] = uuid.uuid1().hex

    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        originname = secure_filename(file.filename)
        curname = change_filename(originname)
        try:
            file.save(os.path.join(UPLOAD_FOLDER, curname))
            file = {'originname': originname, 'curname': curname}
            nodeid = addnew(file)  # addnew nodeid
            resp = jsonify({'message': 'File successfully uploaded', 'status': 201, 'nodeid': session['nodeid']})
            resp.status_code = 201
            print('返回值' + session['nodeid'])
            return resp
        except Exception as e:
            print('upload failed --> {}'.format(str(e)))
            raise e
    else:
        resp = jsonify(
            'Allowed file types are txt, pdf, png, jpg, jpeg, gif, doc, docx, xls, xlsx, ppt, pptx, mp4, rar')
        resp.status_code = 400
        return resp


# @app.route('/api/u/fdb/m/task', methods=['POST'])
# def user_multi_fdb_upload():
#     if 'file' not in request.files:
#         resp = jsonify({'message': 'No file part in the request'})
#         resp.status_code = 400
#         return resp
#     files = request.files.getlist('file')
#     print(files, 111)
#     print('file', 222)
#     errors = {}
#     success = False
#     # parentid = uuid.uuid1()
#     # print(parentid,type(parentid))
#     parent = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
#     # parent = str(uuid.uuid1() ).replace("-", "")
#     # l=[]
#     # l.append(parent)
#     # parent ="parentid"
#     # if parent !=
#     print(parent, "parent", type(parent), 663)
#     # print(l)
#     for file in files:
#         if file and allowed_file(file.filename):
#             originname = secure_filename(file.filename)
#             curname = change_filename(originname)
#             file.save(os.path.join(UPLOAD_FOLDER, originname))
#
#             file = {'originname': originname, 'curname': curname, 'parent': parent}
#             print(file)
#             # children =[]
#             file_nodeid = addmulti(file)  # 新增两条node表数据
#             # children.append(file_nodeid)
#             # print(children)
#             print(file_nodeid)
#             success = True
#         else:
#             errors[file.filename] = 'File type is not allowed'
#     if success and errors:
#         errors['message'] = 'File(s) successfully uploaded'
#         resp = jsonify(errors)
#         resp.status_code = 500
#         return resp
#     if success:
#         resp = jsonify({'message': 'Files successfully uploaded', 'status': 201, 'nodeid': file_nodeid})
#         resp.status_code = 201
#         return resp
#     else:
#         resp = jsonify(errors)
#         resp.status_code = 500
#         return resp


def addnew(file):
    print(session['nodeid'])
    cur = conn.cursor()
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(round(time.time() * 1000)) / 1000))
    node_uuid = uuid.uuid1().hex
    try:
        nodeid = session['nodeid']
    except:
        nodeid = uuid.uuid1().hex
    parent_array = []
    parent_array.append(nodeid)
    print(type(parent_array[0]))
    cur.execute("insert into node(uuid, originname, curname, upddate, crtdate,children) values(%s,%s,%s,%s,%s,%s)",
                (node_uuid, file['originname'], file['curname'], now, now, parent_array))
    conn.commit()
    return nodeid


# def addmulti(file):
#     cur = conn.cursor()
#     now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(round(time.time() * 1000)) / 1000))
#     nodeid = uuid.uuid1()
#     print(type(nodeid))
#     children = str(nodeid)
#     cur.execute(
#         "insert into node(uuid, originname, curname, parent, upddate, crtdate, children) values(%s,%s,%s,%s,%s,%s,%s)",
#         (nodeid, file['originname'], file['curname'], file['parent'], now, now, children))
#     conn.commit()
#     return nodeid


@app.route('/api/u/fdb/task/<uuid>', methods=['GET'])
def user_fdb_download(uuid):
    try:
        filename = get(uuid)
        response = make_response(send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True, ))
        originName = user_fdb_getfilename(uuid)
        response.headers["Content-Disposition"] = "attachment; filename={}".format(
            originName.encode().decode('latin-1'))
        return response
    except Exception as e:
        raise e
    return jsonify({"code": "异常", "message": "{}".format(e)})


def get(uuid):
    cur = conn.cursor()
    tmp_uuid = "'" + uuid + "'"
    cur.execute("select * from node WHERE uuid = {}".format(tmp_uuid))
    rows = cur.fetchone()
    if rows != None:
        try:
            # a = TiNodeModel(**rows)
            # dic= {'filename': a.originname}  
            # filename = a.originname
            filename = rows[7]
            print(filename)
            return filename
        except Exception as e:
            print('download failed --> {}'.format(str(e)))
            raise e
    else:
        return "没有附件"


@app.route('/api/u/fdb/task/<uuid>', methods=['DELETE'])
def user_fdb_delete(uuid):
    print("运行到这里了")
    cur = conn.cursor()
    tmp_uuid = "'" + uuid + "'"
    cur.execute("select * from node WHERE uuid = {}".format(tmp_uuid))
    rows = cur.fetchone()
    if rows != None:
        try:
            filename = rows[7]
            path = os.path.join(UPLOAD_FOLDER, filename)
            print(path)
            os.remove(path)
        except Exception as e:
            print('download failed --> {}'.format(str(e)))
            raise e
    cur.execute("DELETE from node where uuid={}".format(tmp_uuid))
    conn.commit()
    return "1"


@app.route('/api/u/fdb/task/content/<uuid>', methods=['GET'])
def user_fdb_getfile(uuid):
    print("获得文件")
    filename = get(uuid)
    print(filename)
    return send_from_directory(UPLOAD_FOLDER, filename)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def change_filename(filename):
    fileinfo = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + fileinfo[-1]
    return filename


# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------


##BHR4.30新加代码


@app.route('/api/u/activity', methods=['GET'])
def read_avtivities():
    conn = psycopg2.connect(
        database="postgres", user="postgres", password="tongji2020", host="47.111.234.116", port="5432")
    cur = conn.cursor()
    cur.execute(
        "select APPL1011.uuid,APPL1011.category,APPL1011.memberid,APPL1011.begintime,APPL1011.endtime,APPL1011.workday,APPL1011.workpoint,MAST0501.employeeid,MAST0501.firstname,MAST0501.title,APPL1011.courseid,MAST1014.code,MAST1014.name,MAST1014.credit,APPL1011.objectstate from APPL1011  join MAST0501 ON(APPL1011.memberid=MAST0501.uuid) join MAST1014 ON(APPL1011.courseid=MAST1014.uuid)")
    rows = cur.fetchall()
    l = []
    for row in rows:
        print(row)
        dic = {'uuid': str(row[2]), 'employeeid': str(row[7]), 'name': str(row[8]), 'title': str(row[9]),
               'courseuuid': str(row[10]), 'courseid': str(row[11]), 'coursename': str(row[12]), 'credit': str(row[13]),
               'objectstate': str(row[14]), 'begintime': str(row[3]), 'endtime': str(row[4]), 'workday': str(row[5]),
               'workpoint': str(row[6])}
        if (str(row[14]) == "1"):
            dic['objectstate'] = "申请中"
        else:
            dic['objectstate'] = "已分配"
        l.append(dic)
        print(dic.values())
    print(l)
    conn.commit()
    print("Update Successfully")
    conn.close()
    return jsonify(l)


@app.route("/api/u/export/report2", methods=['GET'])
def export_records2():
    conn = psycopg2.connect(
        database="postgres", user="postgres", password="tongji2020", host="47.111.234.116", port="5432")
    cur = conn.cursor()
    sq1 = "select uuid,id,employeeid,firstname from mast0501"
    sq2 = "select courseid from appl1011 where memberid={} and objectstate='3'"
    cur.execute(sq1)
    members = cur.fetchall()
    l = []
    max = 0
    max_index = 0
    for j, member in enumerate(members):
        # tmp={'name':str(member[3]),'employeeid':str(member[2])}

        tmp = {'employeeid': str(member[2]), 'name': str(member[3])}
        member_uuid = "'" + member[0] + "'"
        # print(member[3])
        cur.execute(sq2.format(member_uuid))
        rows = cur.fetchall()
        print(len(rows))
        if (len(rows) > max):
            max = len(rows)
            max_index = j
        for i, row in enumerate(rows):
            # print(i)
            # dic= {'courseid': str(rows[i][0])}
            a = "'" + str(rows[i][0]) + "'"
            cur.execute("select name from mast1014 where uuid={}".format(a))
            courses = cur.fetchall()
            if (len(courses) > 0):
                tmp.update({'课程{}'.format(i + 1): str(courses[0][0])})
            # print(courses[0][6])
        l.append(tmp)
    tmp = l[max_index]
    l[max_index] = l[0]
    l[0] = tmp
    print("tpye of l:", type(l))
    print(l)
    filename = 'REPT1012.xlsx'
    df = pd.DataFrame(l)
    print(df)
    # # 保存到本地excel
    df.to_excel(filename)
    # # 需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
    directory = os.getcwd()  # 假设在当前目录
    return send_from_directory(directory, filename, as_attachment=True)
    conn.commit()
    print("Update Successfully")
    conn.close()
    # return excel.make_response_from_records(l, "xlsx",
    #                                         file_name=u"REPT1012 教师排课一览表")


@app.route("/api/u/export/report3", methods=['GET'])
def export_records3():
    conn = psycopg2.connect(
        database="postgres", user="postgres", password="tongji2020", host="47.111.234.116", port="5432")
    cur = conn.cursor()
    sq1 = "select uuid,code,name from mast1014"
    sq2 = "select memberid from appl1011 where courseid={} and objectstate='3'"
    cur.execute(sq1)
    courses = cur.fetchall()
    l = []
    max = 0
    max_index = 0
    for j, course in enumerate(courses):
        # tmp={'name':str(member[3]),'employeeid':str(member[2])}

        tmp = {'code': str(course[1]), 'coursename': str(course[2])}
        course_uuid = "'" + course[0] + "'"
        # print(member[3])
        cur.execute(sq2.format(course_uuid))
        rows = cur.fetchall()
        print(len(rows))
        if (len(rows) > max):
            max = len(rows)
            max_index = j
        for i, row in enumerate(rows):
            # print(i)
            # dic= {'memberid': str(rows[i][0])}
            a = "'" + str(rows[i][0]) + "'"
            cur.execute("select firstname from mast0501 where uuid={}".format(a))
            print("memberid:", a)
            members = cur.fetchall()
            if (len(members) > 0):
                tmp.update({'membername{}'.format(i + 1): str(members[0][0])})
            # print(members[0][0])
        l.append(tmp)
        print(tmp)
    tmp = l[max_index]
    l[max_index] = l[0]
    l[0] = tmp
    filename = 'REPT1013.xlsx'
    df = pd.DataFrame(l)
    print(df)
    # # 保存到本地excel
    df.to_excel(filename)
    # # 需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
    directory = os.getcwd()  # 假设在当前目录
    return send_from_directory(directory, filename, as_attachment=True)
    conn.commit()
    print("Update Successfully")
    conn.close()


@app.route('/api/u/activity/coursename/<string:name>', methods=['GET'])
def read_activity_by_coursename(name):
    conn = psycopg2.connect(
        database="postgres", user="postgres", password="tongji2020", host="47.111.234.116", port="5432")
    cur = conn.cursor()
    tmp_name = "'" + name + "'"
    cur.execute(
        "select uuid from mast1014 where name={}".format(tmp_name)
    )
    courses = cur.fetchall()
    id = courses[0][0]
    # courseid='55bb4506-8610-11ea-b832-e43c8a9c5604'
    courseid = "'" + id + "'"
    cur.execute(
        "select APPL1011.uuid,APPL1011.category,APPL1011.memberid,APPL1011.begintime,APPL1011.endtime,APPL1011.workday,APPL1011.workpoint,MAST0501.employeeid,MAST0501.firstname,MAST0501.title,APPL1011.courseid,MAST1014.id,MAST1014.name,MAST1014.credit,APPL1011.objectstate from APPL1011  join MAST0501 ON(APPL1011.memberid=MAST0501.uuid) join MAST1014 ON(APPL1011.courseid=MAST1014.uuid) where courseid={}".format(
            courseid))
    rows = cur.fetchall()
    l = []
    for row in rows:
        print(row)
        dic = {'uuid': str(row[2]), 'employeeid': str(row[7]), 'name': str(row[8]), 'title': str(row[9]),
               'courseuuid': str(row[10]), 'courseid': str(row[11]), 'coursename': str(row[12]), 'credit': str(row[13]),
               'objectstate': str(row[14]), 'begintime': str(row[3]), 'endtime': str(row[4]), 'workday': str(row[5]),
               'workpoint': str(row[6])}
        l.append(dic)
    print(l)
    conn.commit()
    print("Update Successfully")
    conn.close()
    return jsonify(l)


@app.route('/api/u/activity/membername/<string:name>', methods=['GET'])
def read_activity_by_membername(name):
    conn = psycopg2.connect(
        database="postgres", user="postgres", password="tongji2020", host="47.111.234.116", port="5432")
    cur = conn.cursor()
    tmp_name = "'" + name + "'"
    cur.execute(
        "select uuid from mast0501 where firstname={}".format(tmp_name)
    )
    courses = cur.fetchall()
    id = courses[0][0]
    # courseid='55bb4506-8610-11ea-b832-e43c8a9c5604'
    memberid = "'" + id + "'"
    cur.execute(
        "select APPL1011.uuid,APPL1011.category,APPL1011.memberid,APPL1011.begintime,APPL1011.endtime,APPL1011.workday,APPL1011.workpoint,MAST0501.employeeid,MAST0501.firstname,MAST0501.title,APPL1011.courseid,MAST1014.id,MAST1014.name,MAST1014.credit,APPL1011.objectstate from APPL1011  join MAST0501 ON(APPL1011.memberid=MAST0501.uuid) join MAST1014 ON(APPL1011.courseid=MAST1014.uuid) where memberid={}".format(
            memberid))
    rows = cur.fetchall()
    l = []
    for row in rows:
        print(row)
        dic = {'uuid': str(row[2]), 'employeeid': str(row[7]), 'name': str(row[8]), 'title': str(row[9]),
               'courseuuid': str(row[10]), 'courseid': str(row[11]), 'coursename': str(row[12]), 'credit': str(row[13]),
               'objectstate': str(row[14]), 'begintime': str(row[3]), 'endtime': str(row[4]), 'workday': str(row[5]),
               'workpoint': str(row[6])}
        l.append(dic)
    print(l)
    conn.commit()
    print("Update Successfully")
    conn.close()
    return jsonify(l)


@app.route('/api/u/activity/test', methods=['GET'])
def read_activity_test():
    # filepath='F:\download\教师任课申请'
    filename = 'REPT1012 教师排课一览表.xlsx'
    # 需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
    directory = os.getcwd()  # 假设在当前目录
    return send_from_directory(directory, filename, as_attachment=True)
    # return filepath+filename


@app.route('/api/u/node', methods=['GET'])
def read_node():
    conn = psycopg2.connect(
        database="dm365", user="postgres", password="tongji2020", host="47.111.234.116", port="5432")
    cur = conn.cursor()
    cur.execute("select uuid,originname,curname,upddate,crtdate from node")
    rows = cur.fetchall()
    l = []
    for row in rows:
        print(row)
        dic = {'uuid': str(row[0]), 'originname': str(row[1]), 'curname': str(row[2]), 'upddate': str(row[3]),
               'crtdate': str(row[4])}
        l.append(dic)
        print(dic.values())
    print(l)
    conn.commit()
    print("Update Successfully")
    conn.close()
    return jsonify(l)


@app.route('/api/u/ecg', methods=['GET'])
def read_ecg():
    f = open('G:\\迅雷下载\\samples.csv')
    # res = pd.read_csv(f)
    data = pd.read_csv(f, header=1)
    data2 = data.values[0:100]
    dic = {}
    for i in range(len(data2)):
        data2[i][0] = data2[i][0][2:14]
    dic['date'] = data2[..., 0].tolist()
    dic['uv'] = data2[..., 1].tolist()
    return jsonify(dic)


if __name__ == '__main__':
    # excel.init_excel(app)  ## 下载excel必须 请勿注释
    # from werkzeug.contrib.fixers import ProxyFix
    # app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run()
