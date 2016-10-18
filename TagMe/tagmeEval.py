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
			if float(entity["link_probability"])>=rho_filter:
				q_entity[qid].add(str(entity["id"]))
		cnt += 1
	driver.close()
	return q_entity

(wiki_map, freebase_map) = utils.loadWikiFreeMap()

#YSQLE_ans = getYSQLE_ans(YSQLE_filepath)
#toFreebaseformat(YSQLE_ans, wiki_map, output)

YSQLE_filepath = "Webscope_L24/ydata-search-query-log-to-entities-v1_0.xml"

#output = "TagMe_YSQLE"
output = "TagMe_YERD"

#YSQLE = parseYSQLE(YSQLE_filepath)
YERD = utils.parseYERD()

#tagMe_q_entity = getEntity(YSQLE)
tagMe_q_entity = getEntity(YERD)

toFreebaseformat(tagMe_q_entity, output)
