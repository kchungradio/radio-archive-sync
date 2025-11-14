# radio archive upload and sync

## file upload

`archive-sync.sh` is run by a cron job on the studio computer at 4am every morning

uploads files stored locally to s3 cloud storage

## syncing files on s3 to the database

`sync.py` is run in the cloud at 5-6am every morning

inserts a record into the database for any new file in the s3 bucket
(db is accessed by the website to list the shows)

the script ignores:

1. non-audio filetypes
2. folders with an invalid date format
3. folders older than 6 months

## local development

run the script locally

### configure local environment

create `config.ini` with credentials
(see `config.example.ini` for format)

```
brew install pipenv
brew install postgresql
pipenv install
```

if you get errors or need help, ask on slack (`#archive-help`)

### run sync script

`pipenv run python sync.py`

## docker deployment

runs s3 to db sync script on aws ecs fargate

### build docker image

`docker build -t archive-sync .`

### run docker image locally

`docker run archive-sync`

### log in to ecr

`aws ecr get-login-password --region us-west-2 --profile kchung | docker login --username AWS --password-stdin 989828836662.dkr.ecr.us-west-2.amazonaws.com/kchungradio`

### register docker image with ecr

`docker tag archive-sync 989828836662.dkr.ecr.us-west-2.amazonaws.com/archive-sync`

### push docker image to registry

`docker push 989828836662.dkr.ecr.us-west-2.amazonaws.com/archive-sync`

## References

<https://towardsdatascience.com/deploying-a-docker-container-with-ecs-and-fargate-7b0cbc9cd608>

<https://faun.pub/creating-an-ecs-scheduled-task-using-aws-cdk-a5a650ef36e8>

<https://github.com/shashimal/cdk-ecs-scheduled-task>
