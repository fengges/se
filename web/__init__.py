
#  author   ：feng
#  time     ：2018/1/25
#  function : 应用初始化

#       注册蓝图

import  os
from main import Query
from flask import Flask,json,request

app = Flask(__name__)

subject = [{"code": '01', "k": 80}, {"code": '0705', "k": 80}, {"code": '0709', "k": 80}, {"code": '04', "k": 80},
           {"code": '03', "k": 80}, {"code": '02', "k": 80}]
a = Query(subject)

@app.route('/search',methods=['GET','POST'])
def index6():
    t = request.data
    if len(t)==0:
        t=request.values['data']
    data = json.loads(t)
    text=data['keyword']
    if "filer" not in  data:
        filer={}
    else:
        filer = data['filer']
        if "school" in filer and "all" in filer["school"]:
            del filer["school"]
        if "code" in filer and "all" in filer["code"]:
            del filer["code"]
    r=a.do_query(text,filer)
    s=json.jsonify(r)
    return s















