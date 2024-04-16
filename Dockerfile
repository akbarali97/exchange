FROM python:3.11.9

# setup app dir
COPY ./app /usr/src/app
WORKDIR /usr/src/app

# install python libraries
COPY ./requirements.txt /var/tmp/requirements.txt
RUN pip install --no-cache-dir -r /var/tmp/requirements.txt

# run script
CMD ["python", "main.py", '--show-log', '--exchanges a,b,c']