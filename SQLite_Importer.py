#  Runs on Python 2.7
#  Please make sure Members.csv and Stores.csv are located in the same directory

from Tkinter import *   
from tkFileDialog import askdirectory       
import csv, sqlite3


# Used for clearing the data displayed on th UI
def ClearTable():
	for i in tablelist:	
		i.destroy()
	col_num = 0
	for i in xrange(0,25,2):
		labels_and_text[i].config(text=labels_and_text[i + 1], height=0, width=0, padx = 10, font="-weight bold")
		labels_and_text[i].grid(row = 1, column = col_num, sticky = W)
		col_num = col_num + 1
	
# Prompts user for the directory containing the 'Members.csv' and 'Stores.csv' files.  
# Then imports the data from the files into a SQLite database with two tables members and stores
def ImportData():
	#  Checks if Members.csv is present in directory
	info_label.config(text='Import data of the .CSV files into a SQLLite database', height=0, width=0, padx = 10)
	info_label.grid(row = 0, column=7, sticky=W, pady = 5, padx = 5  )
	try:
		directory = askdirectory()
		no_first = 0
		csvfile = open(directory + '/Members.csv', 'rb')
		creader = csv.reader(csvfile, delimiter=',', quotechar='"')
	except:
		print directory + '/Members.csv could not be found'
	else:
		#  Checks if Stores.csv is present in directory
		try:
			csvfile2 = open(directory + '/Stores.csv', 'rb')
			creader2 = csv.reader(csvfile2, delimiter=',', quotechar='"')
		except:
			print directory + '/Stores.csv could not be found'
		else:
			db = sqlite3.connect('chynna.sqlite')
			cursor = db.cursor()
			#  Clears tables if they exist
			cursor.execute('DELETE FROM members')
			cursor.execute('DELETE FROM stores')
			ClearTable()
			for i in creader:
				#  Skips first row from file
				if no_first != 0:
					cursor.execute('INSERT INTO  members ( MemberNumber, LastName, FirstName, StreetAddress, City, State, ZipCode, Phone, FavoriteStore, DateJoined, DuesPaid) VALUES (?,?,?,?,?,?,?,?,?,?,?);', i )
				no_first = 1
			db.commit()
			csvfile.close()
			no_first = 0
			for i in creader2:
				#  Skips first row from file
				if no_first != 0:
					cursor.execute('INSERT INTO  stores ( StoreID, StoreName, Location) VALUES (?,?,?);', i )
				no_first = 1
			db.commit()
			cursor.execute('SELECT * FROM members INNER JOIN stores ON members.FavoriteStore = stores.StoreID;') 
			rows = cursor.fetchall()
			row_num = 2	
			col_num = 0
			#  Displays data on table, adds it to tablelist, and prints out data as well
			print 'Member Number | Last Name | First Name | Street Address | City | State | Zip Code | Phone | Date Joined | Dues Paid | Favorite Store ID | Favorite Store Name| Store Location'
			print ''
			for i in rows:
				for j in range (0,13):
					if j != 8:
						labelwhy = Label(root, text=i[col_num], height=0, width=0, padx = 10)
						labelwhy.grid(row = row_num, column=j, sticky=W)
						tablelist.append(labelwhy)	
						col_num = col_num + 1
					else:
						labelwhy = Label(root, text=i[col_num + 1], height=0, width=0, padx = 10)
						labelwhy.grid(row = row_num, column=j, sticky=W)
						tablelist.append(labelwhy)	
						col_num = j + 2
				col_num = 0
				row_num = row_num + 1		
				print '%s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |%s' % (i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7], i[9], i[10],i[11], i[12], i[13])	
				print ''				
			csvfile2.close()
			db.close()	

#  Orders the data by Last Name and then First Name and displays all data from both tables relevant to them
def Alphabetize():
	info_label.config(text='Lists alphabetized member names with all available data', height=0, width=0, padx = 10)
	info_label.grid(row = 0, column=7, sticky=W, pady = 5, padx = 5  )
	ClearTable()
	first_label.config(text='Last Name', height=0, width=0, padx = 10, font="-weight bold")
	first_label.grid(row = 1, column=0, sticky=W)
	second_label.config(text='First Name', height=0, width=0, padx = 10, font="-weight bold")
	second_label.grid(row = 1, column=1, sticky=W)
	third_label.config(text='Member Number', height=0, width=0, padx = 10, font="-weight bold")
	third_label.grid(row = 1, column=2, sticky=W)
	db = sqlite3.connect('chynna.sqlite')
	cursor = db.cursor()
	#  Connects the two tables by Favorite Store ID
	cursor.execute('SELECT * FROM members INNER JOIN stores ON members.FavoriteStore = stores.StoreID ORDER BY LastName, FirstName;')      
	rows = cursor.fetchall()
	row_num = 2
	#  Prints out data as well
	print 'Last Name | First Name | Member Number | Street Address | City | State | Zip Code | Phone  | Date Joined | Dues Paid | Favorite Store ID | Favorite Store Name | Store Location'
	print ''
	#  Displays data on table, adds it to tablelist
	for i in rows:
		labelwhy = Label(root, text=i[1], height=0, width=0, padx = 10)
		labelwhy.grid(row = row_num, column=0, sticky=W)
		tablelist.append(labelwhy)	
		labelwhy = Label(root, text=i[2], height=0, width=0, padx = 10)
		labelwhy.grid(row = row_num, column=1, sticky=W)
		tablelist.append(labelwhy)
		labelwhy = Label(root, text=i[0], height=0, width=0, padx = 10)
		labelwhy.grid(row = row_num, column=2, sticky=W)
		tablelist.append(labelwhy)	
		for j in range (3,8):
			labelwhy = Label(root, text=i[j], height=0, width=0, padx = 10)
			labelwhy.grid(row = row_num, column=j, sticky=W)
			tablelist.append(labelwhy)	
		for k in range (8,13):
			labelwhy = Label(root, text=i[k + 1], height=0, width=0, padx = 10)
			labelwhy.grid(row = row_num, column=k, sticky=W)
			tablelist.append(labelwhy)			
		row_num = row_num + 1
		#  Prints data out
		print '%s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |%s' % (i[1],i[2],i[0],i[3],i[4],i[5],i[6],i[7], i[9], i[10],i[11], i[12], i[13])
		print''
	db.close()

#  Queries for the numbers of members whose ZipCode matches 22101 and whose DuesPaid matches XXXX-01-XX
def January():
	info_label.config(text='Lists all members with zip code 22101 who have paid dues during January', height=0, width=0, padx = 10)
	info_label.grid(row = 0, column=7, sticky=W, pady = 5, padx = 5  )
	ClearTable()
	db = sqlite3.connect('chynna.sqlite')
	cursor = db.cursor()
	cursor.execute('SELECT * FROM members INNER JOIN stores ON members.FavoriteStore = stores.StoreID WHERE ZipCode=? AND DuesPaid LIKE ?;', ('22101','_____01%'))  
	rows = cursor.fetchall()
	row_num = 2
	col_num = 0
	#  Prints out data as well
	print 'Member Number | Last Name | First Name | Street Address | City | State | Zip Code | Phone | Date Joined | Dues Paid | Favorite Store ID | Favorite Store Name| Store Location'
	print ''
	#  Displays data on table, adds it to tablelist
	for i in rows:
		for j in range (0,13):
			if j != 8:
				labelwhy = Label(root, text=i[col_num], height=0, width=0, padx = 10)
				labelwhy.grid(row = row_num, column=j, sticky=W)
				tablelist.append(labelwhy)	
				col_num = col_num + 1
			else:
				labelwhy = Label(root, text=i[col_num + 1], height=0, width=0, padx = 10)
				labelwhy.grid(row = row_num, column=j, sticky=W)
				tablelist.append(labelwhy)	
				col_num = j + 2
		col_num = 0
		row_num = row_num + 1	
		print '%s' % (i[0])
		print ''
	db.close()
	
#  Queries for the numbers of members whose State is VA and whose DateJoined is either past the year 2000, or past 1999-08, or past 1999-07-01
def JoinedSince():
	info_label.config(text='Lists all members who have joined since 1999-07-01 and live in VA', height=0, width=0, padx = 10)
	info_label.grid(row = 0, column=7, sticky=W, pady = 5, padx = 5  )
	ClearTable()
	db = sqlite3.connect('chynna.sqlite')
	cursor = db.cursor()
	cursor.execute('SELECT * FROM members INNER JOIN stores ON members.FavoriteStore = stores.StoreID WHERE State=? AND (DateJoined LIKE ? OR DateJoined LIKE ? OR (DateJoined Like ? AND DateJoined != ?));', ('VA','2%', '1999-08%', '1999-07%', '1999-07-01'))   
	rows = cursor.fetchall()
	#  Creates Window with Headers to display data
	row_num = 2
	col_num = 0
	#  Prints out data as well
	print 'Member Number'
	print ''
	#  Displays data on table, adds it to tablelist
	for i in rows:
		for j in range (0,13):
			if j != 8:
				labelwhy = Label(root, text=i[col_num], height=0, width=0, padx = 10)
				labelwhy.grid(row = row_num, column=j, sticky=W)
				tablelist.append(labelwhy)	
				col_num = col_num + 1
			else:
				labelwhy = Label(root, text=i[col_num + 1], height=0, width=0, padx = 10)
				labelwhy.grid(row = row_num, column=j, sticky=W)
				tablelist.append(labelwhy)	
				col_num = j + 2
		col_num = 0
		row_num = row_num + 1	
		print '%s' % (i[0])
		print ''	
	db.close()

#  Uses a JOIN to query for the names of members and to get the names and locations of their favorite stores based on the StoreID
def FaveStore():
	info_label.config(text='Lists the names of all members and the names of their favorite store and its location', height=0, width=0, padx = 10)
	info_label.grid(row = 0, column=7, sticky=W, pady = 5, padx = 5  )
	ClearTable()
	first_label.config(text='Last Name', height=0, width=0, padx = 10, font="-weight bold")
	first_label.grid(row = 1, column=0, sticky=W)
	second_label.config(text='First Name', height=0, width=0, padx = 10, font="-weight bold")
	second_label.grid(row = 1, column=1, sticky=W)
	third_label.config(text='Favorite Store', height=0, width=0, padx = 10, font="-weight bold")
	third_label.grid(row = 1, column=2, sticky=W)
	fourth_label.config(text='Store Location', height=0, width=0, padx = 10, font="-weight bold")
	fourth_label.grid(row = 1, column=3, sticky=W)
	fifth_label.config(text='Member Number', height=0, width=0, padx = 10, font="-weight bold")
	fifth_label.grid(row = 1, column=4, sticky=W)
	twelfth_label.config(text='Street Address', height=0, width=0, padx = 10, font="-weight bold")
	twelfth_label.grid(row = 1, column=11, sticky=W)
	thirteenth_label.config(text='City', height=0, width=0, padx = 10, font="-weight bold")
	thirteenth_label.grid(row = 1, column=12, sticky=W)
	db = sqlite3.connect('chynna.sqlite')
	cursor = db.cursor()
	cursor.execute("SELECT members.LastName,members.FirstName,stores.StoreName, stores.Location FROM members INNER JOIN stores ON members.FavoriteStore = stores.StoreID;")	
	rows = cursor.fetchall()
	row_num = 2
	#  Prints out data as well
	print 'Last Name |  First Name | Favorite Store | Store Location'
	print ''
	#  Displays data on table, adds it to tablelist
	for i in rows:
		for j in range (0,4):
			labelwhy = Label(root, text=i[j], height=0, width=0, padx = 10)
			labelwhy.grid(row = row_num, column=j, sticky=W)
			tablelist.append(labelwhy)	
		#  Prints data out
		print '%s | %s | %s | %s' % (i[0],i[1],i[2],i[3])
		row_num = row_num + 1
		print ''	
	db.close()

#  Queries stores to get the Store ID of 'Total Wine' inside of a query of members to get the names of members whose favorite store is 'Total Wine'
def WineFave():
	info_label.config(text='Lists the names of  all members whose favorite store is Total Wine', height=0, width=0, padx = 10)
	info_label.grid(row = 0, column=7, sticky=W, pady = 5, padx = 5  )
	ClearTable()
	first_label.config(text='Last Name', height=0, width=0, padx = 10, font="-weight bold")
	first_label.grid(row = 1, column=0, sticky=W)
	second_label.config(text='First Name', height=0, width=0, padx = 10, font="-weight bold")
	second_label.grid(row = 1, column=1, sticky=W)
	third_label.config(text='Member Number', height=0, width=0, padx = 10, font="-weight bold")
	third_label.grid(row = 1, column=2, sticky=W)
	db = sqlite3.connect('chynna.sqlite')
	cursor = db.cursor()
	fave_store = 'Total Wine'
	cursor.execute('SELECT members.LastName,members.FirstName FROM members WHERE members.FavoriteStore=(SELECT stores.StoreID FROM stores WHERE stores.StoreName=? LIMIT 1);', (fave_store,))
	rows = cursor.fetchall()
	row_num = 2
	#  Prints out data as well
	print 'Last Name, First Name'
	print ''
	#  Displays data on table, adds it to tablelist
	for i in rows:
		#  Prints data out
		print '%s | %s' % (i[0],i[1])
		labelwhy = Label(root, text=i[0], height=0, width=0, padx = 10)
		labelwhy.grid(row = row_num, column=0, sticky=W)
		tablelist.append(labelwhy)	
		labelwhy = Label(root, text=i[1], height=0, width=0, padx = 10)
		labelwhy.grid(row = row_num, column=1, sticky=W)
		tablelist.append(labelwhy)	
		row_num = row_num + 1
		print ''
	db.close()
	
#  Shows all data in original format
def ShowData():
	info_label.config(text='All data organized by Member Number', height=0, width=0, padx = 10)
	info_label.grid(row = 0, column=7, sticky=W, pady = 5, padx = 5  )
	ClearTable()
	db = sqlite3.connect('chynna.sqlite')
	cursor = db.cursor()
	cursor.execute('SELECT * FROM members INNER JOIN stores ON members.FavoriteStore = stores.StoreID;') 
	rows = cursor.fetchall()
	row_num = 2	
	col_num = 0
	#  Displays data on table, adds it to tablelist, and prints out data as well
	print 'Member Number | Last Name | First Name | Street Address | City | State | Zip Code | Phone | Date Joined | Dues Paid | Favorite Store ID | Favorite Store Name| Store Location'
	print ''
	for i in rows:
		for j in range (0,13):
			if j != 8:
				labelwhy = Label(root, text=i[col_num], height=0, width=0, padx = 10)
				labelwhy.grid(row = row_num, column=j, sticky=W)
				tablelist.append(labelwhy)	
				col_num = col_num + 1
			else:
				labelwhy = Label(root, text=i[col_num + 1], height=0, width=0, padx = 10)
				labelwhy.grid(row = row_num, column=j, sticky=W)
				tablelist.append(labelwhy)	
				col_num = j + 2
		col_num = 0
		row_num = row_num + 1		
		print '%s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |%s' % (i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7], i[9], i[10],i[11], i[12], i[13])	
		print ''
	db.close()
	

#  Creates 'chynna.sqlite' database and creates members and stores tables within it if they aren't already present
db = sqlite3.connect('chynna.sqlite')
cursor = db.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS members ( MemberNumber TEXT, LastName TEXT, FirstName TEXT, StreetAddress TEXT, City TEXT, State TEXT, ZipCode TEXT, Phone TEXT, FavoriteStore TEXT, DateJoined TEXT, DuesPaid TEXT)')
cursor.execute('CREATE TABLE IF NOT EXISTS stores ( StoreID TEXT, StoreName TEXT, Location)')
db.commit()
db.close()
	
#  Window for Main Menu	
root = Tk() 
root.wm_title('SQLite Importer')                    

buttonframe = Frame(root)
buttonframe.grid(row=0, column=0, columnspan=8, sticky = W)   

#  Buttons to execute the required tasks
import_button = Button(buttonframe, text='Import Data', command=ImportData)
import_button.grid(row = 0, sticky = W, column=0, pady = 5, padx = 5 )

alpha_button = Button(buttonframe, text = 'Alphabetize', command = Alphabetize)
alpha_button.grid(row = 0, column = 1, sticky = W, pady = 5, padx = 5  )

january_button = Button(buttonframe, text = '22101, Dues January', command = January)
january_button.grid(row = 0, column = 2, sticky = W, pady = 5, padx = 5  )

since_button = Button(buttonframe, text = 'VA, Since 07/01/1999', command = JoinedSince)
since_button.grid(row = 0, column = 3, sticky = W, pady = 5, padx = 5  )

fave_button = Button(buttonframe, text = 'Favorite Store', command = FaveStore)
fave_button.grid(row = 0, column = 4, sticky = W, pady = 5, padx = 5  )

wine_button = Button(buttonframe, text = 'Total Wine', command = WineFave)
wine_button.grid(row = 0, column = 5, sticky = W, pady = 5, padx = 5  )

show_button = Button(buttonframe, text = 'Show All Data', command = ShowData)
show_button.grid(row = 0, column = 6, sticky = W, pady = 5, padx = 5  )

#  Shows information about each buttons function
info_label = Label(buttonframe, text='This will tell you what each button did', height=0, width=0, padx = 10)
info_label.grid(row = 0, column=7, sticky=W, pady = 5, padx = 5  )

first_label = Label(root, text='Member Number', height=0, width=0, padx = 10, font="-weight bold")
first_label.grid(row = 1, column=0, sticky=W)
second_label = Label(root, text='Last Name', height=0, width=0, padx = 10, font="-weight bold")
second_label.grid(row = 1, column=1, sticky=W)
third_label = Label(root, text='First Name', height=0, width=0, padx = 10, font="-weight bold")
third_label.grid(row = 1, column=2, sticky=W)
fourth_label = Label(root, text='Street Address', height=0, width=0, padx = 10, font="-weight bold")
fourth_label.grid(row = 1, column=3, sticky=W)
fifth_label = Label(root, text='City', height=0, width=0, padx = 10, font="-weight bold")
fifth_label.grid(row = 1, column=4, sticky=W)
sixth_label = Label(root, text='State', height=0, width=0, padx = 10, font="-weight bold")
sixth_label.grid(row = 1, column=5, sticky=W)
seventh_label = Label(root, text='Zip Code', height=0, width=0, padx = 10, font="-weight bold")
seventh_label.grid(row = 1, column=6, sticky=W)
eigth_label = Label(root, text='Phone', height=0, width=0, padx = 10, font="-weight bold")
eigth_label.grid(row = 1, column=7, sticky=W)
ninth_label = Label(root, text='Date Joined', height=0, width=0, padx = 10, font="-weight bold")
ninth_label.grid(row = 1, column=8, sticky=W)
tenth_label = Label(root, text='Dues Paid', height=0, width=0, padx = 10, font="-weight bold")
tenth_label.grid(row = 1, column=9, sticky=W)
eleventh_label = Label(root, text='Favorite Store ID', height=0, width=0, padx = 10, font="-weight bold")
eleventh_label.grid(row = 1, column=10, sticky=W)
twelfth_label = Label(root, text='Favorite Store Name', height=0, width=0, padx = 10, font="-weight bold")
twelfth_label.grid(row = 1, column=11, sticky=W)
thirteenth_label = Label(root, text='Store Location', height=0, width=0, padx = 10, font="-weight bold")
thirteenth_label.grid(row = 1, column=12, sticky=W)

#List containing the labels that display the sqlite data on the UI
tablelist = []

#  List containing the default text for each label position
labels_and_text = [first_label, 'Member Number', second_label , 'Last Name', third_label , 'First Name', fourth_label , 'Street Address', fifth_label , 'City', sixth_label , 'State', seventh_label , 'Zip_Code', 
eigth_label, 'Phone', ninth_label , 'Date Joined', tenth_label , 'Dues Paid', eleventh_label , 'Favorite Store ID', twelfth_label , 'Favorite Store Name', thirteenth_label , 'Favorite Store Location']

root.mainloop()                 