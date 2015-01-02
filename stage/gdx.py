#!/usr/bin/python
import requests
import xml.etree.ElementTree as ET
import os

MILB_BASE_URL = "http://gdx.mlb.com/components/game/milb/"

def get_master_urls(dates):
  """
  Given a list of date objects, return list of milb_master_game_file.xml URLs
  """
  urls = []
  file_name = 'milb_master_game_file.xml'
  for date in dates:
    mid_url = "year_%s/month_%02d/day_%02d/" % (date.year,date.month,date.day)
    urls.append(MILB_BASE_URL + mid_url + file_name)
  return(urls)

def get_gid_dirs(master_game_url):
  """
  Given a master game URL, return list of gid directories.
  """
  r = requests.get(master_game_url)
  root = ET.fromstring(r.content)
  gid_dirs = []
  for child in root:
    if child.attrib['status'] == 'Final' and 'game//year_' not in child.attrib['boxscore']:
      boxscore_xml_url = child.attrib['boxscore']
      gid_dir = boxscore_xml_url.replace(boxscore_xml_url.split('/')[-1],'')
      gid_dirs.append(gid_dir)
  return(gid_dirs)

def save_game_file(game_file_url,base_url,base_path):
  """
  Given a game file URL, get contents of URL and save text as file.
  """
  r = requests.get(game_file_url)
  if r.status_code == 200:
    file_path = game_file_url.replace(base_url,base_path)
    file_name = game_file_url.split('/')[-1]
    dir_path = file_path.replace(file_path.split('/')[-1],'')
    if os.path.isfile(file_path):
      print("%s already exists at %s" % (file_name,dir_path))
    else:
      if not os.path.exists(dir_path):
        os.makedirs(dir_path)
      with open(file_path,'w') as output_file:
        output_file.write(r.text)
        print("Saved %s in %s" % (file_name,dir_path))
  else:
    print("%s: Invalid URL was given at %s" % (r.status_code,game_file_url))