import xml.etree.ElementTree as ET
import json
import re

def toFreebaseformat(q_entity, wiki_map, filepath):
	out = open(filepath, "w")
	for qid in q_entity:
		res = qid
		for i, wiki_id in enumerate(q_entity[qid]):
			if i==0:
				res += "\t1"
			freebase_id = wiki_map[wiki_id][0] if wiki_id in wiki_map else ""
			res += "\t"+freebase_id
		res += "\n"
		out.write("%s" % (res))
	out.close()

def loadKbSurfaceForm():
	sf_kb_filepath = "/Users/cyc520427/git/CMU/IR_research/resource/freebase_entity_snapshot.tsv"
	sf_entity = {}

	for line in open(sf_kb_filepath):
		line = line.strip().split("\t")
		mention = re.sub("^\"|\"@.*", "", line[1].lower())
		entity = line[0]
		sf_entity[entity] = mention
	return sf_entity

def load_ME_cmns():
	filepath = "/Users/cyc520427/git/CMU/IR_research/resource/cmns"
	(wiki_map, freebase_map) = loadWikiFreeMap()
	kb_sf = loadKbSurfaceForm()
	ME_commonness = {}

	for line in open(filepath):
		line = line.strip().split("\t")
		mention = line[0]
		entity = line[1]
		score = float(line[2])

		#exclude not in wiki & kb
		if entity not in freebase_map or entity not in kb_sf:
			continue
		if mention not in ME_commonness:
			ME_commonness[mention] = {}
		ME_commonness[mention][entity] = score
	return ME_commonness

def cal_ME_cmns():
	filepath = "/Users/cyc520427/git/CMU/IR_research/resource/GoogleSurfaceForm"
	ME_commonness = {}
	entity_set = set()

	for line in open(filepath):
		line = line.strip().split("\t")
		mention = line[0].lower()
		entity = line[1]
		cnt = float(line[2])

		if mention not in ME_commonness:
			ME_commonness[mention] = {}
		if entity not in ME_commonness[mention] or ME_commonness[mention][entity]<cnt:
			ME_commonness[mention][entity] = cnt
		entity_set.add(entity)

	for mention in ME_commonness:
		total_cnt = sum(ME_commonness[mention][entity] for entity in ME_commonness[mention])
		for entity in ME_commonness[mention]:
			ME_commonness[mention][entity] = ME_commonness[mention][entity]/total_cnt

	print ("size of knowledge base:%d" %(len(ME_commonness)))
	print ("size of knowledge base:%d" %(len(entity_set)))
	return ME_commonness

def loadWikiFreeMap():
	filepath = "/Users/cyc520427/git/CMU/IR_research/resource/AllWikiIdAlign"
	wiki_map = {}
	freebase_map = {}
	for line in open(filepath):
		line = line.strip().split("\t")
		wiki_id = line[0]
		freebase_id = line[1]
		name = line[2] if len(line)>2 else ""
		if len(wiki_id)>0 and len(freebase_id)>0:
			wiki_map[wiki_id] = (freebase_id, name)
			freebase_map[freebase_id] = (wiki_id, name)
	return (wiki_map, freebase_map)

def loadValidFreeEntity(filepath):
	valid_entity = set()
	valid_mention = set()
	for line in open(filepath):
		line = line.strip().split("\t")
		freebase_id = line[0]
		name = re.sub("^\"|\"@.*", "", line[1])
		valid_entity.add(freebase_id)
		valid_mention.add(name.lower())
	return (valid_entity, valid_mention)

def parseClueWeb(ground_truth_path=None):
	filepath = "/Users/cyc520427/git/CMU/IR_research/resource/ManualCandidate"
	ClueWeb = {}
	IF = {}
	(wiki_map, freebase_map) = loadWikiFreeMap()
	kb_sf = loadKbSurfaceForm()

	for line in open(filepath):
		line = line.strip().split("\t")
		qid = line[0]
		query = line[1]
		entity = line[2]
		if qid not in ClueWeb:
			ClueWeb[qid] = query
			IF[qid] = []
		if entity in freebase_map and entity in kb_sf:
			IF[qid].append(entity)

	if ground_truth_path!=None:
		ground_truth_f = open(ground_truth_path, "w")
		for qid in IF:
			ground_truth_f.write(qid+"\t1")
			for entity in IF[qid]:
				ground_truth_f.write("\t"+entity)
			ground_truth_f.write("\n")
		ground_truth_f.close()
	return ClueWeb

def parseYERD():
	filepath = "/Users/cyc520427/git/CMU/IR_research/EntityLinkingInQueries-ELQ/Y-ERD/Y-ERD.tsv"
	YERD = {}
	line_cnt = 0

	for line in open(filepath):
		line_cnt += 1
		if line_cnt==1:
			continue
		line = line.strip().split("\t")
		qid = line[1]
		query = line[2]
		YERD[qid] = query
	return YERD

def parseYSQLE(filepath):
	tree = ET.ElementTree(file=filepath)
	root = tree.getroot()
	YSQLE = {}

	for session_ele in tree.iterfind("session"):
		q_id = session_ele.attrib["id"]
		q_cnt = 1
		for query_ele in session_ele:
			query = query_ele.find("text").text

			key = q_id+"_"+str(q_cnt)
			YSQLE[key] = query
			q_cnt += 1
	return YSQLE

def getYSQLE_ans(filepath):
	tree = ET.ElementTree(file=filepath)
	root = tree.getroot()
	YSQLE_ans = {}

	for session_ele in tree.iterfind("session"):
		q_id = session_ele.attrib["id"]
		q_cnt = 1
		YSQLE_ans[q_id] = set()
		for query_ele in session_ele:
			annotations = query_ele.findall("annotation")
			for annotation in annotations:
				target = annotation.find("target")
				if target!=None:
					YSQLE_ans[q_id].add(str(target.attrib["wiki-id"]))
	return YSQLE_ans

def getNgram(string, N):
	word_seq = string.strip().split()
	ngram_list = [" ".join(n_tuple) for n_tuple in zip(*[word_seq[i:] for i in range(N)])]
	return ngram_list

def load_IF(filepath):
	IF = {}
	for line in open(filepath):
		line = line.strip().split("\t")
		qid = line[0]
		if qid not in IF:
			IF[qid] = []
		IF[qid].append(line[2:])
	return IF

