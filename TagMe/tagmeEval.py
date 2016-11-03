import xml.etree.ElementTree as ET
from selenium import webdriver
import json
import sys
sys.path.append("../")
import utils

def toFreebaseformat(q_entity, filepath):
	(wiki_map, freebase_map) = utils.loadWikiFreeMap()
	kb_sf = utils.loadKbSurfaceForm()
	out = open(filepath, "w")

	for qid in q_entity:
		res = qid
		for i, wiki_id in enumerate(q_entity[qid]):
			if i==0:
				res += "\t1"
			freebase_id = wiki_map[wiki_id][0] if wiki_id in wiki_map else ""
			if freebase_id not in freebase_map or freebase_id not in kb_sf:
				continue
			res += "\t"+freebase_id
		res += "\n"
		out.write("%s" % (res))
	out.close()

def getEntity(query_map, rho_filter=0.1):
	token = "35b0db24-f570-499e-bbf1-73455fb43c2c"
	tagMe_host = "https://tagme.d4science.org/tagme/tag?lang=en&gcube-token="+token
	driver = webdriver.PhantomJS(executable_path="/Users/cyc520427/Desktop/phantomjs-2.1.1-macosx/bin/phantomjs")
	q_entity = {}
	cnt = 0

	for qid, query in query_map.items():
		print (cnt, qid, query)
		q_url = tagMe_host+"&text="+query
		driver.get(q_url)
		body = driver.find_element_by_xpath("//body")
		jsonStr = json.loads(body.text)

		q_entity[qid] = set()
		for entity in jsonStr["annotations"]:
			#if float(entity["link_probability"])>=rho_filter:
			if float(entity["rho"])>=rho_filter:
				q_entity[qid].add(str(entity["id"]))
		cnt += 1
	driver.close()
	return q_entity

def loadEntity(filepath):
	q_entity = {}
	for line in open(filepath):
		line = line.strip().split("\t")
		qid = line[0]
		wiki_list = line[1:]
		q_entity[qid] = set()
		q_entity[qid].update(wiki_list)
	return q_entity


output = "TagMe_YERD"
#output = "TagMe_ClueWeb"

YERD = utils.parseYERD()
ClueWeb = utils.parseClueWeb()

#tagMe_q_entity = getEntity(YERD)
#tagMe_q_entity = getEntity(ClueWeb)

e_filepath = "YERD_wiki"
#e_filepath = "ClueWeb_wiki"
tagMe_q_entity = loadEntity(e_filepath)

toFreebaseformat(tagMe_q_entity, output)
