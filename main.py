# -*- coding: utf-8 -*-

from excel_handler import ExcelHandler
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def main():
	if len(sys.argv) != 3:
		print "请输入个人网上问题数统计的时间段"
		print "eg: python main.py 2016-9-1 2016-12-31"
		sys.exit(0)
	start_time = sys.argv[1]
	end_time = sys.argv[2]
	excel_handler = ExcelHandler()
	excel_handler.create_static_workbook_sheet()
	excel_handler.write_static_data(start_time, end_time)

if __name__ == '__main__':
	main()