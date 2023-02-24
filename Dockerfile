FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app/home.py .
COPY app/send_email.py .
COPY app/words.py
COPY app/zd_split_messages.py .
COPY app/zd_ticket_messages.py .

# TODO test the compilation of the docker image
CMD [ "python", "./home.py" ]
