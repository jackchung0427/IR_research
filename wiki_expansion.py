import utils

dataset = "YERD"
predict_file = "TagMe/res_restricted/TagMe_YERD"
#predict_file = "CMN/res_restricted_new/IF_YERD_0.5-th0.3.txt"
out_filepath = dataset+"_wiki"
top = 100

IF_predict = utils.load_IF(predict_file)
out = open(out_filepath, "w")

for qid in IF_predict:
	print qid
	for s in range(len(IF_predict[qid])):
		res = qid
		original = list(IF_predict[qid][s])
		for i, entity in enumerate(original):
			if not utils.check_entity_facc1(qid, top, entity, dataset):
				IF_predict[qid][s].remove(entity)
		for i, entity in enumerate(IF_predict[qid][s]):
			if i==0:
				res += "\t1"
			res += "\t"+entity
		res += "\n"
		out.write("%s" % (res))
out.close()


