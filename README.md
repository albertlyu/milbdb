# milbdb

## Introduction
This project starts as a sandbox for me learn PostgreSQL's JSON operators and functions on json and jsonb data types, using Minor League Baseball JSON data.

## Requirements
This project was built with Python 2.7.5 and PostgreSQL 9.4.0. The initial prototype was created on an OS X machine, in which PostgreSQL 9.4.0 was installed with [Postgresapp 9.4.0.1](https://github.com/PostgresApp/PostgresApp/releases/tag/9.4.0.1).

## Configuration
Update ```config.ini``` with your PostgreSQL credentials. Then create a ```milbdb``` database in your PostgreSQL 9.4 instance:
```
$ createdb -U [USERNAME] milbdb
```

## Instructions
Start a ```virtualenv``` instance and install the requirements.txt file:
```
$ virtualenv ENV
$ source ENV/bin/activate
$ pip install -r requirements.txt
```
Save some JSON files from data source into the ```data``` folder:
```
$ python save_files.py 2014-10-01 2014-10-31
```
Load some JSON data from data source into your database:
```
$ python load_json.py 2014-10-01 2014-10-31
```
Test a SQL query stored in a .sql file in the ```sql``` folder:
```
$ psql -U [USERNAME] -d milbdb -f 'sql/game_metadata.sql'
```

## Credits
Data courtesy of [MLBAM](http://gdx.mlb.com/components/copyright.txt).