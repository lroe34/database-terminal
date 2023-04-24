# database-terminal

Although I have put over 20 hours into this assignment over the course of the past few weeks, there still a few missing assignment criteria that I would like to recognize. The first is that, while the terminal can easily read databases and tables that are already availible on MySQL server, (say created through MySQL Workbench) it has a tough time creating tables that include procedures and functions. I believe I have narrowed down the root of this. I think that the 'DELIMITER' function which is built into MySQL is not native to sql.connector and, as such, cannot run through the connector. I have tried doing this as a multiline query as well with no luck. Since "Sakila-schema.sql" has special delimiters in it, ("//", "$$", etc.) it displays this behavior when being processed by the terminal. I have come to this conclusion after about 7 hours of bug-squashing and forum roaming and I have a fuzzy idea of what a work-around might look like:

```
import re   //for regex

function remove_delimiters.pseudo{
  lines = re.split(r";\n|;;\n|\$\$\n|//\n",sqlFile) //separate by '//', '$$', ';' and ';;'
  for line in lines:
    if line type == func or proc
        cursor.execute(line, multi=True)
        #somehow set the delimiter to work
    else:
        cursor.execute(line)
}
```

Furthermore, the drop tables function works, but it shouldbe noted that it will make a huge mess if the databases that it drops tables from. This is because it drops the table regardless of any keys that it may have which breaks tables that rely on it for foreign keys. I was going to implement a check from the INFORMATION_SCHEMA.TABLE_CONSTRAINTS table to more gracefully handle this, but unfortunetly I ran out of time (the beginnings of my code for this are evident in app.py). On this note, I was going to implement a feature to filter the table the user is viewing by a few user adjusted parameters, but also ran out of time for this feature. 

## Things I wish I had more time for:
- delimiter work-around 
- filter feature
- graceful drop table
- cleaner UI
- document code better


Note:
    I left the sakila examples and my own examples in the root directory, I hope this is ok since I have the program just search here for uploading the files rather than seeking them out in subdirectories. The examples I provide are .sql files I found online and work pretty well for testing. Similar to sakila, 01_mysql_create.sql must be run before any of 02-13 can be run since it build the table structure.