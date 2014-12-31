#!/usr/bin/python
import ConfigParser
import psycopg2
from datetime import datetime, timedelta
import sys
import requests
import stage

def create_connection():
  """
  Create PostgreSQL connection given configuration file.
  """
  config = ConfigParser.ConfigParser()
  config.read("config.ini")
  localhost = config.get('postgresql','localhost')
  database = config.get('postgresql','database')
  username = config.get('postgresql','username')
  password = config.get('postgresql','password')
  conn_string = "host='" + localhost + "' dbname='" + database + "' user='" + username + "' password='" + password + "'"
  print("Connecting to database...")
  conn = psycopg2.connect(conn_string)
  print("Connection established!")
  return(conn)

if __name__ == "__main__":
  # Get list of dates and make sure dates are valid
  try:
    start_date = datetime.strptime(sys.argv[1], "%Y-%m-%d")
    end_date = datetime.strptime(sys.argv[2], "%Y-%m-%d")
    dates = [start_date + timedelta(days=x) for x in range((end_date-start_date).days+1)]
  except IndexError:
    print("Invalid start and end dates ('YYYY-MM-DD').")
    sys.exit()

  # Create PSQL connection and create table to store JSON data
  conn = create_connection()
  cursor = conn.cursor()

  create_table = "CREATE TABLE IF NOT EXISTS json_data (gid varchar(100), league varchar(3), file_type varchar(50), data jsonb, CONSTRAINT gid_file PRIMARY KEY(gid,file_type));"
  cursor.execute(create_table)

  # Load JSON into database given gid directories spanning date range
  master_urls = stage.get_master_urls(dates)
  file_names = ['boxscore.json','linescore.json','game_events.json','plays.json']
  base_url = "http://gdx.mlb.com/components/game/"
  gid_dirs = []
  for url in master_urls:
    gid_dirs = stage.get_gid_dirs(url)
    game_file_urls = [gid_dir+file_name for gid_dir in gid_dirs for file_name in file_names]
    for game_file_url in game_file_urls:
      gid = game_file_url.split('/')[-2]
      league = game_file_url.split('/')[-6]
      file_type = game_file_url.split('/')[-1].split('.')[0]
      r = requests.get(game_file_url)
      if r.status_code == 200:
        insert_record = "INSERT INTO json_data (gid,league,file_type,data) VALUES ('%s','%s','%s',$$%s$$);" % (gid,league,file_type,r.text)
        cursor.execute(insert_record)
        conn.commit()
        print("Inserted %s record for %s" % (file_type,gid))
      else:
        print("%s: Invalid URL was given at %s" % (r.status_code,game_file_url))

  # Close cursor connection
  cursor.close()
  conn.close()