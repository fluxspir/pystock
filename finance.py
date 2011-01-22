#!/usr/bin/python3
#
# (c) : Franck Labadille
# inspired on libfinance-yahooquote.pl
#
#  Copyright (C) 1998-2002, Dj Padzensky <djpadz@padz.net>
#  Copyright (C) 2002-2010  Dirk Eddelbuettel <edd@debian.org>
#
#
import sys
import time
import gettext  #TODO
import sqlite3
#import liburl2

progname = "pyfinance"

class KnownStocks:
	"""
	Used to verify if a stock exist in our database

	Stocks are keeped in an sqlite3 database.
	---------------------
	| MetaTable			|
	|-------------------|
	| TBLK | NAME | TYPE|
	|------|------|-----|
	| 001  | Loc1 | 1	|
	| 003  | ent1 | 2	|
	| 010  | tok1 | 3	|
	| 123  | prvd1| 4	|
	---------------------

	---------------------
	|  Location PLACE 	|
	|  prev < 2K     	|
	|-------------------|
	| LOCK|Name  |TBLK	|
	|-----|------|------|
	| 001 |NYSE  | 001	|
	| 002 |Nasdaq|foreig|
	| 003 |paris | key	|
	---------------------

	-------------------------------------
	| ENTITIES (indices, warrants, obli)|
	|      prev < 50K        		   	|
	|-----------------------------------|
	| ENTK | ENTNAME | LOCK | TBLK |
	|------|---------|------|------|
	| 001  | dj30    | 001  | 010  |
	| 002  | name    |foreig|foreig|
	| 003  | not     | key  |key   |
	| 004  | null    | 
    --------------------------------------

	-------------------------------------
	|      TOKENS                        |
	|   prev < 100M                      |
	|------------------------------------|
	| TOKK|"Int Norm Code"|ENTK|LOCK|TBLK|
	|     |(yahoo code)   |    |    |	 |
	|-----|---------------|----|----|----|
	| 1   |general motor  |fore|fore|fore|
	| 2   |   goog        |key |key |key |
    --------------------------------------


    |   PROVIDER Codes  (yahoo, google, boursorama)	|
    |  prev : Stocks + indices + warrants.... 		|
    |-----------------------------------------------|
    | PVDK |Name  |TOKK|ENTK|LOCK|TBLK|
    | (req)|      |    |	|  	 |    |
    |------|------|----|----|----|----|


	usage : 
	db = database path ; 

	"""
	def __init__(self, db=os.path("~/.pyfinance.db"), metatable="Metatable", \
					loctable="SE", enttable="indices",	toktable="stocks",\
					prvdtable="yahoo", location="",\ entity="",\
					token="", prvd="" ):
		self.db = db
		self.metatable	= metatable
		self.loctable	= loctable
		self.enttable	= enttable
		self.toktable	= toktable
		self.prvdtable	= prvdtable
		self.location	= location
		self.entity		= entity
		self.token		= token
		self.prvd		= prvd

		check_db = os.path.exists(self.db)
		if not check_db:
			response = raw_input("Do you want to create new database ? y/n\n")
			if response == "y":
				##TODO mkdir self.db
				makenewDB(self.db, self.loctable, self.enttable \
							self.toktable, self.prvdtable)
			else:
				print("can't go further this way without database.\n\
				Thank you for trying %s \n" % progname )
				sys.exit(3)

		##TODO checkDB()

	def _testMakeTable(self, db, metatable, test):
		"""
		Makes sure table doesn't already exists in db
		verify = c.exec(''' "is there a table who already has this name")
		if verify ...
		cf _testAddEntry
		"""
		conn = sqlite3.connect(db)
		c = conn.cursor()
		verify = c.execute('''select %s from %s''' % (test, metatable))
		if verify:
			newentry = raw_input("'%s' already exists in %s ; \n\
						please pick another name :\n"\
						% (test, metatable) )
			_testMakeTable(db, table, newentry)
		else:
			c.close()
			return(test)

	def makeMetaTable(self, db, metatable, tabletype)
		""" 
		The MetaTable will know the names and type of every tables:
		type : 	* loctable
				* enttable
				* toktable
				* prvdtable

		TBLK : primary key
		TBLNAME : the name of the table
		TBLTYPE : 	* 1 : LocationTable
					* 2 : EntityTable
					* 3 : TokenTable
					* 4 : PrvdTable
		"""
		#TODO test tabletype
		conn = sqlite3.connect(db)
		c = conn.cursor()
		c.execute('''create table %s ( \
				TBLK integer primary key asc, \
				TBLNAME text not null \
				TBLTYPE integer not null)''' \
				% metatable, tabletype)
		conn.commit()
		c.close

	def _addMetaTable(self, db, metatable, tablename, tabletype):
		"""
		add infos in the MetaTable about the new table created
		"""
		conn = sqlite3.connect(db)
		c = conn.cursor()
		c.execute(""" insert into %s values (\
				'%s', '%s')""" \
				% (metatable, tablename, tabletype))
		conn.commit()
		c.close()

	def makeLocation(self, db, metatable, loctable):
		_addMetaTable(db, metatable, loctable, 1)
		loctable = _testMakeTable(db, metatable, loctable)
		conn = sqlite3.connect(db)
		c = conn.cursor()
		c.execute('''create table %s ( \
					LOCK integer primary key asc, \
					LOCNAME text not null, \
					TBLK integer,
					foreign key(TBLK) references %s(TBLK))''' \
					% (loctable, metatable))
		conn.commit()
		c.close()

	def makeEntity(self, db, metatable, loctable, enttable):
		_addMetaTable(db, metatable, enntable, 2)
		enttable = _testMakeTable(db, metatable, enttable)
		conn = sqlite3.connect(db)
		c = conn.cursor()
		c.execute('''create table %s( \
					ENTK integer primary key asc, \
					ENTNAME text not null, \
					LOCK integer, \
					TBLK integer, \
					foreign key(LOCK) references %s(LOCK))
					foreign key(TBLK) references %s(TBLK))''' \
					% (enttable, loctable, metatable))
		conn.commit()
		c.close()

	def makeTokens(self, db, metatable, loctable, enttable, toktable):
		_addMetaTable(db, metatable, toktable, 3)
		toktable = _testMakeTable(db, metatable, toktable)
		conn = sqlite3.connect(db)
		c = conn.cursor()
		c.execute('''create table %s ( \
					TOKK integer primary key asc, \
					TOKNAME text not null, \
					ENTK integer, \
					LOCK integer, \
					TBLK integer, \
					foreign key(ENTK) references %s(ENTK) \
					foreign key(LOCK) references %s(LOCK))
					foreign key(TLBK) references %s(TBLK)''' \
					% (toktable, enttable, loctable, metatable))
		conn.commit()
		c.close()
		
	def makePrvd(self, db, metatable, loctable, enttable, toktable, prvdtable):
		_addMetaTable(db, metatable, prvdtable, 4)
		prvdtable = _testMakeTable(db, metatable, prvdtable)
		conn = sqlite3.connect(db)
		c = conn.cursor()
		c.execute('''create table %s ( \
					PVDK integer primary key asc, \
					PVDCode text not null, \
					TOKK integer, \
					ENTK integer, \
					LOCK integer, \
					TBLK integer, \
					foreign key(TOKK) references %s(TOKK) \
					foreign key(ENTK) references %s(ENTK), \
					foreign key(LOCK) references %s(LOCK))
					foreign key(TBLK) references %s(TBLK))''' \
					% (prvdtable, toktable, enttable, loctable, metatable))
		conn.commit()
		c.close()

	def makenewDB(self, db, metatable, loctable, enttable, toktable, prvdtable):
		"""
		Creation of sqlite3 tables :
			* Stock Exchange
			* entity
			* tokens 
			* provider
		"""
		makeMetaTable(db, metatable)
		makeLocation(db, metatable, loctable)
		makeEntity(db, metatable, loctable, enttable)
		makeToken(db, metatable, loctable, enttable, toktable)
		makePrvd(db, metatable, loctable, enttable, toktable, prvdtable)

	def checkDB(self):
		pass
	

	def _selectTable(self, db, qw):
		"""
		qw : database query wraped in tuple, secure.
		qw = (pattern, table, [colname], [colpattern], )
		 return(primarykey, pattern)
		"""
		pattern = qw[0]
		table = qw[1]
		conn = sqlite3.connect(db)
		c = conn.cursor()
		if len(qw) == 2:
			tableinfo = c.execute("""select %s into %s""", \
								% (pattern, table))
		elif len(qw) == 4:
			colname = qw[2]
			colpattern = qw[3]   ## TODO (qw[4], ) ; cf below
			##TODO HOW TO CHANGE last %s(colpattern) in sqlitesynthaxe :"?" ???
			tableinfo = c.execute(""" select %s into %s where %s = %s""" \
								% (pattern, table, colname, colpattern)
		c.close 								# No commit, nothing changed
		return(tableinfo)

	def _getTableKey(self, db, pattern, table, colname, colpattern):
		"""
		Only used internally, when a table is created
		"""
		if colname:
			qw = ( pattern, table, colname, colpattern)
			tableinfo = selectTable(db, qw)
		else:
			qw = (pattern, table)
			tableinfo = selectTable(db, qw)
			##TODO if crash, try-except and link to makeMetaTable
		return(tableinfo)

	def _testInput(self, db, table, name="")
		"""
		At first, only determines if "name" is given ; if not, ask for one.
		Then, if "name" is already in database, ask for "name" again,
		for the new entry.
		"""
		qw = (table, name)
		if not name:
			newentry = raw_import("Please enter a new name for %s" % table)
			_testInput(db, table, newentry)

		verify = _selectTable(db, qw)
		if verify:
			_testInput(db, table, "")
		return(name)

	def _pickPriKey(self, db, colprikey, colname, table, colwhere, colpat):
		"""
		Prints every Names already knows for this query
		 SELECT (columns(prikey AND name)) FROM table
		 WHERE colwhere = colpattern

		  gives :([(prikey0, name0),(prikey1, name1),...])

		then print(name* + number)
		user pick a number in list (the primarykey && name) is return
		or user choose a newname, so and a new entry is created
		"""
		conn = sqlite3.connect(db)
		c = conn.cursor()
		prikeyname = c.execute("""select (%s and %s) from %s \
								where %s='%s' """\
							% (colprik, colname, table, colname, colpat))
		c.close
		prikeydict = {}
		i = 1
		for row in prikeyname:
			prikeydict = {i: prikeyname}
			print("%d\t %s\n" % i, prikeydict[i][1]
			i++
		userpick = raw_import("select one choice, or add a new one")
		if str(userpick).isdigit and if prikeydict[userpick]:
			(prikey, name) = (prikeydict[userpick][0], prikeydict[userpick][1]
			return(prikey, name)
		else:
			return(userpick)
			
		
	def addLocation(self, db, tblt, loct, location):
		""" add str(location) into the lockt(table of locations)"""
		tblt = _getTableKey(db, loct, tblt, "TBLTYPE", "1")
		#tableinfo = _getTableKey(db, loctable, metatable, "TBLTYPE", "1")
		location = _testInput(db, loct, location)
		conn = sqlite3.connect(db)
		c = conn.cursor()
		c.execute("""insert into ? values (?, ?)"""
				% (loct, location, tblt[0]))
		conn.commit()
		c.close()

	def addEntity(self, db, tblt, loct, entt, entity):
		""" """
		tblt = _getTableKey(db, entt, tblt, "TBLTYPE", "2")
		entity = _testInput(db, enttable, entity)
		if not location:
			lockeyname = _pickPriKey(db, "LOCK", "LOCNAME", loctable, )
			if not prikeyname:
				addEntity(db, metatable, enttable, prikeyname, entity)
			else:
				lockey = prikeyname[0]
		else:
			lockeyname = _pickPriKey(db, 
			= _testInput(db, loctable, location)
		entity = _testAddEntry(db, enttable, location, entity)
		conn = sqlite3.connect(db)
		c = conn.cursor()
		c.execute("""insert into %s values (\
				'%s', '%s', '%s')""" \
				% (enttable, entity, lock[0], TBL[0]))
		conn.commit()
		c.close()

	def addToken(self, db, toktable, location, entity, token):
		""" """
		tableinfo = getTableKey(db, metatable, toktable)
		token = _testAddEntry(db, toktable, token)
		conn = sqlite3.connect(db)
		c = conn.cursor()
		c.execute("""insert into %s values (\
				'%s', '%s', '%s')"""\
				% (toktable, token, entity, location)
		conn.commit()
		c.close()

	def addPrvd(self, db, prvdtable, location, entity, token, prvd):
		prvd = _testAddEntry(db, prvdtable, prvd)
		conn = sqlite3.connect(db)
		c = conn.cursor()
		c.execute("""insert into %s values (\
				'%s', '%s', '%s', '%s')"""\
				% (prvdtable, prvd, token, entity, location)
		conn.commit()
		c.close()

				
	def addSymbol(self, db, loctable="", enttable="", toktable=""\
				prvdtable="", location="", entity="", token="", prvd=""):
		"""
		insert into chosen table elements required and optionnal

		addSymbol(db, [loctable], [enttable], [toktable], [prvdtable] \
				[location], [entity], [token], [prvd])

		both  "table" and "table_entry"	     ( loctable AND location,
										AND/OR enttable AND entity,
										AND/OR toktable AND token,
										AND/OR prvdtable AND prvd   )
				ARE REQUIRED IN ORDER addSymbol() to do something.
		"""
		conn = sqlite3.connect(db)
		c = conn.cursor()

		if not location:
			if not loctable:
				knownloctable = c.execute('''select''' #TODO ###########
				loctable = raw_import("Please select a location_table\n\
						or create a new one by naming it")
				MakeLocation(db, 
#			location = raw_import("select location or add a new one\n
			%s

		elif toktable

	


class Elements:
    """
    unify the Element query:
    based on Finance::Yahoo  (libfinance-yahooquote-perl)
    introduce in url by : "&f="
        'Symbol'                                        's'
        'Name'                                          'n'
        'Last Trade (With Time)'                        'l'
        'Last Trade (Price Only)'                       'l1'
        'Last Trade Date'                               'd1'
        'Last Trade Time'                               't1'
        'Last Trade Size'                               'k3'
		...

    """
    def __init__(self, elements):
        self.elements = "".join(elements)
        return("&f=%s" % self.elements)

class Symbols:
    """
    check if they are different from yahoo, google...
    make a unified table of symbols if needed
    introduce in url by : "&s="
    symbols are type : goog ; bnp.pa ...
    """
    def __init__(self, symbols):
        self.symbols =  "".join(symbols)
        return("&s=%s" % self.symbols)


class Provider:
    """
    Choose the quote_server/provider
    
    Default and fall_back on yahoo-finance (historical reason)
    Choices between :
        "yahoo"
        "google"
    You may add an other provider to use into the provider_tup if you give 
    information in select_provider in order the query to update.
	give the access to (prvdk-pvdrname) : displays "pvrdname" ;
	use prvdk for db queries.
    """

	class Yahoo:
    	""" 
	    Deals with yahoo db.
	    """
	    def __init__(self):
    	    self.baseurl = ""
       	 self.token = token      #token might be of : cf Elements.__doc__
       	 self.symbols = Symbols()

  		def getSymbol(self):
        	""" accept a tuple (or a list) of stock Symbols to get """
        	return(self.symbols)

	class Boursorama:
		""" """
		pass
	class Google:
		""" """
		pass

class ShrTasks:
    """
	The Share Tasks class : manage the query to get most valuables informations

    Some providers gives delayed informations.
    Others may distribute fewer or differents informations.
    We, hereby, are trying to share tasks between servers
    to fit the most accurate :
        time data
        information required
    e.g. :
        provider A gives RT infos, but doesn't gives feature X.
        provider B gives delayed infos, but also tells Y features.
        Despite the greater network load, we'll get information from
        both providers, so users will given best datas.
    User may choose to use ONLY provider "A"
    and may be able to tell the desired provider to use IF POSSIBLE.

	chosenprvd : provider to use ; default to defprvd
	behavior : 	"0" → let the lib do what it wants to get you informations
				"1" → the user wants chosenprovider to be use, but will 
			agree for the lib to fetch informations he required and that 
			are not on the chosenprovider to be fetch from external sources
				"2" → get information from this and only provider.
	"""
    def __init__(self, chosenprvd, behavior="0"):
		knownproviders = ("yahoo", "google", "boursorama",)
		acceptedbehavior = ("0", "1", "2")

		if chosenprvd not in knownproviders:
            chosenprvd = defprvd
        self.prvd = chosenprvd
		if behavior not in acceptedbehavior
			self.behavior = behavior
	
	def _RT(self, defrt=1):
		"""
		Does user wants "above all" the real time information ?
		Default :	1 (yes, please, if possible, give me real time !)
					0 (no. real time isn't the main issue
		"""
		if defrt:
			self.RT = defrt

	def _create_urls(self):
		""" """

class Market:
	"""
	Market you want to work with :
		* StockExchange
		* Currencies
		* RealEstate
	"""
	def __init__(self, market):
		if SE not in knownSE:
			self.add_SE(SE)
		self.SE = SE

class StockExchange(Market):
	"""
	AMSTERDAM, NYSE, NASDAQ, PARIS,
	"""
	def location(self)
		return(location)
	def add(self):

	class Symbol:
		""" """
		def code(self):
			""" "USxxxxxxxx", "FRxxxxxxx", """
		def element(self):
			"""name, value, last trade, higher..."""
		def add(self):
			""" Call database"""
			def code(self):
				pass
			def element(self):
	pass
class Stock(StockExchange):
	""" inherit international_normalized_code, element,
	"""
	def element(self):
		pass
class Index(Stock):
	"""DJ30, NASDAQ100, CAC40,
	index → name ; stocks_included
	"""
	def newindex(self):
		pass

class Obligation(StockExchange):
	"""Debt1, Debt2"""
	pass
class Futures(StockExchange):
	pass
class Warrants(StockExchange):
	pass
	
class Currency(Market):
	pass
class RealEstate(Market):
	pass
		

if __name__ == "__main__" :
    try:
        print("ok")
        time.sleep(2)
        sys.exit(0)


    except KeyboardInterrupt:
        print("keyboard interrupt")
        sys.exit(1)
