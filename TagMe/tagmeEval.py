import xml.etree.ElementTree as ET
import json
import sys
sys.path.append("../")
import tagme
import utils

def toFreebaseformat(q_entity, filepath, isRestricted):
	(wiki_map, freebase_map) = utils.loadWikiFreeMap()
	kb_sf = utils.loadKbSurfaceForm()
	out = open(filepath, "w")

	for qid in q_entity:
		res = qid
		for i, wiki_id in enumerate(q_entity[qid]):
			if i==0:
				res += "\t1"
			freebase_id = wiki_map[wiki_id][0] if wiki_id in wiki_map else ""
			if isRestricted and (freebase_id not in freebase_map or freebase_id not in kb_sf):
				continue
			res += "\t"+freebase_id
		res += "\n"
		out.write("%s" % (res))
	out.close()

def getQEntity(query_map, e_filepath):
	T = tagme.TagMe()
	q_entity = {}
	cnt = 0

	for qid, query in query_map.items():
		print (cnt, qid, query)
		e_map = T.getEntity(query, 0)
		q_entity[qid] = e_map
		cnt += 1
	T.close()

	out = open(e_filepath, "w")
	for qid in q_entity:
		jsonStr = json.dumps(q_entity[qid])
		out.write(qid+"\t"+jsonStr+"\n")
	out.close()
	return q_entity

def loadEntity(filepath, threshold):
	q_entity = {}
	for line in open(filepath):
		line = line.strip().split("\t", 1)
		qid = line[0]
		wiki_list = json.loads(line[1])
		q_entity[qid] = set()
		for wiki_id in wiki_list:
			rho = wiki_list[wiki_id]["rho"]
			if rho>=threshold:
				q_entity[qid].add(wiki_id)
	return q_entity


dataset = "YERD"
#dataset = "ClueWeb"
isRestricted = False
threshold = 0.3

out_dir = "res_restricted" if isRestricted else "res_nonrestricted"
output = out_dir+"/TagMe_"+dataset+"_"+str(threshold)
Q = utils.parseYERD() if dataset=="YERD" else utils.parseClueWeb()
e_filepath = dataset+"_wiki"

#tagMe_q_entity = getQEntity(Q, e_filepath)

tagMe_q_entity = loadEntity(e_filepath, threshold)
toFreebaseformat(tagMe_q_entity, output, isRestricted)
