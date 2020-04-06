#!/bin/sh

#
# set variables (use absolute filepaths)
#

s3_log="/var/log/kchung/s3_log.txt"
db_log="/var/log/kchung/db_log.txt"
local_dir="/path/to/archive"
remote_dir="s3://archive.kchungradio.org"

#
# s3 sync, requires awscli
#

printf "`date '+%Y-%m-%d  %H:%M:%S'`\n" >> $s3_log

/usr/local/bin/aws s3 sync --exclude "*" --include "*.mp3" --no-progress $local_dir $remote_dir >> $s3_log 2>&1

printf "`date '+%Y-%m-%d  %H:%M:%S'`\n" >> $s3_log
printf "\n" >> $s3_log


#
# sync s3 to db
#

printf "`date '+%Y-%m-%d  %H:%M:%S'`\n" >> $db_log

/usr/local/bin/pipenv run python sync.py >> $db_log 2>&1

printf "`date '+%Y-%m-%d  %H:%M:%S'`\n" >> $db_log
printf "\n" >> $db_log
