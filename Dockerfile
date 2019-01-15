FROM python:3

COPY . /main

WORKDIR /main

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 5000

CMD [ "python", "./main.py" ]