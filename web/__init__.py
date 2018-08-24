
#  author   ：feng
#  time     ：2018/1/25
#  function : 应用初始化

#       注册蓝图

import  os
from main import Query
from flask import Flask,json,request

app = Flask(__name__)

subject = [{"code": '01', "k": 46}, {"code": '02', "k": 98}, {"code": '03', "k": 98},
           {"code": '04', "k": 88}, {"code": '05', "k": 98}, {"code": '06', "k": 28},
           {"code": '07', "k": 54}, {"code": '0701', "k": 64}, {"code": '0702', "k": 30},
           {"code": '0703', "k": 52}, {"code": '0705', "k": 16}, {"code": '0706', "k": 12},
           {"code": '0707', "k": 14}, {"code": '0709', "k": 98}, {"code": '0710', "k": 98},
           {"code": '0712', "k": 10}, {"code": '08', "k": 50}, {"code": '0801', "k": 26},
           {"code": '0802', "k": 98}, {"code": '0803', "k": 14}, {"code": '0804', "k": 12},
           {"code": '0805', "k": 98}, {"code": '0806', "k": 12}, {"code": '0807', "k": 38},
           {"code": '0808', "k": 98}, {"code": '0809', "k": 52}, {"code": '0810', "k": 98},
           {"code": '0811', "k": 22}, {"code": '0812', "k": 72}, {"code": '0813', "k": 30},
           {"code": '0814', "k": 68}, {"code": '0815', "k": 14}, {"code": '0816', "k": 14},
           {"code": '0817', "k": 98}, {"code": '0818', "k": 14}, {"code": '0819', "k": 18},
           {"code": '0820', "k": 18}, {"code": '0821', "k": 18}, {"code": '0823', "k": 24},
           {"code": '0824', "k": 14}, {"code": '0825', "k": 26}, {"code": '0826', "k": 10},
           {"code": '0827', "k": 12}, {"code": '0828', "k": 36}, {"code": '0829', "k": 14},
           {"code": '0830', "k": 82}, {"code": '0831', "k": 16}, {"code": '0832', "k": 28},
           {"code": '09', "k": 74}, {"code": '10', "k": 98}, {"code": '11', "k": 14},
           {"code": '12', "k": 98}]
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















