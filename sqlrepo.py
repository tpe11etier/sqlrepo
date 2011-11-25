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

def encode(string):
	return string.encode('utf-8')


def get():
	c.cur.execute('select distinct customer from sqlrepo')
	customers = c.cur.fetchall()
	custList = [a[0].encode('utf-8') for a in customers]
	print '\n---Customers---'
	print seperator
	for cust in custList:
		print cust
	print ''
	customer = raw_input('Select the customer:')
	if customer not in custList:
		print '\n---Invalid Customer.---'
		get()
	c.cur.execute('select wonum from sqlrepo where customer like ?',[customer])
	wos = c.cur.fetchall()
	wosList = [a[0] for a in wos]
	print '\n---WO Numbers---'
	print seperator
	for w in wosList:
		print w
	print ''
	wo = input('Select the Work Order:')
	if wo not in wosList:
		print '\n---Invalid Work Order.---'
		get()
	c.cur.execute('select dataset from sqlrepo where customer like ? and wonum = ?', (customer,wo))
	datasets = c.cur.fetchall()
	datasetsList = [a[0].encode('utf-8') for a in datasets]
	print '\n---Data Sets---'
	print seperator
	for d in datasetsList:
		print d
	print ''
	dataset = raw_input('Select DataSet:')
	if dataset not in datasetsList:
		print '\n---Invalid Data Set.---'
		get()
	c.cur.execute('select sql from sqlrepo where customer like ? and wonum = ? and dataset like ?', (customer,wo, dataset))
	allentries = c.cur.fetchall()
	for x in allentries:
		string = ''.join(x)
		print string
		file = open(filename, 'wb')
		file.write(string)
	if sys.platform == 'linux2':
		subprocess.Popen('geany ' + filename, shell='False')
	else:
		subprocess.Popen('notepad++.exe ' + filename, shell='True')


def insert():
	customer = raw_input('Please enter customer name:')
	print 'You entered ' + customer + '. Is this correct?'
	answer = raw_input('Enter Yes or No: ')
	if answer in ['No','N']:
		insert()
	else:
		pass
	wonum = raw_input('Enter a WO Number: ')
	dataset = raw_input('Enter a DataSet value.  e.g. EX_AnswerSummary: ')
	filename = raw_input('Enter a File Name: ')
	try:
		file = open(filename,'rb')
		sql = file.read()
		c.conn.execute('insert into sqlrepo (customer, wonum, dataset, sql) values(?,?,?,?)', (customer,wonum,dataset,sql))
		c.conn.commit()
		print 'Insert successful.'
		print ''
		main()
	except Exception, e:
		print e
		main()

def delete():
	c.cur.execute('select customer from sqlrepo order by customer')
	customer = raw_input('Please enter customer name: ')
	c.cur.execute('select wonum from sqlrepo where customer like ?', (customer,))
	wonums = c.cur.fetchall()
	print '\n---WO Number---'
	print seperator
	for row in wonums:
		print row[0]
	print ''
	wonum = raw_input('Please enter WO number: ')
	c.cur.execute('select dataset from sqlrepo where customer like ? and wonum = ?', (customer, wonum))
	dataset = c.cur.fetchall()
	print '\n---Data Set---'
	print seperator
	for row in dataset:
		print encode(row[0])
	print ''
	dataset = raw_input('Please enter the dataset: ')

	try:
		print '\nYou are about to delete the following entry: '
		print '-Customer-  -WO Number-  -Data Set-'
		print seperator
		print encode(customer), wonum, encode(dataset)
		print ''
		answer = raw_input('Are you sure you want to do so? (Yes or No): ')
		if answer == 'Yes' or 'Y':
			c.cur.execute('delete from sqlrepo where customer like ? and wonum = ? and dataset like ?', (customer, wonum, dataset))
			c.conn.commit()
			print '%s %s %s has been deleted!\n' % (customer, wonum, dataset)
		else:
			print 'Deletion Cancelled!'
			sys.exit()
	except Exception, e:
		print e


def showall():
	c.cur.execute('select customer, wonum, dataset from sqlrepo order by customer')
	allrows = c.cur.fetchall()
	print '\nCustomer - WO Num - Data Set'
	print seperator
	for row in allrows:
		print encode(row[0]), row[1], encode(row[2])
	print ''


def searchbywo():
	wonum = raw_input('Please enter WO Number:')
	wonum = '%' + wonum + '%'
	c.cur.execute('select customer, wonum, dataset from sqlrepo where wonum like ? order by customer', (wonum,))
	result = c.cur.fetchall()
	print '\nCustomer - WO Num - Data Set'
	print seperator
	for row in result:
		if len(row) > 0:
			print encode(row[0]), row[1], encode(row[2])
		else:
			print 'No Results.'
	print ''

def searchbycust():
	customer = raw_input('Please enter Customer:')
	customer = '%' + customer + '%'
	c.cur.execute('select customer, wonum, dataset from sqlrepo where customer like ? order by customer', (customer,))
	result = c.cur.fetchall()
	print '\nCustomer - WO Num - Data Set'
	print seperator
	for row in result:
		if len(row) > 0:
			print encode(row[0]), row[1], encode(row[2])
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
		get()
	elif option == '2':
		insert()
	elif option == '3':
		searchbywo()
		main()
	elif option == '4':
		searchbycust()
		main()
	elif option == '5':
		showall()
		main()
	elif option == '6':
		delete()
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
