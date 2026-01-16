FROM nvcr.io/nvidia/pytorch:24.08-py3

ARG UNAME=pytorch
ARG UID=1000
ARG GID=1000
RUN groupadd -g $GID -o $UNAME \
    && useradd -m -u $UID -g $GID -o -s /bin/bash $UNAME

RUN mkdir /app \
    && chown -R $UID:$GID /app 

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src /app/src
COPY config.yaml .
COPY train.py .
COPY ingest.py .
COPY query.py .
COPY retrieve_vectors.py .

#RUN mkdir /results
#RUN chown -R $UID:$GID /results
RUN mkdir /vectors
RUN chown -R $UID:$GID /vectors
RUN chown -R $UID:$GID /app

USER $UNAME

ENTRYPOINT ["python"]
CMD ["train.py"]
