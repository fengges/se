from  base import dbs
from  config import root
import pickle
def getTeacherWord(code,k):
    sql="SELECT name FROM `discipline_new` where code=%s"
    result = dbs.getDics(sql,(code,))
    name=result[0]['name']
    path=root+'/' + name + '-' + code
    file= open(path+ "/"+code+"_fenci_tdidf.txt", 'r', encoding="utf8")
    paper = pickle.load(open(root+'/paperTeacher', 'rb'))
    list=file.readlines()
    teacherWord={}
    for line in list:
        temp=eval(line)
        paper_id=temp['id']
        teacher_id=paper[paper_id]["author_id"]
        if teacher_id not in teacherWord:
            teacherWord[teacher_id]={}
        words=temp['fenci'].split(' ')
        for w in words:
            if w in teacherWord[teacher_id]:
                teacherWord[teacher_id][w]+=1
            else:
                teacherWord[teacher_id][w]= 1

    pickle.dump(teacherWord, open(root+'/'+ code+'/k'+str(k)+'/teacherWord', 'wb'))

def computer(code,k):
    teacherWord=pickle.load(open(root+'/'+ code+'/k'+str(k)+'/teacherWord', 'rb'))
    word={}
    wordIndex={}
    length=0
    for teacher_id in teacherWord:
        teacher = teacherWord[teacher_id]
        size=len(teacher)
        for w in teacher:
            if w not in wordIndex:
                wordIndex[w]={}
                word[w]=0
            word[w]+=teacher[w]
            length+=teacher[w]
            wordIndex[w][teacher_id]=teacher[w]/size
    for w in word:
        wordIndex[w]["col_fre"]=word[w]/length
    pickle.dump(wordIndex, open(root+'/'+ code+'/k'+str(k)+'/wordIndex', 'wb'))
def getSchoolWord(code, k):
    sql = "SELECT name FROM `discipline_new` where code=%s"
    teacherSchool=pickle.load(open(root+'/teacherSchool', 'rb'))
    result = dbs.getDics(sql, (code,))
    name = result[0]['name']
    path = root+'/' + name + '-' + code
    file = open(path + "/" + code + "_fenci_tdidf.txt", 'r', encoding="utf8")
    paper = pickle.load(open(root+'/paperTeacher', 'rb'))
    list = file.readlines()
    schoolWord = {}
    for line in list:
        temp = eval(line)
        paper_id = temp['id']
        teacher_id = paper[paper_id]["author_id"]
        school_id=teacherSchool[teacher_id]
        if school_id not in schoolWord :
            schoolWord[school_id] = {}
        words = temp['fenci'].split(' ')
        for w in words:
            if w in schoolWord [school_id]:
                schoolWord[school_id][w] += 1
            else:
                schoolWord[school_id][w] = 1

    pickle.dump(schoolWord, open(root+'/' + code + '/k' + str(k) + '/schoolWord', 'wb'))
def computerSchool(code,k):
    schoolWord=pickle.load(open(root+'/'+ code+'/k'+str(k)+'/schoolWord', 'rb'))
    word={}
    wordIndex={}
    length=0
    for school_id in schoolWord:
        school = schoolWord[school_id]
        size=len(school)
        for w in school:
            if w not in wordIndex:
                wordIndex[w]={}
                word[w]=0
            word[w]+=school[w]
            length+=school[w]
            wordIndex[w][school_id]=school[w]/size
    for w in word:
        wordIndex[w]["col_fre"]=word[w]/length
    pickle.dump(wordIndex, open(root+'/'+ code+'/k'+str(k)+'/s_wordIndex', 'wb'))
if __name__ == '__main__':
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
        getTeacherWord(sub['code'],sub['k'])
        computer(sub['code'],sub['k'])
        getSchoolWord(sub['code'],sub['k'])
        computerSchool(sub['code'], sub['k'])
        pass