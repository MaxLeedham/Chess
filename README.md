# Database setup
To run the game you first need to setup the database yourself locally

##### Linux:
```bash
cd ./database/
nano schema.txt
# Copy the contents of this file to the clipboard
# Then exit the file with ctrl-x
sqlite3 game_database.db
```
Paste the contents of the clipboard and exit with `ctrl-d`

##### Windows:
Create a new sqlite3 database in the `./database` directory using the schema provided in the `./database/schema.txt` file