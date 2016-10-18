import sys
sys.path.append("../")
import utils

class CMN():
	def __init__(self, query, threshold, ME_commonness=None):
		self.query = query
		self.threshold = threshold
		if ME_commonness==None:
			self.ME_commonness = utils.load_ME_cmns()
		else:
			self.ME_commonness = ME_commonness

	def getEntityRank(self, mention_set):
		max_mention_len = max(len(mention.split()) for mention, entity in mention_set) if len(mention_set)>0 else 0
		max_mention_list = [(mention, entity) for mention, entity in mention_set if len(mention.split())==max_mention_len]
		entity_score = {}

		for mention, entity in max_mention_list:
			if entity not in entity_score:
				entity_score[entity] = (mention, self.ME_commonness[mention][entity])
			else:
				(mention_old, score_old) = entity_score[entity]
				if self.ME_commonness[mention][entity]>score_old:
					entity_score[entity] = (mention, self.ME_commonness[mention][entity])
		entity_rank = sorted(entity_score.items(), key=lambda e: e[1][1], reverse=True)
		return entity_rank

	def getMentions(self):
		max_length = 0
		N = min(len(self.query.split()), 10)
		mention_set = set()

		for n in range(N+1):
			ngram_list = utils.getNgram(self.query.lower(), n)
			for ngram in ngram_list:
				if ngram in self.ME_commonness:
					for entity in self.ME_commonness[ngram]:
						if self.ME_commonness[ngram][entity]>=self.threshold:
							mention_set.add((ngram, entity))
		return mention_set

