FROM python:3.10 as base

WORKDIR /plytz

RUN apt-get update && apt-get install -y \
    curl tar gzip openssh-client libyaml-dev unzip rsync jq expect \
    git autoconf bison build-essential libssl-dev libreadline6-dev \
    zlib1g-dev libncurses5-dev libffi-dev libgdbm6 libgdbm-dev libdb-dev

COPY requirements.txt .
RUN pip install -r requirements.txt

FROM base as production
RUN useradd -mUs /bin/sh -d /plytz plytz \
    && chown -R plytz:plytz /plytz
COPY --chown=plytz . .
USER plytz
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
