FROM python:3.7

COPY dev-requirements.txt dev-requirements.txt
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
RUN pip install -r dev-requirements.txt
COPY . .

CMD ['python', '-m pytest tests/']