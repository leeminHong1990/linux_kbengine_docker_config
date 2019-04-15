# -*- coding:utf-8 -*-
import os
import re
import random
import xml.etree.ElementTree as ET

class xml(object):

	def __init__(self, xml):
		self.xml = xml
		self.tree = ET.parse(xml)
		self.root = self.tree.getroot()

	def chXMLNode(self, value, *args):
		cursor = self.findNode(*args)
		try:
			cursor.text = value
			# cursor.set(key, value)
			self.tree.write(self.xml, encoding="utf-8")
		except:
			err, msg, stack = sys.exc_info()
			print("chXMLNode error; exc_info: {} ,{}".format(err, msg))

	def addXMLNode(self, key, value, *args):
		cursor = self.findNode(*args)
		if cursor.find(key) is not None:
			self.removeXMLNode(key, *args)
		try:
			newEle = ET.Element(key)
			newEle.text = value
			cursor.append(newEle)
			self.tree.write(self.xml, encoding="utf-8")
		except:
			err, msg, stack = sys.exc_info()
			print("chXMLNode error; exc_info: {} ,{}".format(err, msg))

	def removeXMLNode(self, key, *args):
		cursor = self.findNode(*args)
		try:
			cursor.remove(cursor.find(key))
			self.tree.write(self.xml, encoding="utf-8")
		except:
			err, msg, stack = sys.exc_info()
			print("chXMLNode error; exc_info: {} ,{}".format(err, msg))


	def findNode(self, *args):
		cursor = self.root
		for i in range(len(args)):
			key = args[i]
			next_cursor = cursor.find(key)
			if next_cursor is not None:
				cursor = next_cursor
			else:
				return None
		return cursor

def configurate_dockerfile(**kwargs):
	path = "./Dockerfile"
	if not os.path.exists(path):
		return
	with open(path, "r") as r_f:
		lines = r_f.readlines()
		r_f.close()

	with open(path, "w") as w_f:
		for w_str in lines:
			# print(w_str)
			w_str = w_str.replace('{uid}', str(kwargs["id"] + 65536 + 1))
			# w_str = w_str.replace('{user}', str(kwargs["name"]).lower())
			w_f.write(w_str)
			print(w_str)
		w_f.close()

def configurate_docker_compose(**kwargs):
	path = "./docker-compose.yml"
	if not os.path.exists(path):
		return
	with open(path, "r") as r_f:
		lines = r_f.readlines()
		r_f.close()

	with open(path, "w") as w_f:
		for w_str in lines:
			# print(w_str)
			w_str = w_str.replace('{service_name}', str(kwargs["name"]).lower())
			w_str = w_str.replace('{container_name}', kwargs["name"])
			w_str = w_str.replace('{port0}', str(kwargs["loginPort"]))
			w_str = w_str.replace('{port1}', str(kwargs["basePort"]))
			w_str = w_str.replace('{port2}', str(kwargs["baseTelnetPort"]))
			w_str = w_str.replace('{port3}', str(kwargs["cellTelnetPort"]))
			w_f.write(w_str)
			print(w_str)
		w_f.close()

def configurate_kbengine_xml(**kwargs):
	path = "../kbengine/assets/res/server/kbengine.xml"
	if not os.path.exists(path):
		return

	name 			= kwargs["name"]
	basePort 		= kwargs["basePort"]
	baseTelnetPort 	= kwargs["baseTelnetPort"]
	cellTelnetPort 	= kwargs["cellTelnetPort"]
	ip 				= kwargs["ip"]

	# xml
	xml_obj = xml(path)

	# telnet
	xml_obj.chXMLNode(str(baseTelnetPort), "baseapp", "telnet_service", "port")
	xml_obj.chXMLNode(str(cellTelnetPort), "cellapp", "telnet_service", "port")

	# base external port
	xml_obj.addXMLNode("externalPorts_min", str(basePort), "baseapp")
	xml_obj.addXMLNode("externalPorts_max", str(basePort), "baseapp")

	# base external ip
	xml_obj.chXMLNode(str(ip), "baseapp", "externalAddress")

	# DB
	xml_obj.chXMLNode("kbe_" + str(name), "dbmgr", "databaseInterfaces", "default", "databaseName")
	# xml_obj.chXMLNode("kbe", "dbmgr", "databaseInterfaces", "default", "auth", "username")
	xml_obj.chXMLNode(str(ip), "dbmgr", "databaseInterfaces", "default", "host")

def configurate_kbengine_bash(id):
	path = "../kbengine/assets/start_server.sh"
	if not os.path.exists(path):
		return
	with open(path, "r") as r_f:
		lines = r_f.readlines()
		r_f.close()

	p = r"\d{3,}"  # 匹配数字至少3次
	pattern = re.compile(p)

	with open(path, "w") as w_f:
		for i in range(len(lines)):
			# print(w_str)
			out = re.sub(pattern, str(id * 100000000000 + i), lines[i])
			w_f.write(out)
			print(out)
		w_f.close()

def configurate_client_switch(**kwargs):
	path = "../cocos/src/switch.js"
	if not os.path.exists(path):
		return
	
	with open(path , "rb") as r_f:
		lines = r_f.readlines()
		r_f.close()

	with open(path, "wb+") as w_f:
		for line in lines:
			line = line.decode("utf-8")
			if line.find("switches.kbeServerIP") >= 0:
				w_f.write("switches.kbeServerIP = \"{}\";\r\n".format(kwargs["ip"]).encode('utf-8'))
			elif line.find("switches.kbeServerLoginPort") >= 0:
				w_f.write("switches.kbeServerLoginPort = {};\r\n".format(kwargs["loginPort"]).encode('utf-8'))
			else:
				w_f.write(line.encode('utf-8'))
			# print(out)
		w_f.close()

if __name__ == "__main__":

	# parse args
	import argparse
	parser = argparse.ArgumentParser(description='build')
	parser.add_argument("--name")
	parser.add_argument("--id")
	parser.add_argument("--ip")
	parser.add_argument("--db")
	args = parser.parse_args()

	args.id = args.id or random.randint(3, 10)
	args.id = int(args.id)

	args.name = args.name or str(args.id)

	loginPort = 20013 + args.id
	basePort = 30000 + args.id
	baseTelnetPort = 40000 + args.id
	cellTelnetPort = 50000 + args.id

	print('--name:{0} --id:{1} --loginPort:{2} --basePort:{3} --baseTelnetPort:{4} --cellTelnetPort:{5}'.format(args.name, args.id, loginPort, basePort, baseTelnetPort, cellTelnetPort))

	configurate_dockerfile(name=args.name, id=args.id)

	# configurate docker-compose.yml
	configurate_docker_compose(name=args.name, id=args.id, loginPort=loginPort, basePort=basePort, baseTelnetPort=baseTelnetPort, cellTelnetPort=cellTelnetPort)

	# configurate kbengine/assets/res/server/kbengine.xml
	configurate_kbengine_xml(name=args.name, basePort=basePort, baseTelnetPort=baseTelnetPort, cellTelnetPort=cellTelnetPort, ip="192.168.1.52")

	# configurate kbengine/assets/start_server.sh
	configurate_kbengine_bash(args.id)

	# configurate kbengine/assets/start_server.sh
	configurate_client_switch(ip="192.168.1.52", loginPort=loginPort)

