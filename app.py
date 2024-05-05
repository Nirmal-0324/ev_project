from flask import Flask, render_template, request, jsonify,redirect
from math import radians, sin, cos, sqrt, atan2
import requests
import mysql.connector
import pymysql
import hashlib


app = Flask(__name__)

# st_db
db_config = {
    'host':  'localhost',
    'user': ' root',
    'database': 'evcs'
}
# user_db
db_config_user = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'user_db'
}


sample_data = [
    {'name': 'Item 1', 'value': 10},
    {'name': 'Item 2', 'value': 20},
    {'name': 'Item 3', 'value': 30},
]




def insert_port_data(owner_name, contact, location, sub_stations, port_types, costs):
    connection = None
    cursor = None  

    try:
      
        connection = mysql.connector.connect(**db_config)

        cursor = connection.cursor()
        cursor.execute("select st_id from ev_data")
        ids = cursor.fetchall()
        id = ((ids[-1][0]) + 1)
        
        print(1)
        for sub_st, port_type, cost in zip(sub_stations, port_types, costs):
            print(2)
            sql_query = "INSERT INTO ev_data (st_id, st_name,contact, location,sub_st, port_type, cost) VALUES (%s, %s, %s,%s, %s, %s, %s)"
            print(3)
            
            lat,lng=map(str,location.split((',')))
            loc=lat[7:]+','+lng[6:-1]
           
            data = (id, owner_name, contact,loc, sub_st, port_type, cost)
         
            cursor.execute(sql_query, data)

        connection.commit()

        print("Data inserted successfully!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@app.route('/')
def loginpage():
    return render_template('index.html')

@app.route('/st_owner', methods=['GET', 'POST'])
def ev_form():
    if request.method == 'POST':
        owner_name = request.form['ownerName']
        contact = request.form['contact']
        location = request.form['location']
        sub_stations = request.form.getlist('stations[]')
        port_types = request.form.getlist('portType[]')
        costs = request.form.getlist('cost[]')


        insert_port_data(owner_name,contact,location, sub_stations, port_types, costs)

    return render_template('st_owner.html')


@app.route('/test', methods=['GET','POST'])
def empty_location():
    print(1)
    information = request.form.get('information')
    print(2)
    if information != None :
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        query= "select * from ev_data"
        cursor.execute(query)
        u_data=cursor.fetchall()
        #print(data)
        
        def haversine(lat1, lon1, lat2, lon2):
            lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            R = 6371.0
            distance = R * c
            return distance
        def ordering(a):
            #k=[1,2,3,[st_id,[],[],[]],[st_id[],[],[]]]
            b=[]
            for i in a:
                for j in b:
                    if i[3] in j:
                        for k in j[3:]:
                            if k[0]==i[4]:
                                k[1].append(i[5])
                                k[2].append(i[6])
                                k[3].append(i[7])
                                break
                        else:
                            n_st=[i[4],[i[5]],[i[6]],[i[7]]]
                            j.append(n_st)
                        break
                else:
                    b.append([i[2],i[3],i[8],[i[4],[i[5]],[i[6]],[i[7]]]]) 
            return b
        data=ordering(u_data)
        lst=[]
        k=len(data)
        i=0
        a=str(float((requests.get( "https://api.thingspeak.com/channels/2491345/fields/1/last.json").json().get('field1'))[:-1])/100)+','+(str(float((requests.get( "https://api.thingspeak.com/channels/2491345/fields/2/last.json").json().get('field2'))[:-1])/100))
        while (i<k):
            lat1,lng1=map(float,data[i][1].split((",")))
            lat2,lng2=map(float,a.split(","))
            lst.append(haversine(lat1,lng1,lat2,lng2))
            i+=1
        for j in range(1, len(lst)):
            #print(lst)
            for i in range(j):
                if lst[i] > lst[j]:
                    t2=data[j]
                    t = lst[j]
                    data.pop(j)
                    lst.pop(j)
                    data.insert(i,t2)
                    lst.insert(i, t)
        print("Received information:", information)
        response_data = {'status': 'success', 'location': information}
        print(data)
        return jsonify(data)
    return render_template('test.html')


conn = pymysql.connect(host='localhost', user='root', password='', db='user_db')

@app.route('/login', methods=['GET', 'POST'])
def login():
    cursor = conn.cursor()

    if request.method == 'POST':
        email = request.form.get('email')

        if email:
            cursor.execute("SELECT name FROM user_form WHERE email = %s", (email,))
            result = cursor.fetchone()

            if result:
                name = result[0]
                return render_template('test.html', name=name)
            else:
                return "Invalid email or password"
        else:
            return "Email is missing"
    else:
        return render_template('login.html')
    
    
@app.route('/signup', methods=['GET', 'POST'])
    
def signup():
    error = []

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = hashlib.md5(request.form['psw'].encode()).hexdigest()

        connection_user = mysql.connector.connect(**db_config_user)
        cursor_user = connection_user.cursor()

        select_query = "SELECT * FROM user_form WHERE email=%s AND password=%s"
        cursor_user.execute(select_query, (email, password))
        if cursor_user.fetchone():
            error.append('User already exists!')
            print('User already exists:', email) 
        else:
            # Insert new user into database
            insert_query = "INSERT INTO user_form(name, email, password) VALUES (%s, %s, %s)"
            cursor_user.execute(insert_query, (name, email, password))
            connection_user.commit()
            cursor_user.close()
            print('User added:', email) 
            return redirect("/login") 

    return render_template('register.html', error=error)


if __name__ == '__main__':
    app.run(debug=True)