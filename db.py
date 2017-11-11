from flask import Flask
from flask import request

import psycopg2
from psycopg2 import sql

app = Flask(__name__)

def connect():
    try:
        conn = psycopg2.connect("dbname='geolocations' user='power_user' host='localhost' password='password'")
        return conn
    except:
        return None


@app.route('/test', methods=['GET'])
def test():
  conn = connect()
  cur = conn.cursor()
  cur.execute(sql.SQL('INSERT INTO {} VALUES (%s)').format(sql.Identifier('test')), ['lmao'])
  conn.commit()
  conn.close()

  return "Successfully inserted meme."

@app.route('/add_points_of_interest', methods=['POST'])
def add_cities():
  conn = connect()
  cur = conn.cursor()
  points = request.json
  print len(points)
  parsed_points = [(i, p['Name'], " ".join(p['Type']), p['Description'], p['Latitude'], p['Longitude'], p['City_ID']) for i, p in enumerate(points)]

  args_str = ','.join(cur.mogrify("(%s, %s, %s, %s, %s, %s)", poi) for poi in parsed_points)
  cur.execute("INSERT INTO points_of_interest VALUES "  + args_str)
  conn.commit()
  conn.close()

  return "Successfully inserted points_of_interest."

@app.route('/add_photos', methods=['POST'])
def add_photos():
  conn = connect()
  cur = conn.cursor()
  photos = request.json
  parsed_photos = [(p['URL'], p['Date'], p['Time'], p['Popularity'], p['POI_Name']) for p in photos]

  args_str = ','.join(cur.mogrify("(%s, %s, %s, %s, %s)", photo) for photo in parsed_photos)
  cur.execute("INSERT INTO photo(url, date_taken, time_taken, popularity, POI_name) VALUES "  + args_str)
  conn.commit()
  conn.close()

  return "Successfully inserted photos."

# city post endpoint

# return places of interest, joined with city

#get route that takes in time, lat long bounding box and returns pictures sorted by popularity for that region, limited to some number

if __name__ == '__main__':
    app.run(debug=True, port = 80, host = '0.0.0.0')

