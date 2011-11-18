#!/usr/bin/env python

import sqlite3
import sys
import subprocess

db = "sqlrepo.db"
filename = "sql.sql"
seperator = "=" * 50


class Connection(object):
	def __init__(self, database=db):
		try:
			self.datbase=database
			self.conn = sqlite3.connect(database)
			self.cur = self.conn.cursor()
		except Exception, e:
			print e

	def encode(self,dataset):
		return dataset[0].encode('utf-8'), dataset[1], dataset[2].encode('utf-8')


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
			file = open(filename, "wb")
			file.write(string)
		if sys.platform == 'linux2':
			subprocess.Popen('geany ' + filename, shell='False')
		else:
			subprocess.Popen('notepad.exe ' + filename, shell='True')


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

		        
	def showall(self):
		self.cur.execute('select customer, wonum, dataset from sqlrepo order by customer')
		allrows = self.cur.fetchall()
		for row in allrows:
			print self.encode(row)


	def search(self):
		wonum = raw_input("Please enter WO Number:")
		self.cur.execute('select customer, wonum, dataset from sqlrepo where wonum like ? order by customer', (wonum,))
		result = self.cur.fetchall()
		for row in result:
			if len(row) > 0:
				print self.encode(row)
			else:
				print 'No Results.'



def main():
	print seperator
	print "1. Retrieve SQL."
	print "2. Insert SQL."
	print "3. Search by WO Number."
	print "4. Show all Rows."
	option = raw_input("Select an option: ")
	if option == '1':
		c.get()
	elif option == '2':
		c.insert()
	elif option == '3':
		c.search()
		main()
	elif option == '4':
		c.showall()
		main()

if __name__ == '__main__':
	c = Connection()
	main()
