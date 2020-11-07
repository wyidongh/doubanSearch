#/usr/bin/python
# -*- coding: UTF-8 -*-
import argparse
import re
import sys
import pymysql
import requests
import time
requests.packages.urllib3.disable_warnings()


def arg_parse():
	parser = argparse.ArgumentParser()
	parser.add_argument("-u", "--url",  required=True, help="The URL you want to search")
	return parser.parse_args() 

def get(url, param):
	r = requests.get(str(url), params=param, headers=header, verify=False)
	print(r.url)
	return r.text

def parse_content(content):
	#pattern = re.compile(r"<div id=\"content\">.+?(?:<tr class=\"\">.+?<td class=\"title\">.+?<a href=\"(.+?)\" title=\"(.+?)\".+?</a>.+?</td></tr>)*", re.M|re.S)
	pattern = re.compile(r"(?:<td class=\"title\">.+?<a href=\"(?P<title_link>(.+?))\" title=\"(?P<title>(.+?))\".+?</a>.+?</td>.+?<td nowrap=\"nowrap\">.+?<a href=\"(?P<author_profile>(.+?))\".+?\">(?P<author>(.+?))</a>.+?</td>.+?<td.+?class=\"time\">(?P<time>(.+?)))</td>", re.M|re.S)
	return pattern.finditer(content)

def write2mysql(host, user, passwd, db, table, data):
	db = pymysql.connect(host, user, passwd, db)
	cur = db.cursor()
	sqli="insert into %s values(%s, %s, %s, %s, %s)" % (table, "\"" +  data["author"] + "\"", "\"" + data["author_profile"] + "\"", "\"" + data["title"] + "\"", "\"" + data["title_link"] + "\"", "\"" + data["time"] + "\"")
	print(sqli)
	try:
		cur.execute(sqli)
	
		db.commit()
		print("commit OK")
	except Exception as m:
		print(m)
		db.rollback()
	db.close()

	

def main():
	#args = arg_parse()
	#print(args.u)
	global header
	header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36"}

	for i in range(count):
		print(i)
		parameters = {"start": i * 50}
		content = get(url, parameters)
		infors = parse_content(content)
		for infor in infors:
			msg = infor.groupdict()
			for keyword in keywords:
				if keyword in msg.get("title"):
					#print(msg)
					write2mysql(host, user, passwd, db, table, msg)
		

if __name__ == "__main__":
	url = "https://www.douban.com/group/shanghaizufang/discussion"
	keywords = ["9号线", "佘山", "泗泾", "九亭", "七宝"]
	count = 10
	host = "127.0.0.1"
	port = 3306
	user = "douban"
	passwd = "douban"
	db = "douban"
	table = "rent"
	main()


