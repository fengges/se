# coding=utf-8
from __future__ import division
from config import root
import pickle
import time,jieba
import jieba.posseg as pseg

class Subject:

    def __init__(self,sub):
        self.sub=sub
        code=self.sub['code']
        k=self.sub['k']
        print("load:"+code)
        self.path= root+'/' + code + '/k' + str(k)
        self.lmindex =  pickle.load(open(self.path+'/wordIndex', 'rb'))
        self.ldaword = pickle.load(open(self.path+'/wordToTopic', 'rb'))
        self.ldaexp = pickle.load(open(self.path+'/teacherTopic', 'rb'))
        self.pagerank = pickle.load(open(self.path+'/teacherRank', 'rb'))
        self.lmne = len(self.lmindex)

    def cal_lda_one_word(self,word,teacher_id):
        """计算单个词的专家lda得分"""
        ld = self.ldaword.get(word)

        sort = {}
        res = {}
        if ld != None:
            if teacher_id is not None:
                ld = {k: ld[k] for k in ld if k in teacher_id}
            sortld = sorted(ld.items(),key=lambda item:item[1],reverse=True)
            a = [r for r in sortld if r[1]>1.0e-06]
            for i in a :
                sort[i[0]] = i[1]

        for j in sort.keys():
            for m in self.ldaexp.keys():
                if j in self.ldaexp[m]:
                    res[m] = self.ldaexp[m][j]*sort[j]
        return res

    def cal_one_word(self,word,teacher_id):
        """计算单个词的专家语言模型得分"""
        lm = self.lmindex.get(word)

        res = {}
        miu = 10
        cal = self.lmne / (self.lmne + miu)     # 引入平滑系数
        if lm != None:
            if teacher_id is not None:
                lm = {k: lm[k] for k in lm if k in teacher_id or k=="col_fre"}
            for l in lm.keys():
                if l != 'col_fre':
                    res[l] = cal*lm[l]+(1-cal)*lm['col_fre']
            res['col'] = lm['col_fre']
        return res

    def cal_rank(self,res,lda):
        """计算专家排序"""
        rank = {}

        exp_list = [r for wd in res.keys() for r in res[wd]]
        exp_list = set(exp_list)
        exp_list.remove('col')

        for r in exp_list:
            rank[r] = 1
            for wd in res.keys():
                if len(res[wd]) != 0:
                 if res[wd].get(r):
                    rank[r] *= res[wd][r]
                 else:
                    rank[r] *= res[wd]['col']

            for wd in lda.keys():
                if lda[wd].get(r):
                    adjust = lda[wd][r]\
                             #*10e6
                    rank[r] *= adjust
                else:
                    rank[r] *= 10e-6
            if self.pagerank.get(r):
                rank[r] *= self.pagerank[r]
        return rank

    def do_query(self,words,teacher_id):
        temp_res = {}
        temp_lda = {}
        for word in words :
            temp_res[word] = self.cal_one_word(word,teacher_id)
            temp_lda[word] = self.cal_lda_one_word(word,teacher_id)
        for word in words:
            if not temp_res[word]:
                temp_res.pop(word)
            if not temp_lda[word]:
                temp_lda.pop(word)
        if not temp_res and not temp_lda:
            return []
        rank = self.cal_rank(temp_res,temp_lda)
        sortrk = sorted(rank.items(), key=lambda item: item[1], reverse=True)
        result = [(r[0],r[1]) for r in sortrk[:20]]
        return result
class Query:
    def __init__(self,subs):
        self.subs=subs
        self.Subject={sub['code']:Subject(sub) for sub in self.subs}
        self.stop=[]
        stopword = [line.strip() for line in open('fenci/stopwords.txt', encoding='utf-8').readlines()]
        stopword1 = [line.strip() for line in open('fenci/stop_word_4.txt', encoding='utf-8').readlines()]
        stopwords = [i.split(':')[0] for i in stopword1]
        self.id_name=pickle.load(open(root+'/teacherName', 'rb'))
        self.stop.extend(stopword)
        self.stop.extend(stopwords)
        self.fill = ['vn', 'n', 'nr', 'nr1', 'nr2', 'nrj', 'nrf', 'ns', 'nsf',
                'nt', 'nz', 'nl', 'ng']
        jieba.load_userdict('fenci/userdict.txt')
    def prints(self,result):
        for code in result:
            teacher=result[code]
            print(code)
            for t in teacher:
                print(self.id_name[t[0]]["name"])
            print()
    def do_query(self,text,filer):
        seg_list = pseg.cut(text)
        words = []
        for word, flag in seg_list:
            if flag in self.fill and word not in self.stop:
                words.append(word)

        if "school" in filer and len(filer["school"])>0:
            teacher_id={t for t in self.id_name if self.id_name[t]['school_id'] in filer['school']}
        else:
            teacher_id=None
        if "name" in filer and len(filer["name"])>0:
            if teacher_id:
                teacher_id={t for t in teacher_id if self.id_name[t]['name'].find(filer["name"])>=0}
            else:
                teacher_id = {t for t in self.id_name if self.id_name[t]['name'].find(filer["name"])>=0}
        result={}
        for sub in self.Subject:
            if "code" in filer and len(filer['code'])>0 and sub not in filer['code']:
                continue
            else:
                result[sub]=self.Subject[sub].do_query(words,teacher_id)
        return result

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
    a = Query(subject)
    # test = a.cal_lda_one_word(u'淋巴细胞')

    # test1 = ' '.join(jieba.cut(text,cut_all=False)).split()
    # test2 = ' '.join(jieba.cut_for_search(text)).split()

    # 时间测试1
    # start = time.time()
    # s1 = a.do_query(text1)
    # end = time.time()
    # print end - start

    #查询时间测试2
    # start = time.time()
    # s2 = a.do_query(text2)
    # end = time.time()
    # print end - start

    #查询时间测试3
    text=['人工智能','机器学习','贝叶斯','淋巴细胞','应答标拟器系统','白血病']
    filer={"code":{"01"},"school":{19037}}
    filer={}
    start = time.time()
    for t in text:
        print(t)
        r=a.do_query(t,filer)
        a.prints(r)
    end = time.time()
    print (end - start)




