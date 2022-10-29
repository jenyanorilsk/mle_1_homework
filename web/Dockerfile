FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt
RUN pip python src/preprocess.py && python src/train.py && python src/predict.py -t func && coverage run src/unit_tests/test_preprocess.py && coverage run -a src/unit_tests/test_train.py && coverage run -a src/unit_tests/test_predict.py && coverage report -m
