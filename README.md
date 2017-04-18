# FYP

## Using Word of the People

### Prerequisites
* [Twython](https://github.com/ryanmcgrath/twython)
* [Python 2.7](https://docs.python.org/2/)
* [MySQLdb](http://mysql-python.sourceforge.net/MySQLdb.html)

### Initialisation

Create Tables using the `init_db.sql` file
The Database Class will attempt to connect to a localhost MySQL Database with username `wop`, password `password` and the database `FYP`.

From here Word of the People can be initialised by executing the command `python WOPMain.py`

If done correctly you should now be in the main Command Line Interface as shown below.
![Command Line Display][images/cli.png]
From here you should be able to create a client to begin collecting data. This will be the only functional command at first as there will be no data to compile or analyze.