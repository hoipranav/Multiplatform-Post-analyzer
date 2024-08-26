
FROM python:3.12


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY . /code/app


CMD ["streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]