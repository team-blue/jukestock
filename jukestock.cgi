#! /usr/bin/env python3
print('Content-type: text/html\n')

import cgi, random, MySQLdb
form = cgi.FieldStorage()

string = "i211u16_jaschoi" #change username to yours!!!
password = "my+sql=i211u16_jaschoi" #change username to yours!!!
db_con = MySQLdb.connect(host="db.soic.indiana.edu", port = 3306,user=string, passwd=password, db=string)
cursor = db_con.cursor()

###when transaction occurs
# get old price
def get_oldprice(cursor, songname):
    try:
        SQL="SELECT Price FROM Song WHERE Song_Name = '"+str(songname)+"';"
        cursor.execute(SQL)
        oldprice = cursor.fetchall()[0][0]
    except:
        oldprice = "Something Wrong"
    return oldprice

#get new price
#def get_newprice(price,amount):
 #   newprice = price + amount
  #  if newprice >=0:
  #      realprice = newprice
  #  else:
  #      realprice = 0
  #  return realprice 

#add transaction
def add_transaction(cursor, songname, amount,oldprice, newprice):
    try:
        SQL="INSERT INTO Transactions(Buy_sell, Song_name,Before_price,After_price) VALUES("+str(amount)+','+'"'+str(songname)+'"'+','+str(oldprice)+','+str(newprice)+');'
        cursor.execute(SQL)
        db_con.commit()
    except:
        print("Transactions row not added!")

#change price
def change_price(cursor, songname, amount):
    try:
        SQL="UPDATE Song "
        SQL+= "SET Price="
        SQL+= str(amount)
        SQL +=" WHERE Song_Name ="
        SQL += '"'
        SQL += str(songname)
        SQL+= '";'
        cursor.execute(SQL)
        db_con.commit()
    except:
        print("song price have not been changed!")
        


    

#main
html = """<html>
<head><title>JukeStock</title></head>"""
html += """<body>
<table border='1' width='30%'> <tr><th>SongID</th><th>Song_Name</th><th>Musicians_Name</th><th>Price</th></tr> {0} </table>
<table border='1' width='50%'> <tr><th>Transaction_ID</th><th>Buy_Sell</th><th>Song_Name</th><th>Before_Price</th><th>After_Price</th><th>Date_and_Time</th></tr> {1} </table>
"""

def songlist(cursor):
	try:
		SQL = "SELECT*FROM Song;"
		cursor.execute(SQL)
		results = cursor.fetchall()
	except Exception as e:
		print('<p>Something went wrong with the SQL<p>')
		print(SQL,"\nError:",e)
	else:
		table="<p>"
		for row in results:
			table+="<tr>"
			for entry in row:
				table += "<td align='center'>" +str(entry)+"</td>"
			table+="</tr>"
		table+="</p>"
	return table


def trans_list(cursor):
	try:
		SQL = "SELECT*FROM Transactions;"
		cursor.execute(SQL)
		results = cursor.fetchall()
	except Exception as e:
		print('<p>Something went wrong with the SQL<p>')
		print(SQL,"\nError:",e)
	else:
		tables="<p>"
		for row in results:
			tables+="<tr>"
			for entry in row:
				tables += "<td align='center'>" +str(entry)+"</td>"
			tables+="</tr>"
		tables+="</p>"
	return tables
	
try:
    SQL = "SELECT Song_Name FROM Song;"
    cursor.execute(SQL)
    names = cursor.fetchall()
except Exception as e:
    print('<p>Something went wrong with the SQL!</p>')
    print(SQL,"Error:",e)
else:
	html+="""
<H1>Choose the song and amount for transaction</H1><hr />
<FORM method = "post" action = "jukestock.cgi">
<p>Song Name:
<select name="buy_song">"""
	for name in names:
		html+="<option>"+name[0]+"</option>"
	html+="</select>"
	html +="""<select name="amounts">"""
	amount_lst = [-5,-4,-3,-2,-1,1,2,3,4,5]
	for num in amount_lst:
		html+="<option>"+str(num)+"</option>"
	html+="""</select></p>
<input type="submit" value="transaction"/>
</FORM>
<hr />
</body>
</html>
"""

	songname=form.getfirst("buy_song", "So What")
	amount=form.getfirst("amounts",0)
	olddprice = float(get_oldprice(cursor, songname))
	if olddprice + amount >= 0:
		newwprice = olddprice + amount
	else:
		newwprice = 0
	add_transaction(cursor, songname, int(amount),olddprice, newwprice)
	change_price(cursor, songname, int(newwprice))


print(html.format(songlist(cursor),trans_list(cursor)))

    
    
    
            

    
