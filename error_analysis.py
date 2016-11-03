import sys, random
sys.path.append("../")
import utils

def write_entity_map(IF_list, out):
	entity = []
	for IF in IF_list:
		for e in IF:
			if e not in entity:
				entity.append(e)
	for e in entity:
		out.write("\t"+e+"="+sf[e])
	out.write("\n")

def err_analysis(IF_groundtruth, IF_predict, qid_map, err_filepath):
	out = open(err_filepath, "w")
	for qid in IF_groundtruth:
		if qid not in IF_predict:
			if  len(IF_groundtruth[qid][0])==0:
				continue
			out.write(qid+"\t"+qid_map[qid]+"\t"+str(IF_groundtruth[qid]))
			write_entity_map(IF_groundtruth[qid], out)
			out.write(qid+"\t"+qid_map[qid]+"\tNone\n")
		else:
			mis_IF = []
			predict_entity = list(IF_predict[qid])
			for IF in IF_groundtruth[qid]:
				if IF in IF_predict[qid]:
					IF_predict[qid].remove(IF)
				else:
					mis_IF.append(IF)
			if len(mis_IF)>0 or len(IF_predict[qid])>0:
				out.write(qid+"\t"+qid_map[qid]+"\t"+str(mis_IF))
				write_entity_map(mis_IF, out)
				out.write(qid+"\t"+qid_map[qid]+"\t"+str(predict_entity))
				write_entity_map(predict_entity, out)
	out.close()

def sample_err(filepath, ratio, out_filepath):
	out = file(out_filepath, "w")
	lines = open(filepath).readlines()
	for i in range(len(lines)):
		if i%2==0:
			ground_truth = lines[i].strip()
			predict = lines[i+1].strip()
			r = random.uniform(0, 1)
			if r<=ratio:
				out.write(ground_truth+"\n")
				out.write(predict+"\n")
	out.close()

'''		
filepath = "err_out"
ratio = 0.5

out_filepath = filepath+"_"+str(ratio)
sample_err(filepath, ratio, out_filepath)
'''

#'''
#ground_truth_file = "EntityLinkingInQueries-ELQ/qrels/IF/qrels_IF_Y-ERD.txt"
ground_truth_file = "resource/ClueWeb_ans"

predict_file = "cmn/res_restricted_new/IF_YERD_0.5-th0.3.txt"
predict_file = "CMN/res_restricted_new/IF_ClueWeb_0.5-th0.3.txt"

predict_file = "TagMe/res_restricted/TagMe_YERD"

#Q_MAP = utils.parseYERD()
Q_MAP = utils.parseClueWeb()

sf = utils.loadKbSurfaceForm()
IF_groundtruth = utils.load_IF(ground_truth_file)
IF_predict = utils.load_IF(predict_file)

err_filepath = "err_out"

err_analysis(IF_groundtruth, IF_predict, Q_MAP, err_filepath)
#'''
