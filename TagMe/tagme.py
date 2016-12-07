import xml.etree.ElementTree as ET
from selenium import webdriver
import re, json

class TagMe():
	token = "35b0db24-f570-499e-bbf1-73455fb43c2c"
	tagMe_host = "https://tagme.d4science.org/tagme/tag?lang=en&gcube-token="+token
	driver = webdriver.PhantomJS(executable_path="/Users/cyc520427/Desktop/phantomjs-2.1.1-macosx/bin/phantomjs")

	def getEntity(self, query, rho_filter):
		query = re.sub("\\W", " ", query)
		if len(query.strip())==0:
			return None
		q_url = self.tagMe_host+"&text="+query
		self.driver.get(q_url)
		body = self.driver.find_element_by_xpath("//body")
		jsonStr = json.loads(body.text)

		e_map = {}
		for entity in jsonStr["annotations"]:
			if float(entity["rho"])>=rho_filter:
				e_map[entity["id"]] = {}
				e_map[entity["id"]]["rho"] = entity["rho"]
				e_map[entity["id"]]["link_probability"] = entity["link_probability"]
				#q_entity.add(str(entity["id"]))
		return e_map

	def close(self):
		self.driver.close()


