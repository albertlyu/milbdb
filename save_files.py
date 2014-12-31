#!/usr/bin/python
from datetime import datetime, timedelta
import sys
import stage

if __name__ == "__main__":
  # Get list of dates and make sure dates are valid
  try:
    start_date = datetime.strptime(sys.argv[1], "%Y-%m-%d")
    end_date = datetime.strptime(sys.argv[2], "%Y-%m-%d")
    dates = [start_date + timedelta(days=x) for x in range((end_date-start_date).days+1)]
  except IndexError:
    print("Invalid start and end dates ('YYYY-MM-DD').")
    sys.exit()

  # Fetch files given gid directories spanning date range
  master_urls = stage.get_master_urls(dates)
  file_names = ['boxscore.json','linescore.json','game_events.json','plays.json']
  base_url = "http://gdx.mlb.com/components/game/"
  base_path = "data/"
  gid_dirs = []
  for url in master_urls:
    gid_dirs = stage.get_gid_dirs(url)
    game_file_urls = [gid_dir+file_name for gid_dir in gid_dirs for file_name in file_names]

    for game_file_url in game_file_urls:
      stage.save_game_file(game_file_url,base_url,base_path)