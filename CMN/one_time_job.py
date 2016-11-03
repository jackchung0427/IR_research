import sys
sys.path.append("../")
import utils

def write_cmns():
	out = file("resource/cmns", "w")
	ME_commonness = utils.cal_ME_cmns()

	for mention in ME_commonness:
		for entity in ME_commonness[mention]:
			out.write(mention+"\t"+entity+"\t"+str(ME_commonness[mention][entity])+"\n")
	out.close()

write_cmns()
