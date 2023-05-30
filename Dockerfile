FROM python:3.10 as base

ENV WORKDIR=/plytz
WORKDIR ${WORKDIR}

RUN apt-get update && apt-get install -y \
    curl tar gzip openssh-client libyaml-dev unzip rsync jq expect \
    git autoconf bison build-essential libssl-dev libreadline6-dev \
    zlib1g-dev libncurses5-dev libffi-dev libgdbm6 libgdbm-dev libdb-dev

RUN useradd -mUs /bin/sh -d ${WORKDIR} plytz \
    && chown -R plytz:plytz ${WORKDIR}

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY --chown=plytz . .

EXPOSE 8000


FROM base as production
USER plytz
CMD ["uvicorn", "plytz_runner.main:app", "--host", "0.0.0.0"]
