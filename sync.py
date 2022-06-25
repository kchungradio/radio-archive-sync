import configparser
from datetime import datetime, timedelta
from getpass import getpass

import boto3
import psycopg2

def valiDate(date_text):
    try:
        if date_text != datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d'):
            raise ValueError
        return True
    except ValueError:
        return False

# get db config
config = configparser.ConfigParser()
config.read('config.ini')
host = config['DEFAULT']['DB_HOST']
dbname = config['DEFAULT']['DB_NAME']
user = config['DEFAULT']['DB_USER']
password = config['DEFAULT']['DB_PASS']

# login to s3 using boto config
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
six_months_ago = now - timedelta(days=183)

for object in bucket.objects.all():
    path = object.key

    print(path)

    if not path.endswith((
        '.mp3', '.MP3',
        '.m4a', '.M4A',
        '.mp4', '.MP4',
        '.aiff', '.AIFF',
        '.aif', '.AIF',
        '.wav', '.WAV'
        )):
        continue

    # filename = path.split('/')[-1]
    date = path.split('/')[0][:10]

    if not valiDate(date):
        continue

    if datetime.fromisoformat(date) < six_months_ago: # skip old dates
        continue

    # lookup file in db
    cursor.execute('''
    SELECT id FROM radio.archive
    WHERE path = %s
    ''', [path])
    row = cursor.fetchone()

    # if record exists, do nothing
    if row:
        continue

    # insert into db
    cursor.execute('''
    INSERT INTO radio.archive
    (path, date, created_at, created_by)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (path) DO NOTHING
    ''',
    (path, date, now, app_name))

    print('=====================SUCCESS=====================')

conn.commit()
cursor.close()
conn.close()

