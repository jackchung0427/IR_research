import sys
import cmn
sys.path.append("../")
import utils

def exec_wiki_q(dataset, threshold):
	ME_commonness = utils.load_ME_cmns()
	YERD = utils.parseYERD()
	wiki_res_path = dataset+"_wiki"
	top = 10

	MD_out = "MD_wiki_"+dataset+"_"+str(threshold)
	MD_f = open(MD_out, "w")

	for qid, query in YERD.items():
		mention_set = set()
		wiki_list = utils.get_top_wiki(wiki_res_path, qid, top)
		for wiki in wiki_list:
			filepath = ""
			with open(filepath, "r") as content_file:
				content = content_file.read()
			common = cmn.CMN(content, threshold, ME_commonness)
			mention_set.update(common.getMentions())
		
                for mention, entity in mention_set:
			MD_f.write(qid+"\t"+entity+"\t"+mention+"\t"+str(ME_commonness[mention][entity])+"\n")
	MD_f.close()

def exec_original_q(dataset, threshold):
	ME_commonness = utils.load_ME_cmns()
	YERD = utils.parseYERD()
	ClueWeb = utils.parseClueWeb()

	MD_out = "MD_"+dataset+"_"+str(threshold)
	SM_out = "SM_"+dataset+"_"+str(threshold)
	MD_f = open(MD_out, "w")
	SM_f = open(SM_out, "w")
	SM_f.write("qid\tfreebase_id\tmention\tscore\n")

	for qid, query in YERD.items():
	#for qid, query in ClueWeb.items():
		print qid
		common = cmn.CMN(query, threshold, ME_commonness)
		mention_set = common.getMentions()
		for mention, entity in mention_set:
			MD_f.write(qid+"\t"+entity+"\t"+mention+"\t"+str(ME_commonness[mention][entity])+"\n")

		entity_rank = common.getEntityRank(mention_set)
		for i in range(len(entity_rank)):
			entity = entity_rank[i][0]
			(mention, score) = entity_rank[i][1]
			SM_f.write(qid+"\t"+entity+"\t"+mention+"\t"+str(score)+"\n")
	MD_f.close()
	SM_f.close()

dataset = "YERD"
#dataset = "ClueWeb"

threshold = 0.5
exec_original_q(dataset, threshold)
#exec_wiki_q(dataset, threshold)
