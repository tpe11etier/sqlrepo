#!/usr/bin/env python

import sqlite3
import os
import commands
import sys
import subprocess

db = "sqlrepo.db"
filename = "sql.txt"
seperator = "=" * 50


class Connection(object):
	def __init__(self, database=db,file=filename):
		self.datbase=database
		self.file=file
		self.conn = sqlite3.connect(database)
		self.cur = self.conn.cursor()
		
		
	def get(self):
		self.cur.execute("select distinct customer from sqlrepo")
		customers = self.cur.fetchall()
		custList = [a[0] for a in customers] 
		for cust in custList:
			print cust.encode('utf-8')
		customer = raw_input("Select the customer:")
		self.cur.execute("select distinct wonum from sqlrepo where customer = ?",[customer])
		wos = self.cur.fetchall()
		wosList = [a[0] for a in wos] 
		for w in wosList:
			print w
		wo = raw_input("Select the Work Order:")
		self.cur.execute("select dataset from sqlrepo where customer = ? and wonum = ?", (customer,wo))
		datasets = self.cur.fetchall()
		datasetsList = [a[0] for a in datasets] 
		for d in datasetsList:
			print d
		dataset = raw_input("Select DataSet:")
		
		self.cur.execute('select sql from sqlrepo where customer = ? and wonum = ? and dataset = ?', (customer,wo, dataset))
		allentries = self.cur.fetchall()
		for x in allentries:
			string = ''.join(x)
			print string
			file = open("sql.txt", "wb")
			file.write(string)
		subprocess.Popen('notepad.exe ' + filename)
	
		
	def insert(self):
		customer = raw_input("Please enter customer name:")
		print "You entered " + customer + ". Is this correct?"
		answer = raw_input("Enter Yes or No: ")
		if answer == 'No':
			customer = raw_input("Please enter customer name:")
		else:
			pass
		wonum = raw_input("Enter a WO Number: ")
		dataset = raw_input("Enter a DataSet value.  e.g. EX_AnswerSummary: ")
		filename = raw_input("Enter a File Name: ")
		file = open(filename,"rb")
		sql = file.read()
		
		self.conn.execute("insert into sqlrepo (customer, wonum, dataset, sql) values(?,?,?,?)", (customer,wonum,dataset,sql))
		self.conn.commit()

def main():
	print seperator
	print "1. Retrieve SQL."
	print "2. Insert SQL."
	option = raw_input("Select an option: ")
	if option == '1':
		c.get()
	elif option == '2':
		c.insert()
	
if __name__ == '__main__':
	c = Connection()
	main()
