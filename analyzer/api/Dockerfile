
FROM python:alpine3.19


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN python3 -m nltk.downloader stopwords wordnet

COPY . /code/api

EXPOSE 8081

CMD ["fastapi", "run", "api/api.py", "--port", "8081"]