/*
subject: boxscore
data: returns pitcher game stats for gid_2015_01_01_canwin_melwin_1
  game id (gid)
  home team full name
  away team full name
  team flag (home or away)
  innings pitched
  hits allowed
  runs allowed
  earned runs allowed
  walks allowed
  strikeouts
  home runs allowed
  earned run average
*/

SELECT gid
  ,((json_data.data->>'data')::json->>'boxscore')::json->>'home_fname' AS home_fname
  ,((json_data.data->>'data')::json->>'boxscore')::json->>'away_fname' AS away_fname
  ,((json_array_elements((((json_data.data->>'data')::json->>'boxscore')::json->>'pitching')::json))->>'team_flag') AS team_flag
  --,json_array_elements((((json_data.data->>'data')::json->>'boxscore')::json->>'pitching')::json) AS pitching
  --,json_array_elements((((json_data.data->>'data')::json->>'boxscore')::json->>'pitching')::json)->>'pitcher' AS pitchers
  --,json_array_elements((json_array_elements((((json_data.data->>'data')::json->>'boxscore')::json->>'pitching')::json)->>'pitcher')::json) AS pitcher
  ,json_array_elements((json_array_elements((((json_data.data->>'data')::json->>'boxscore')::json->>'pitching')::json)->>'pitcher')::json)->>'name_display_first_last' AS pitcher_full_name
  ,(json_array_elements((json_array_elements((((json_data.data->>'data')::json->>'boxscore')::json->>'pitching')::json)->>'pitcher')::json)->>'out')::int/3 AS ip
  ,(json_array_elements((json_array_elements((((json_data.data->>'data')::json->>'boxscore')::json->>'pitching')::json)->>'pitcher')::json)->>'out')::int%3 AS outs_left
  ,(json_array_elements((json_array_elements((((json_data.data->>'data')::json->>'boxscore')::json->>'pitching')::json)->>'pitcher')::json)->>'h')::int AS h
  ,(json_array_elements((json_array_elements((((json_data.data->>'data')::json->>'boxscore')::json->>'pitching')::json)->>'pitcher')::json)->>'r')::int AS r
  ,(json_array_elements((json_array_elements((((json_data.data->>'data')::json->>'boxscore')::json->>'pitching')::json)->>'pitcher')::json)->>'er')::int AS er
  ,(json_array_elements((json_array_elements((((json_data.data->>'data')::json->>'boxscore')::json->>'pitching')::json)->>'pitcher')::json)->>'bb')::int AS bb
  ,(json_array_elements((json_array_elements((((json_data.data->>'data')::json->>'boxscore')::json->>'pitching')::json)->>'pitcher')::json)->>'so')::int AS so
  ,(json_array_elements((json_array_elements((((json_data.data->>'data')::json->>'boxscore')::json->>'pitching')::json)->>'pitcher')::json)->>'hr')::int AS hr
  ,(json_array_elements((json_array_elements((((json_data.data->>'data')::json->>'boxscore')::json->>'pitching')::json)->>'pitcher')::json)->>'era')::float AS era
FROM json_data
WHERE file_type = 'boxscore' AND gid = 'gid_2015_01_01_canwin_melwin_1'
ORDER BY team_flag ASC
;