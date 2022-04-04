FROM registry.ccsteam.ru/bots/botx-app-base:3.9-master

COPY poetry.lock pyproject.toml ./
COPY pybotx-submodule pybotx-submodule

RUN poetry install --no-dev

COPY app app

ARG CI_COMMIT_SHA=""
ENV GIT_COMMIT_SHA=${CI_COMMIT_SHA}

CMD ["uvicorn", "--host=0.0.0.0", "app.main:app"]
