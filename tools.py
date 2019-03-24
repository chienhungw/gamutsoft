#!/usr/bin/python
# encoding:utf8
import xlrd

excel = xlrd.open_workbook("tmp.xls")
table = excel.sheet_by_index(0)
rows = table.get_rows()
date_list = table.row_values(3, start_colx=4)
print(date_list)
# print(table.cell(3, 3).value == "姓名")
user = table.col_values(3, start_rowx=4, end_rowx=None)  # 获取操作人员信息
schedule = table.col_values(0 + 4, start_rowx=4, end_rowx=None)  # 获取排班信息
print(user)
print(schedule)
# name_list = table.col_values(3, start_rowx=4)
# print(name_list)
# from datetime import date, timedelta
#
# begin = date(year=1970, month=1, day=1)
# print(begin + timedelta(days=date_list[0] - 1))
