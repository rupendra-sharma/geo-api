from flask import Flask, url_for, json
import psycopg2
app = Flask(__name__)

@app.route('/')
def api_root():
    return 'Welcome'

#get location by name
@app.route('/location/name')
def api_articles():

	try:
		conn = psycopg2.connect("dbname='geoapi' user='rupendra' host='localhost' password='pass@123'")
		cur = conn.cursor()
		
		#select the data
		cur.execute("""SELECT * from geodata""")
		
		rows = cur.fetchall()
		
		#return nearby locations
		return json.dumps(rows)
	except:
		return json.dumps("Status code: 500 Server error")

#Post location data
@app.route('/location/', , methods = ['POST'])
def api_article(articleid):
    if request.headers['Content-Type'] == 'text/plain':
        return "403, bad request: " + request.data

    elif request.headers['Content-Type'] == 'application/json':
		#save location data to database
		#load json data
		reqData = json.loads(request.json)
		
		#connect to the database
		conn = psycopg2.connect("dbname='geoapi' user='rupendra' host='localhost' password='pass@123'")
		cur = conn.cursor()
		
		#insert the data
		query = "INSERT into geodata(id, name, longitude, latitude) values(%d, %s, %d, %d);"
		data = (reqData["name"], reqData["longitude"], reqData["latitude"])
		cur.execute(query, data)
		
		conn.commit()
        
		return json.dumps("Status code: 200 ok")

if __name__ == '__main__':
    app.run()