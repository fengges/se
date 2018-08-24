import pickle,os
from  base import dbs
from  config import root
def getTeacherName():
    sql = "SELECT * from teacher "
    result=dbs.getDics(sql)
    dic={}
    for r in result:
        dic[r['id']]=r
    pickle.dump(dic, open(root+'/teacherName', 'wb'))
def getPaperAndTecher():
    sql="SELECT a.id,a.author_id,b.`name` FROM `paper2` a JOIN teacher b on a.author_id=b.id"
    paper={}
    teacher={}
    result=dbs.getDics(sql)
    for r in result:
        paper[r["id"]]={"author_id":r["author_id"],"name":r["name"]}
        if r["author_id"] in teacher:
            teacher[r["author_id"]].append(r["id"])
        else:
            teacher[r["author_id"]]=[r["id"]]
    pickle.dump(paper,open(root+'/paperTeacher', 'wb'))
    pickle.dump(teacher,open(root+'/teacherPaper', 'wb'))
def getTeacherAndSchool():
    sql = "SELECT a.id,a.school_id from teacher a"
    result = dbs.getDics(sql)
    teacher={}
    school={}
    for r in result:
        if r["school_id"] in school:
            school[r["school_id"]].append(r["id"])
        else:
            school[r["school_id"]]=[r["id"]]
        teacher[r["id"]]=r["school_id"]
    pickle.dump(teacher, open(root+'/teacherSchool', 'wb'))
    pickle.dump(school, open(root+'/schoolTeacher', 'wb'))
def getWordPaper(code,k):
    sql="SELECT name FROM `discipline_new` where code=%s"
    result = dbs.getDics(sql,(code,))
    name=result[0]['name']
    p=root+'/'+name+'-'+code+'/k'+str(k)
    file = open(p+'/'+code+"_topic.txt", 'r', encoding="utf8")
    list = file.readlines()
    wordToTopic={}
    topicToWord = {}
    for topic_id,line in enumerate(list):
        index=line.find(":")
        words=eval(line[index+1:])
        topicToWord[topic_id]=words
        for w in words:
            if w in wordToTopic:
                wordToTopic[w][topic_id]=words[w]
            else:
                wordToTopic[w]={}
                wordToTopic[w][topic_id] = words[w]
    path=root+'/'+code+'/k'+str(k)
    if not os.path.exists(path):
        os.makedirs(path)
    pickle.dump(topicToWord, open(path+'/topicToWord', 'wb'))
    pickle.dump(wordToTopic, open(path+'/wordToTopic', 'wb'))

def getPaperTopic(code,k):
    sql="SELECT name FROM `discipline_new` where code=%s"
    result = dbs.getDics(sql,(code,))
    name=result[0]['name']
    p = root+'/' + name + '-' + code + '/k' + str(k)
    file = open(p+'/'+code+"_teacher_topic.txt", 'r', encoding="utf8")
    paperId = open(root+'/' + name + '-' + code + "/"+code+"_fenci_tdidf.txt", 'r', encoding="utf8")
    ids=[]
    for line in paperId.readlines():
        item=eval(line)
        ids.append(item['id'])
    paperToic={}

    for paper_index, line in enumerate(file.readlines()):
        temp = eval(line)
        paperToic[ids[paper_index]] = {}
        for t in temp:
            paperToic[ids[paper_index]][t[0]] = t[1]
    path = root+'/'+ code + '/k' + str(k)
    pickle.dump(paperToic, open(path+'/paperToic', 'wb'))
def teacherTopic(code,k):
    path = root+'/' + code + '/k' + str(k)
    paperToic=pickle.load( open(path + '/paperToic', 'rb'))
    paper=pickle.load(open(root+'/paperTeacher', 'rb'))
    teacherTopic={}
    for p in paperToic:
        author_id=paper[p]["author_id"]
        if author_id not in teacherTopic:
            teacherTopic[author_id]={}
        p_topic=paperToic[p]
        for topic in p_topic:
            if topic in teacherTopic[author_id]:
                teacherTopic[author_id][topic]+=p_topic[topic]
            else:
                teacherTopic[author_id][topic]= p_topic[topic]
    path = root+'/' + code + '/k' + str(k)
    pickle.dump(teacherTopic, open(path+'/teacherTopic', 'wb'))
def getTopicTeacher(code,k):
    path = root+'/'+ code + '/k' + str(k)
    teacherTopic=pickle.load(open(path+'/teacherTopic', 'rb'))
    topicTeacher={}
    for teacher_id in teacherTopic:
        teacher=teacherTopic[teacher_id]
        for topic_id in teacher:
            if topic_id not in topicTeacher:
                topicTeacher[topic_id]={}
            topicTeacher[topic_id][teacher_id]=teacher[topic_id]
    pickle.dump(topicTeacher, open(path +'/topicTeacher', 'wb'))
def getTeacherTeacher(code,k):
    path = root+'/' + code + '/k' + str(k)
    topicTeacher=pickle.load(open(path + '/topicTeacher', 'rb'))
    TeacherTeacher={}
    for topic_id in topicTeacher:
        teacher=topicTeacher[topic_id]
        for t in teacher:
            if t not in TeacherTeacher:
                TeacherTeacher[t]={}
            for o in teacher:
                if o!=t:
                    if o not in TeacherTeacher[t]:
                        TeacherTeacher[t][o]=0
                    TeacherTeacher[t][o]+=teacher[t]*teacher[o]
    pickle.dump(TeacherTeacher, open(path+'/TeacherTeacher', 'wb'))

def getSchoolTopic(code,k):
    path = root+'/' + code + '/k' + str(k)
    teacherTopic=pickle.load(open(path+'/teacherTopic', 'rb'))
    teacher=pickle.load(open(root+'/teacherSchool', 'rb'))
    schoolTopic={}
    for t in teacherTopic:
        s=teacher[t]
        if s==0:
            continue
        topic=teacherTopic[t]
        if s not in schoolTopic:
            schoolTopic[s]={}
        for to in topic:
            if to in schoolTopic[s]:
                schoolTopic[s][to]+=topic[to]
            else:
                schoolTopic[s][to]= topic[to]
    pickle.dump(schoolTopic, open(path+'/schoolTopic', 'wb'))
def getTopicSchool(code, k):
    path = root+'/' + code + '/k' + str(k)
    schoolTopic = pickle.load(open(path + '/schoolTopic', 'rb'))
    topicSchool = {}
    for school_id in schoolTopic:
        school = schoolTopic[school_id]
        for topic_id in school:
            if topic_id not in topicSchool:
                topicSchool[topic_id] = {}
            topicSchool[topic_id][school_id] = school[topic_id]
    pickle.dump(topicSchool, open(path + '/topicSchool', 'wb'))
def getSchoolSchool(code, k):
    path = root+'/' + code + '/k' + str(k)
    topicSchool = pickle.load(open(path + '/topicSchool', 'rb'))
    SchoolSchool = {}
    for topic_id in topicSchool:
        school = topicSchool[topic_id]
        for t in school:
            if t not in SchoolSchool:
                SchoolSchool[t] = {}
            for o in school:
                if o != t:
                    if o not in SchoolSchool[t]:
                        SchoolSchool[t][o] = 0
                        SchoolSchool[t][o] += school[t] * school[o]
    pickle.dump(SchoolSchool, open(path + '/SchoolSchool', 'wb'))

if __name__ == '__main__':
    # getTeacherName()
    # getPaperAndTecher()
    # getTeacherAndSchool()
    subject = [{"code": '01', "k": 46},{"code": '02', "k": 98},{"code": '03', "k": 98},
               {"code": '04', "k": 88},{"code": '05', "k": 98},{"code": '06', "k": 28},
               {"code": '07', "k": 54}, {"code": '0701', "k": 64}, {"code": '0702', "k": 30},
               {"code": '0703', "k": 52}, {"code": '0705', "k": 16}, {"code": '0706', "k": 12},
               {"code": '0707', "k": 14}, {"code": '0709', "k": 98}, {"code": '0710', "k": 98},
               {"code": '0712', "k": 10}, {"code": '08', "k":50}, {"code": '0801', "k": 26},
               {"code": '0802', "k": 98}, {"code": '0803', "k": 14}, {"code": '0804', "k":12},
               {"code": '0805', "k": 98}, {"code": '0806', "k":12}, {"code": '0807', "k": 38},
               {"code": '0808', "k": 98}, {"code": '0809', "k": 52}, {"code": '0810', "k": 98},
               {"code": '0811', "k": 22}, {"code": '0812', "k": 72}, {"code": '0813', "k": 30},
               {"code": '0814', "k": 68}, {"code": '0815', "k":14}, {"code": '0816', "k": 14},
               {"code": '0817', "k":98}, {"code": '0818', "k": 14}, {"code": '0819', "k": 18},
               {"code": '0820', "k": 18}, {"code": '0821', "k": 18}, {"code": '0823', "k": 24},
               {"code": '0824', "k": 14}, {"code": '0825', "k": 26}, {"code": '0826', "k": 10},
               {"code": '0827', "k": 12}, {"code": '0828', "k": 36}, {"code": '0829', "k": 14},
               {"code": '0830', "k": 82}, {"code": '0831', "k": 16}, {"code": '0832', "k": 28},
               {"code": '09', "k": 74}, {"code": '10', "k": 98},{"code": '11', "k": 14},
               {"code": '12', "k": 98}]
    for sub in subject:
        print(sub)
        getWordPaper(sub['code'],sub['k'])
        getPaperTopic(sub['code'],sub['k'])
        teacherTopic(sub['code'],sub['k'])
        getTopicTeacher(sub['code'],sub['k'])
        getTeacherTeacher(sub['code'],sub['k'])
        getSchoolTopic(sub['code'],sub['k'])
        getTopicSchool(sub['code'],sub['k'])
        getSchoolSchool(sub['code'],sub['k'])
        pass
