#!/bin/sh

#
# set variables (use absolute filepaths)
#

s3_log="/var/log/kchung/s3_log.txt"
local_dir="/Users/development/kchung/archive"
remote_dir="s3://archive.kchungradio.org"

#
# s3 sync, requires awscli
#

printf "`date '+%Y-%m-%d  %H:%M:%S'`\n" >> $s3_log

/usr/local/bin/aws s3 sync --exclude "*" --include "*.mp3" --no-progress $local_dir $remote_dir >> $s3_log 2>&1

printf "`date '+%Y-%m-%d  %H:%M:%S'`\n" >> $s3_log
printf "\n" >> $s3_log
