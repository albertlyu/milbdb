#!/usr/bin/python
import ConfigParser
import psycopg2
import requests

def create_connection(config_file):
  """
  Create PostgreSQL connection given configuration file.
  """
  config = ConfigParser.ConfigParser()
  config.read(config_file)
  localhost = config.get('postgresql','localhost')
  database = config.get('postgresql','database')
  username = config.get('postgresql','username')
  password = config.get('postgresql','password')
  conn_string = "host='" + localhost + "' dbname='" + database + "' user='" + username + "' password='" + password + "'"
  print("Connecting to database...")
  conn = psycopg2.connect(conn_string)
  print("Connection established!")
  return(conn)

def create_cursor(conn):
  """
  Create cursor given a PostgreSQL connection.
  """
  return(conn.cursor())
  print("Cursor created.")

def create_table(conn,cursor,table_schema,table_name,columns,data_types):
  """
  Create a table given schema, table, columns, and their data types.
  """
  create_string = "CREATE TABLE IF NOT EXISTS %s.%s" % (table_schema,table_name)
  columns_list = zip(columns,data_types)
  columns_string = ','.join(("%s %s" % tup for tup in columns_list))
  create_table = "%s (%s);" % (create_string,columns_string)
  try:
    cursor.execute(create_table)
  except psycopg2.DatabaseError:
    conn.rollback()
  else:
    conn.commit()
    print("Created table %s.%s" % (table_schema,table_name))

def add_primary_key(conn,cursor,table_schema,table_name,constraint_name,pk_columns):
  """
  Add a primary key to a table given constraint name and pk columns.
  """
  alter_string = "ALTER TABLE %s.%s" % (table_schema,table_name)
  pk_string = ','.join(('%s' % column for column in pk_columns))
  constraint_string = "ADD CONSTRAINT %s PRIMARY KEY(%s)" % (constraint_name,pk_string)
  add_pk = alter_string + ' ' + constraint_string
  try:
    cursor.execute(add_pk)
  except psycopg2.DatabaseError:
    conn.rollback()
  else:
    conn.commit()
    print("Added primary key to %s.%s" %(table_schema,table_name))

def insert_json(conn,cursor,game_file_url):
  """
  Given a game_file_url that must be JSON, insert JSON data into database.
  """
  gid = game_file_url.split('/')[-2]
  league = game_file_url.split('/')[-6]
  file_type = game_file_url.split('/')[-1].split('.')[0]
  r = requests.get(game_file_url)
  if r.status_code == 200:
    insert_record = "INSERT INTO json_data (gid,league,file_type,data) VALUES ('%s','%s','%s',$$%s$$);" % (gid,league,file_type,r.text)
    try:
      cursor.execute(insert_record)
    except psycopg2.IntegrityError:
      conn.rollback()
      print("Error: Integrity violation with %s, %s" % (gid, file_type))
    else:
      conn.commit()
      print("Inserted %s record for %s" % (file_type,gid))
  else:
    print("%s: Invalid URL was given at %s" % (r.status_code,game_file_url))

def close_cursor(cursor):
  """
  Close cursor.
  """
  cursor.close()
  print("Cursor closed.")

def close_connection(conn):
  """
  Close PostgreSQL connection.
  """
  conn.close()
  print("Connection closed. Bye!")