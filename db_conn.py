# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class DBConn(object):
	"""mysql连接类"""
	def __init__(self, **config):
		print("init DBConn instance...")
		self.config = config
		self.conn = None

	def __del__(self):
		self.release()

	def __enter__(self):
		pass

	def release(self):
		print("release DBConn...")
		self.close()
		sys.exit(1)

	def close(self):
		print("close mysql connection...")
		self.conn.close()

	def create_conn(self):
		print("create mysql connection...")
		self.conn = mdb.connect(host = self.config["host"], port = int(self.config["port"]),
			user = self.config["user"], passwd = self.config["passwd"], db = self.config["db"],
			charset = self.config["charset"]);

  	def get(self):
  		print("get a mysql connection...")
  		if self.conn is None:
  			self.create_conn()
  		
  		return self.conn
