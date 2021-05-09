# radio archive sync

uploads files stored locally to s3 storage

inserts a record into our database for any new file in the s3 bucket

logs everything

`archive-sync.sh` is run by a cron job on the studio computer at 4am every morning

## set up environment

create `kchung` profile in `.aws/credentials` with creds
create `kchung` profile in `.aws/config` with `region=us-west-2`
create `config.ini` with db creds
`brew install pipenv`
`brew install postgresql`
`pipenv install`

## run sync script

`pipenv run python sync.py`
