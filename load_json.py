#!/usr/bin/python
from datetime import datetime, timedelta
import sys
import requests
from stage import gdx, database as db

if __name__ == "__main__":
  # Get list of dates and make sure dates are valid
  try:
    start_date = datetime.strptime(sys.argv[1], "%Y-%m-%d")
    end_date = datetime.strptime(sys.argv[2], "%Y-%m-%d")
    dates = [start_date + timedelta(days=x) for x in range((end_date-start_date).days+1)]
  except IndexError:
    print("Invalid start and end dates ('YYYY-MM-DD').")
    sys.exit()

  # Create PSQL connection
  conn = db.create_connection('config.ini')
  cursor = db.create_cursor(conn)

  # Create table to store JSON data
  table_schema = 'public'
  table_name = 'json_data'
  columns = ['gid','league','file_type','data']
  data_types = ['varchar(100)','varchar(3)','varchar(50)','jsonb']
  constraint_name = 'pk_gidfile'
  pk_columns = ['gid','file_type']

  db.create_table(conn,cursor,table_schema,table_name,columns,data_types)
  db.add_primary_key(conn,cursor,table_schema,table_name,constraint_name,pk_columns)
  
  # Load JSON into database given gid directories spanning date range
  master_urls = gdx.get_master_urls(dates)
  file_names = ['boxscore.json','linescore.json','game_events.json','plays.json']
  base_url = "http://gdx.mlb.com/components/game/"
  gid_dirs = []
  for url in master_urls:
    gid_dirs = gdx.get_gid_dirs(url)
    game_file_urls = [gid_dir+file_name for gid_dir in gid_dirs for file_name in file_names]
    for game_file_url in game_file_urls:
      db.insert_json(conn,cursor,game_file_url)

  # Close cursor connection
  db.close_cursor(cursor)
  db.close_connection(conn)