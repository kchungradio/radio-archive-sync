FROM --platform=linux/amd64 python:3.12-slim as base

FROM base AS python-deps

RUN pip install pipenv
RUN apt-get update && apt-get -y --no-install-recommends install libpq-dev gcc

COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

FROM base AS runtime

COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

COPY . .

CMD ["python", "sync.py"]
