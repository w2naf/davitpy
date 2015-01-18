# I/O module __init__.py
"""
*******************************
            IO
*******************************
This subpackage contains various I/O routines for DaViT-py
DEV: functions/modules/classes with a * have not been developed yet

This includes the following module(s):
	DataTypes
		defines the general data pointer
	radDataTypes
		defines the fundamental radar data types
	radDataRead
		contains the functions necessary for reading radar data
	pygridIo
		library for reading and writing pygrid files
	dbUtils
		general utilities for database maintenance
	dbRead
		library for reading records from the database


*******************************
"""
try:
	import fetchUtils
	from fetchUtils import *
except: print 'problem importing fetchUtils'

try:
	import DataTypes
	from DataTypes import *
except: print 'problem importing DataTypes'

try:
	import radDataTypes
	from radDataTypes import *
except: print 'problem importing radDataTypes'
	
try:
	import radDataRead
	from radDataRead import *
except: print 'problem importing radDataRead'

try:
	import sdDataTypes
	from sdDataTypes import *
except: print 'problem importing sdDataTypes'
	
try:
	import sdDataRead
	from sdDataRead import *
except Exception,e: 
	print e
	print 'problem importing sdDataRead'
	
# try:
# 	import pygridIo
# 	from pygridIo import *
# except: print 'problem importing pygridIo'

try:
	import fitexfilter
	from fitexfilter import *
except Exception,e: 
	print e
	print 'problem importing fitexfilter'
	
try:
	import dbUtils
	from dbUtils import *
except Exception,e: 
	print 'problem importing dbUtils: ', e
