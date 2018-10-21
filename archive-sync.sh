#!/bin/sh

#
# set variables (use absolute filepaths)
#
s3log="/files/synced/from/local/to/s3/log.txt"
dblog="/new/entries/made/in/db/log.txt"
localdir="/your/local/directory/to/sync"
remotedir="s3://your.s3.name"
#

printf "`date '+%Y-%m-%d  %H:%M:%S'`\n" >> $log

/usr/local/bin/aws s3 sync --exclude "*" --include "*.mp3" --no-progress $localdir $remotedir >> $s3log 2>&1

printf "`date '+%Y-%m-%d  %H:%M:%S'`\n" >> $s3log
printf "\n" >> $s3log


#
# sync s3 to db
#

printf "`date '+%Y-%m-%d  %H:%M:%S'`\n" >> $dblog

/usr/local/bin/pipenv run python sync.py >> $dblog 2>&1

printf "`date '+%Y-%m-%d  %H:%M:%S'`\n" >> $dblog
printf "\n" >> $dblog
