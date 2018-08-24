# coding=utf-8
import pickle
import networkx as nx
from config import root
def makeIndex(code,k):
    path = root+'/' + code + '/k' + str(k)
    teacherTopic=pickle.load(open(path + '/teacherTopic', 'rb'))
    G = nx.Graph()
    exp_to_topic = []
    topic_top_exp = []
    num=len(teacherTopic)
    for teacher in teacherTopic:
        for topic in teacherTopic[teacher]:
            exp_to_topic.append((teacher,"topic_"+str(topic), teacherTopic[teacher][topic]))
            topic_top_exp.append(("topic_"+str(topic),teacher, teacherTopic[teacher][topic]*10/num))
    G.add_weighted_edges_from(exp_to_topic)
    G.add_weighted_edges_from(topic_top_exp)
    print("computer")
    layout = nx.spring_layout(G)
    nx.draw_networkx(G)
    pr = nx.pagerank(G, alpha=0.85)

    dmin = min(pr.items(), key=lambda x: x[1])[1]
    dmax = max(pr.items(), key=lambda x: x[1])[1]
    nx.draw_networkx(G, pos=layout, node_size=[x * 6000 for x in pr.values()], node_color='m', with_labels=True)
    teacherRank={}
    for node, pageRankValue in pr.items():
        if type(node)==str:
            continue
        teacherRank[node]=(pageRankValue - dmin) / (dmax - dmin)
    pickle.dump(teacherRank,open(path + '/teacherRank', 'wb'))

def makeSchoolIndex(code, k):
    path = root+'/' + code + '/k' + str(k)
    schoolTopic = pickle.load(open(path + '/schoolTopic', 'rb'))
    G = nx.Graph()
    exp_to_topic = []
    topic_top_exp = []
    num = len(schoolTopic)
    for school in schoolTopic:
        for topic in schoolTopic[school]:
            exp_to_topic.append((school, "topic_" + str(topic), schoolTopic[school][topic]))
            topic_top_exp.append(("topic_" + str(topic), school, schoolTopic[school][topic] * 10 / num))
    G.add_weighted_edges_from(exp_to_topic)
    G.add_weighted_edges_from(topic_top_exp)
    print("computer")
    layout = nx.spring_layout(G)
    nx.draw_networkx(G)
    pr = nx.pagerank(G, alpha=0.85)

    dmin = min(pr.items(), key=lambda x: x[1])[1]
    dmax = max(pr.items(), key=lambda x: x[1])[1]
    nx.draw_networkx(G, pos=layout, node_size=[x * 6000 for x in pr.values()], node_color='m', with_labels=True)
    schoolRank = {}
    for node, pageRankValue in pr.items():
        if type(node) == str:
            continue
        schoolRank[node] = (pageRankValue - dmin) / (dmax - dmin)
    pickle.dump(schoolRank, open(path + '/schoolRank', 'wb'))
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
        makeIndex(sub['code'],sub['k'])
        makeSchoolIndex(sub['code'], sub['k'])