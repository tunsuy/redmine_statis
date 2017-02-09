# -*- coding: utf-8 -*-

from db_conn import DBConn
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class DataHandler(object):
	"""数据操作类"""

	def __init__(self, **conf):
		print("conf: {}".format(conf))
		print("init DataHandler instance...")
		self.init_data()
		self.__set_cursor(conf)

	def init_data(self):
		self.proj_versions_info = None
		self.issue_statuses_info = None
		self.issue_trackers_info = None
		self.users_info = None
		self.proj_modules_name = None

	def __set_cursor(self, conf):
		print("set mysql connection cursor...")
		self.mdbconn = DBConn(**conf)
		self.conn = self.mdbconn.get()
		with self.conn:
			self.cursor = self.conn.cursor()

	def select_db_data_list(self, sql_str):
		print("sql: {}".format(sql_str))
		self.cursor.execute(sql_str)
		db_data = self.cursor.fetchall()		
		return db_data
	
	'''=================================================='''	
	def get_users_list(self):
		""" 获取用户信息列表，采用了内存缓存的机制
			返回：dictionary类型元素的list """
		print("get project versinons data...")
		if self.users_info is None:
			self.users_info = self.__get_users_from_db()
		return self.users_info

	def __get_users_from_db(self):
		print("get users data from db...")
		sql = "SELECT id, firstname, lastname FROM users WHERE type = 'User'"
		users_info = self.select_db_data_list(sql)
		users_info_list = []
		for index in xrange(len(users_info)):
			user_info = {
				"id": users_info[index][0],
				"name": (users_info[index][1] + users_info[index][2])
			}
			users_info_list.append(user_info)
		return users_info_list

	def __get_user_id_with_name(self, user_name):
		users_info = self.get_users_list()
		for user_info in users_info:
			if user_info["name"] == user_name:
				return user_info["id"]

	'''==================================================='''
	def get_proj_versions_list(self):
		""" 获取项目版本列表，采用了内存缓存的机制
			返回：dictionary类型元素的list """
		print("get project versinons data...")
		if self.proj_versions_info is None:
			self.pro_versions_info = self.__get_proj_versions_from_db()
		return self.pro_versions_info

	def __get_proj_versions_from_db(self):
		print("get project versinons data from db...")
		sql = "SELECT id, name FROM versions WHERE project_id = 1" #指定为MOA迭代项目
		proj_versions_info = self.select_db_data_list(sql)
		return self.__tuple_tuple_to_dic_list(proj_versions_info)

	def __get_proj_version_id_with_name(self, version_name):
		proj_versions_info = self.get_proj_versions_list()
		for proj_version_info in proj_versions_info:
			if proj_version_info["name"] == version_name:
				return proj_version_info["id"]

	'''============================================'''
	def get_issue_trackers_list(self):
		""" 获取问题跟踪列表，采用了内存缓存的机制 
			返回：dictionary类型元素的list """
		print("get issue trackers data...")
		if self.issue_trackers_info is None:
			self.issue_trackers_info = self.__get_issue_trackers_from_db()
		return self.issue_trackers_info

	def __get_issue_trackers_from_db(self):
		print("get issue trackers data from db...")
		sql = "SELECT id, name FROM trackers"
		trackers_info = self.select_db_data_list(sql)
		return self.__tuple_tuple_to_dic_list(trackers_info)

	'''============================================='''
	def get_issue_statuses_list(self):
		""" 获取问题状态列表，采用了内存缓存的机制 
			返回：dictionary类型元素的list """
		print("get issue statuses data...")
		if self.issue_statuses_info is None:
			self.issue_statuses_info = self.__get_issue_statuses_from_db()
		return self.issue_statuses_info

	def __get_issue_statuses_from_db(self):
		print("get issue statuses data from db...")
		sql = "SELECT id, name FROM issue_statuses"
		issue_statuses_info = self.select_db_data_list(sql)
		return self.__tuple_tuple_to_dic_list(issue_statuses_info)

	'''================================================='''
	def get_proj_modules_name_list(self):
		""" 获取项目模块列表，采用了内存缓存的机制 
			返回：模块name的list """
		print("get project modules name...")
		if self.proj_modules_name is None:
			self.proj_modules_name = self.__get_proj_modules_name_from_db()
		return self.proj_modules_name

	def __get_proj_modules_name_from_db(self):
		print("get project modules name from db...")
		sql = "SELECT possible_values FROM custom_fields WHERE id = 2"
		proj_modules = self.select_db_data_list(sql)
		proj_modules_name = proj_modules[0][0].encode("utf-8").split("-")
		proj_modules_name_real = []
		for proj_module_name in proj_modules_name:
			if proj_module_name.strip() != "":
				proj_modules_name_real.append(proj_module_name.strip())
		
		return proj_modules_name_real

	'''=================================================='''
	def __tuple_tuple_to_dic_list(self, tuple_tuple_data):
		""" 将tuple元素的tuple转换为dic元素的list
			注：只针对获取db中字段为id和name的情况 """
		dic_list = []
		for index in xrange(0, len(tuple_tuple_data)):
			dic_data = {
				"id": tuple_tuple_data[index][0],
				"name": tuple_tuple_data[index][1]
			}
			dic_list.append(dic_data)
		return dic_list

	'''=================================================='''
	def __person_bug_with_trackers_id(self, bug_trackers ,not_in_flag):
		""" 获取个人迭代bug数统计之tracker条件列表
			返回：trackers条件id """
		trackers_info = self.get_issue_trackers_list()
		trackers_id = "("
		for tracker_info in trackers_info:
			if not_in_flag == True:
				if tracker_info["name"] not in bug_trackers:
					trackers_id += str(tracker_info["id"]) + ","
			elif not_in_flag == False:
				if tracker_info["name"] in bug_trackers:
					trackers_id += str(tracker_info["id"]) + ","
			
		if trackers_id != "(":
			trackers_id = trackers_id.strip()[0:-1] + ")"
		else:
			trackers_id = "()"
		print("bug for trackers_id: {}".format(trackers_id))
		return trackers_id

	def __person_bug_with_statuses_id(self, bug_statuses, not_in_flag):
		""" 获取个人迭代bug数统计之statuses条件列表
			返回：trackers条件id """
		statuses_info = self.get_issue_statuses_list()
		statuses_id = "("
		for status_info in statuses_info:
			if not_in_flag == True:
				if status_info["name"] not in bug_statuses:
					statuses_id += str(status_info["id"]) + ","
			elif not_in_flag == False:
				if status_info["name"] in bug_statuses:
					statuses_id += str(status_info["id"]) + ","
			
		if statuses_id != "(":
			statuses_id = statuses_id.strip()[0:-1] + ")"
		else:
			statuses_id = "()"
		print("bug for statuses_id: {}".format(statuses_id))
		return statuses_id

	def get_person_version_bug_count(self, person_name, proj_version_name):
		""" 个人迭代bug数：发现版本custom_field_id=5
				只统计project_id=1（MOA迭代项目）
			cond: 跟踪标签 = 错误 + 网上问题 + 问题
				  问题状态 != 拒绝
			返回：某人某版本的bug数
		"""
		person_bug_trackers = ["错误", "网上问题", "问题"]
		trackers_id = self.__person_bug_with_trackers_id(person_bug_trackers, False)

		person_bug_not_statuses = ["拒绝"]
		statuses_id = self.__person_bug_with_statuses_id(person_bug_not_statuses, True)

		person_id = self.__get_user_id_with_name(person_name)
		proj_version_id = self.__get_proj_version_id_with_name(proj_version_name)

		# sql = "SELECT COUNT(*) FROM (issues a INNER JOIN custom_values b ON a.id = b.customized_id" \
		# 	" AND a.tracker_id in{} AND a.project_id = {} AND a.status_id in {} AND a.assigned_to_id = {})" \
		# 	" INNER JOIN custom_fields c ON b.custom_field_id = c.id AND c.id = {} AND b.value = {}" \
		# 	.format(trackers_id, 1, statuses_id, person_id, 5, proj_version_id)

		issues_filter_sql = "SELECT id FROM issues WHERE tracker_id in{} AND project_id = 1 AND status_id in {}" \
			" AND assigned_to_id = {}".format(trackers_id, statuses_id, person_id)

		custom_values_version_sql = "SELECT customized_id AS id FROM custom_values" \
			" WHERE custom_field_id = 5 AND value = {}" \
			.format(proj_version_id)

		sql = "SELECT COUNT(issues_filter.id) FROM ({})issues_filter LEFT JOIN ({})custom_values_version" \
			" USING(id) WHERE custom_values_version.id is not null" \
			.format(issues_filter_sql, custom_values_version_sql)

		person_bug_count = self.select_db_data_list(sql)
		print("person_bug_count: {}".format(person_bug_count[0][0]))

		return person_bug_count[0][0]

	def get_module_version_bug_count(self, module_name, proj_version_name):
		""" 模块迭代bug数：模块custom_field_id=2，发现版本custom_field_id=5
				只统计project_id=1（MOA迭代项目）
			cond: 跟踪标签 = 错误 + 网上问题
				  问题状态 != 拒绝
			返回：某模块某版本的bug数
		"""
		print("query for module_name {} and proj_version_name {}".format(module_name, proj_version_name))

		module_bug_trackers = ["错误", "网上问题"]
		trackers_id = self.__person_bug_with_trackers_id(module_bug_trackers, False)

		module_bug_not_statuses = ["拒绝"]
		statuses_id = self.__person_bug_with_statuses_id(module_bug_not_statuses, True)

		proj_version_id = self.__get_proj_version_id_with_name(proj_version_name)

		issues_filter_sql = "SELECT id FROM issues WHERE tracker_id in{} AND project_id = 1 AND status_id in {}" \
			.format(trackers_id, statuses_id)

		custom_values_module_sql = "SELECT customized_id AS id FROM custom_values" \
			" WHERE custom_field_id = 2 AND value = '{}'" \
			.format(module_name)

		custom_values_version_sql = "SELECT customized_id AS id FROM custom_values" \
			" WHERE custom_field_id = 5 AND value = {}" \
			.format(proj_version_id)

		issue_module_sql = "SELECT issues_filter.id FROM ({})issues_filter LEFT JOIN ({})custom_values_module USING(id)" \
			" WHERE custom_values_module.id is not null" \
			.format(issues_filter_sql, custom_values_module_sql)

		sql = "SELECT count(issues_module.id) FROM ({})issues_module LEFT JOIN ({})custom_values_version USING(id)" \
			" WHERE custom_values_version.id is not null" \
			.format(issue_module_sql, custom_values_version_sql)

		module_bug_count = self.select_db_data_list(sql)
		print("module_bug_count: {}".format(module_bug_count[0][0]))

		return module_bug_count[0][0]

	def get_person_online_issue_count(self, person_name, start_time, end_time):
		""" 个人网上问题数：只统计project_id=1（MOA迭代项目）
			cond: 跟踪标签 = 网上问题
				  问题状态 != 拒绝
			返回：某人某个时间段的网上问题数
		"""
		person_bug_trackers = ["网上问题"]
		trackers_id = self.__person_bug_with_trackers_id(person_bug_trackers, False)

		person_bug_not_statuses = ["拒绝"]
		statuses_id = self.__person_bug_with_statuses_id(person_bug_not_statuses, True)

		person_id = self.__get_user_id_with_name(person_name)

		sql = "SELECT COUNT(id) FROM issues WHERE tracker_id in{} AND project_id = 1 AND status_id in {}" \
			" AND assigned_to_id = {} AND created_on > '{}' AND created_on < '{}'" \
			.format(trackers_id, statuses_id, person_id, start_time, end_time)

		person_online_count = self.select_db_data_list(sql)
		print("person_online_count: {}".format(person_online_count[0][0]))

		return person_online_count[0][0]

	def get_person_not_finish_issue_count(self, person_name):
		""" 个人遗留问题数：只统计project_id=1（MOA迭代项目）
			cond: 跟踪标签 = 网上问题+问题+错误
				  问题状态 = 新建+进行中+后续再解决
			返回：某人某个时间段的网上问题数
		"""
		person_bug_trackers = ["网上问题", "问题", "错误"]
		trackers_id = self.__person_bug_with_trackers_id(person_bug_trackers, False)

		person_bug_statuses = ["新建", "进行中", "后续再解决"]
		statuses_id = self.__person_bug_with_statuses_id(person_bug_statuses, False)

		person_id = self.__get_user_id_with_name(person_name)

		sql = "SELECT COUNT(id) FROM issues WHERE tracker_id in{} AND project_id = 1 AND status_id in {}" \
			" AND assigned_to_id = {}" \
			.format(trackers_id, statuses_id, person_id)

		person_not_finish_count = self.select_db_data_list(sql)
		print("person_not_finish_count: {}".format(person_not_finish_count[0][0]))

		return person_not_finish_count[0][0]

	def get_person_version_work_weight(self, person_name, proj_version_name):
		""" 个人迭代工作粒度：解决版本custom_field_id=9；工作粒度custom_field_id=7
				只统计project_id=1（MOA迭代项目）
			cond: 跟踪标签 = 功能
				  问题状态 = 已回归+已解决
			返回：某人某个时间段的网上问题数
		"""
		person_bug_trackers = ["功能"]
		trackers_id = self.__person_bug_with_trackers_id(person_bug_trackers, False)

		person_bug_statuses = ["已回归", "已解决"]
		statuses_id = self.__person_bug_with_statuses_id(person_bug_statuses, False)

		person_id = self.__get_user_id_with_name(person_name)
		proj_version_id = self.__get_proj_version_id_with_name(proj_version_name)

		issues_filter_sql = "SELECT id FROM issues WHERE tracker_id in{} AND project_id = 1 AND status_id in {}" \
			" AND assigned_to_id = {}".format(trackers_id, statuses_id, person_id)

		custom_values_version_sql = "SELECT customized_id AS id FROM custom_values" \
			" WHERE custom_field_id = 9 AND value = {}" \
			.format(proj_version_id)

		weight_issue_sql = "SELECT issues_filter.id FROM ({})issues_filter LEFT JOIN ({})custom_values_version" \
			" USING(id) WHERE custom_values_version.id is not null" \
			.format(issues_filter_sql, custom_values_version_sql)

		sql = "SELECT value FROM custom_values WHERE customized_id in ({}) AND custom_field_id = 7".format(weight_issue_sql)

		person_version_weight_tuple = self.select_db_data_list(sql)
		print("person_version_weight_tuple: {}".format(person_version_weight_tuple))
		person_version_weight_sum = 0
		for person_version_weight in person_version_weight_tuple:
			if person_version_weight[0] == "":
				continue
			person_version_weight_sum += int(person_version_weight[0])
		print("person_version_weight_sum: {}".format(person_version_weight_sum))

		return person_version_weight_sum
