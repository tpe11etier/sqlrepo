#!/usr/bin/env python

import sqlite3
import sys
import subprocess

db = 'sqlrepo.db'
filename = 'sql.sql'
seperator = '=' * 50


class Connection(object):
	def __init__(self, database=db):
		try:
			self.datbase=database
			self.conn = sqlite3.connect(database)
			self.cur = self.conn.cursor()
		except Exception, e:
			print e

	def encode(self,string):
		return string.encode('utf-8')


	def get(self):
		self.cur.execute('select distinct customer from sqlrepo')
		customers = self.cur.fetchall()
		custList = [a[0] for a in customers]
		print '\n---Customers---'
		print seperator
		for cust in custList:
			print cust.encode('utf-8')
		print ''
		customer = raw_input('Select the customer:')
		self.cur.execute('select wonum from sqlrepo where customer like ?',[customer])
		wos = self.cur.fetchall()
		wosList = [a[0] for a in wos]
		print '\n---WO Numbers---'
		print seperator
		for w in wosList:
			print w
		print ''
		wo = raw_input('Select the Work Order:')
		self.cur.execute('select dataset from sqlrepo where customer like ? and wonum = ?', (customer,wo))
		datasets = self.cur.fetchall()
		datasetsList = [a[0] for a in datasets]
		print '\n---Data Sets---'
		print seperator
		for d in datasetsList:
			print d
		print ''
		dataset = raw_input('Select DataSet:')

		self.cur.execute('select sql from sqlrepo where customer like ? and wonum = ? and dataset like ?', (customer,wo, dataset))
		allentries = self.cur.fetchall()
		for x in allentries:
			string = ''.join(x)
			print string
			file = open(filename, 'wb')
			file.write(string)
		if sys.platform == 'linux2':
			subprocess.Popen('geany ' + filename, shell='False')
		else:
			subprocess.Popen('notepad++.exe ' + filename, shell='True')


	def insert(self):
		customer = raw_input('Please enter customer name:')
		print 'You entered ' + customer + '. Is this correct?'
		answer = raw_input('Enter Yes or No: ')
		if answer == 'No':
			customer = raw_input('Please enter customer name:')
		else:
			pass
		wonum = raw_input('Enter a WO Number: ')
		dataset = raw_input('Enter a DataSet value.  e.g. EX_AnswerSummary: ')
		filename = raw_input('Enter a File Name: ')
		try:
			file = open(filename,'rb')
			sql = file.read()
			self.conn.execute('insert into sqlrepo (customer, wonum, dataset, sql) values(?,?,?,?)', (customer,wonum,dataset,sql))
			self.conn.commit()
			print 'Insert successful.'
			print ''
			main()
		except Exception, e:
			print e
			main()

	def delete(self):
		self.cur.execute('select customer from sqlrepo order by customer')
		customer = raw_input('Please enter customer name: ')
		self.cur.execute('select wonum from sqlrepo where customer like ?', (customer,))
		wonums = self.cur.fetchall()
		print '\n---WO Number---'
		print seperator
		for row in wonums:
			print row[0]
		print ''
		wonum = raw_input('Please enter WO number: ')
		self.cur.execute('select dataset from sqlrepo where customer like ? and wonum = ?', (customer, wonum))
		dataset = self.cur.fetchall()
		print '\n---Data Set---'
		print seperator
		for row in dataset:
			print self.encode(row[0])
		print ''
		dataset = raw_input('Please enter the dataset: ')

		try:
			print '\nYou are about to delete the following entry: '
			print '-Customer-  -WO Number-  -Data Set-'
			print seperator
			print self.encode(customer), wonum, self.encode(dataset)
			print ''
			answer = raw_input('Are you sure you want to do so? (y or n): ')
			if answer == 'y':
				self.cur.execute('delete from sqlrepo where customer like ? and wonum = ? and dataset like ?', (customer, wonum, dataset))
				self.conn.commit()
				print '%s %s %s has been deleted!\n' % (customer, wonum, dataset)
			else:
				print 'Deletion Cancelled!'
				sys.exit()
		except Exception, e:
			print e


	def showall(self):
		self.cur.execute('select customer, wonum, dataset from sqlrepo order by customer')
		allrows = self.cur.fetchall()
		print '\nCustomer - WO Num - Data Set'
		print seperator
		for row in allrows:
			print self.encode(row[0]), row[1], self.encode(row[2])
		print ''


	def searchbywo(self):
		wonum = raw_input('Please enter WO Number:')
		wonum = '%' + wonum + '%'
		self.cur.execute('select customer, wonum, dataset from sqlrepo where wonum like ? order by customer', (wonum,))
		result = self.cur.fetchall()
		print '\nCustomer - WO Num - Data Set'
		print seperator
		for row in result:
			if len(row) > 0:
				print self.encode(row[0]), row[1], self.encode(row[2])
			else:
				print 'No Results.'
		print ''

	def searchbycust(self):
		customer = raw_input('Please enter Customer:')
		customer = '%' + customer + '%'
		self.cur.execute('select customer, wonum, dataset from sqlrepo where customer like ? order by customer', (customer,))
		result = self.cur.fetchall()
		print '\nCustomer - WO Num - Data Set'
		print seperator
		for row in result:
			if len(row) > 0:
				print self.encode(row[0]), row[1], self.encode(row[2])
			else:
				print 'No Results.'
		print ''



def main():
	print '---Main Menu---'
	print seperator
	print '1.  Retrieve SQL.'
	print '2.  Insert SQL.'
	print '3.  Search by WO Number.'
	print '4.  Search by Customer.'
	print '5.  Show all Rows.'
	print '6.  Delete Entry.'
	print '99. Exit Program.'
	option = raw_input('Select an option: ')
	if option == '1':
		c.get()
	elif option == '2':
		c.insert()
	elif option == '3':
		c.searchbywo()
		main()
	elif option == '4':
		c.searchbycust()
		main()
	elif option == '5':
		c.showall()
		main()
	elif option == '6':
		c.delete()
		main()
	elif option == '99':
		sys.exit()
	else:
		print '\nInvalid option. Please try again.\n'
		main()

if __name__ == '__main__':
	try:
		c = Connection()
		main()
	except KeyboardInterrupt:
		print 'User exited program.'
