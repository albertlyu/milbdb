/*
subject: boxscore
data: returns metadata about each game
  game id (gid)
  game date
  home team full name
  away team full name
  venue name
runtime: ~6 seconds (pgAdmin3)
*/

SELECT gid
  --,json_extract_path(json_extract_path(json_extract_path(json_data.data::json,'data'),'boxscore'),'date') AS date
  ,((json_data.data->>'data')::json->>'boxscore')::json->>'date' AS date
  ,((json_data.data->>'data')::json->>'boxscore')::json->>'home_fname' AS home_fname
  ,((json_data.data->>'data')::json->>'boxscore')::json->>'away_fname' AS away_fname
  ,((json_data.data->>'data')::json->>'boxscore')::json->>'venue_name' AS venue_name
FROM json_data
WHERE file_type = 'boxscore'
ORDER BY gid ASC
;