import sys
sys.path.append("../")
import utils

def getEntityRank(mention_set, ME_commonness):
	max_mention_len = max(len(mention.split()) for mention, entity in mention_set) if len(mention_set)>0 else 0
	max_mention_list = [(mention, entity) for mention, entity in mention_set if len(mention.split())==max_mention_len]
	entity_score = {}

	for mention, entity in max_mention_list:
		if entity not in entity_score:
			entity_score[entity] = (mention, ME_commonness[mention][entity])
		else:
			(mention_old, score_old) = entity_score[entity]
			if ME_commonness[mention][entity]>score_old:
				entity_score[entity] = (mention, ME_commonness[mention][entity])
	entity_rank = sorted(entity_score.items(), key=lambda e: e[1][1], reverse=True)
	return entity_rank

def getMentions(query, ME_commonness, threshold):
	max_length = 0
	N = len(query.split())
	mention_set = set()

	for n in range(N+1):
		ngram_list = utils.getNgram(query.lower(), n)
		for ngram in ngram_list:
			if ngram in ME_commonness:
				for entity in ME_commonness[ngram]:
					if ME_commonness[ngram][entity]>=threshold: mention_set.add((ngram, entity))
	return mention_set


threshold = 0.5

ME_commonness = utils.load_ME_cmns()

YERD = utils.parseYERD()
ClueWeb = utils.parseClueWeb()

#MD_out = "MD_YERD"+"_"+str(threshold)
#SM_out = "SM_YERD"+"_"+str(threshold)
MD_out = "MD_ClueWeb"+"_"+str(threshold)
SM_out = "SM_ClueWeb"+"_"+str(threshold)

MD_f = open(MD_out, "w")
SM_f = open(SM_out, "w")
SM_f.write("qid\tfreebase_id\tmention\tscore\n")

#for qid, query in YERD.items():
for qid, query in ClueWeb.items():
	mention_set = getMentions(query, ME_commonness, threshold)
	for mention, entity in mention_set:
		MD_f.write(qid+"\t"+entity+"\t"+mention+"\t"+str(ME_commonness[mention][entity])+"\n")

	entity_rank = getEntityRank(mention_set, ME_commonness)
	for i in range(len(entity_rank)):
		entity = entity_rank[i][0]
		(mention, score) = entity_rank[i][1]
		#SM_f.write(qid+"\t"+query+"\t"+entity+"\t"+mention+"\t"+str(score)+"\n")
		SM_f.write(qid+"\t"+entity+"\t"+mention+"\t"+str(score)+"\n")
MD_f.close()
SM_f.close()
