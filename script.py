import configparser
from datetime import datetime
from getpass import getpass

import boto3
import psycopg2

# get db config
config = configparser.ConfigParser()
config.read('config.ini')
host = config['DEFAULT']['DB_HOST']
dbname = config['DEFAULT']['DB_NAME']
user = config['DEFAULT']['DB_USER']
password = config['DEFAULT']['DB_PASS']

# boto config
session = boto3.session.Session(profile_name='kchung')
s3 = session.resource('s3')
bucket = s3.Bucket('archive.kchungradio.org')

# connect to db
conn = psycopg2.connect(
        host=host,
        dbname=dbname,
        user=user,
        password=password)
cursor = conn.cursor()

app_name = 'sync'
now = datetime.now()

for object in bucket.objects.all():
    path = object.key

    if path.endswith((
        '.mp3', '.MP3',
        '.m4a', '.M4A',
        '.mp4', '.MP4',
        '.aiff', '.AIFF',
        '.aif', '.AIF',
        '.wav', '.WAV'
        )):

        # filename = path.split('/')[-1]
        date = path.split('/')[0][:10]

        # lookup file in db
        cursor.execute('''
        SELECT id FROM radio.archive
        WHERE path = %s
        ''', [path])
        row = cursor.fetchone()

        # if record exists, do nothing
        if row:
            continue

        print(path)

        # insert into db
        cursor.execute('''
        INSERT INTO radio.archive
        (path, date, created_at, created_by)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (path) DO NOTHING
        ''',
        (path, date, now, app_name))

conn.commit()
cursor.close()
conn.close()

