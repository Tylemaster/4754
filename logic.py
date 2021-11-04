#!C:\Users\tyler\AppData\Local\Programs\Python\Python37-32\python.exe
import cgi
import mysql.connector
mydb = mysql.connector.connect(host = "localhost", user = "proj", passwd = "proj", database = "SupplyDB")
mycursor = mydb.cursor()
print("Content-type: text/html\r\n\r\n") 
print("<html><head><meta charset='utf-8'/></head><body>") 
print("<h1> Results of Query </h1>")

form = cgi.FieldStorage()

if form["kind"].value == "A":
    if "pname" not in form:
        print("Please go back and enter a part name")
    else:
        print("<table align = 'center' border><tr>")
        if "sname" in form:
            print("<th>Supplier Name</th>")
        if "sid" in form:
            print("<th>Supplier ID</th>")
        if "address" in form:
            print("<th>Supplier Address</th>")
        if "cost" in form:
            print("<th>Part Cost</th>")
        print("</tr>")
        pname = form["pname"].value
        sql = "select S.sname, S.sid, S.address, C.cost from Suppliers S, Catalog C, Parts P where S.sid = C.sid and P.pid = C.pid" \
              " and P.pname =" + "'" + pname +"'"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        for x in myresult:
            print("<tr>")
            if "sname" in form:
                print("<td>" + str(x[0]) + "</td>")
            if "sid" in form:
                print("<td>" + str(x[1]) + "</td>")
            if "address" in form:
                print("<td>" + str(x[2]) + "</td>")
            if "cost" in form:
                print("<td>" + str(x[3]) + "</td>")
            print("</tr>")
        print("</table>")
elif form["kind"].value == "B":
    if "cost" not in form:
       print("Please go back and enter a cost")
    elif not(form["cost"].value).isnumeric():
       print("Please go back and enter a cost (in numerals)")
       print(math.isnan(form["cost"].value))
    else:
       print("<table align = 'center' border><tr><th>Supplier Name</th></tr>")
       cost =form["cost"].value
       sql = "select distinct S.sname from Suppliers S, Catalog C where S.sid = C.sid and C.cost >=" + "'" + cost +"'"
       mycursor.execute(sql)
       myresult = mycursor.fetchall()
       for x in myresult:
            print("<tr><td>" + str(x[0]) + "</td></tr>")
       print("</table>")
elif form["kind"].value == "C":
    if "pid" not in form:
       print("Please go back and enter a part id")
    else:
        print("<table align = 'center' border><tr><th>Supplier Name</th><th>Supplier Address</th></tr>")
        pid =form["pid"].value
        sql = "select distinct S.sname, S.address from Suppliers S, Catalog C, Parts P where S.sid = C.sid and P.pid = C.pid and C.pid =" + "'" + pid +"'" \
              " and C.cost >= (select max(C1.cost) from Catalog C1, Parts P1 where C1.pid = P1.pid and C1.pid =" + "'" + pid +"')"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        for x in myresult:
            print("<tr><td>" + str(x[0]) + "</td><td>" + str(x[1]) + "</td></tr>")
        print("</table>")
elif form["kind"].value == "D":
    if "color" not in form or "address" not in form:
       print("Please go back and enter a part color and supplier address")
    else:
        print("<table align = 'center' border><tr><th>Part Name</th></tr>")
        color = form["color"].value
        address = form["address"].value
        sql = "select distinct P.pname from Suppliers S, Catalog C, Parts P where S.sid = C.sid and P.pid = C.pid and P.color =" + "'" + color +"'" \
              "and S.address =" + "'" + address +"'"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        for x in myresult:
            print("<tr><td>" + str(x[0]) + "</td></tr>")
        print("</table>")
elif form["kind"].value == "E":
    if "address" not in form:
       print("Please go back and enter a supplier address")
    else:
        print("<table align = 'center' border><tr><th>Supplier ID</th><th>Supplier Name</th></tr>")
        address = form["address"].value
        sql = "select distinct S.sid, S.sname from Suppliers S where S.address =" + "'" + address + "'" \
              "and S.sid not in (select C.sid from Catalog C)"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        for x in myresult:
            print("<tr><td>" + str(x[0]) + "</td><td>" + str(x[1]) + "</td></tr>")
        print("</table>")

print("</body></html>")
