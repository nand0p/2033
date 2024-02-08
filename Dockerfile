FROM python:3.8-slim-buster

ENV STOCKS=None
ENV MPLCONFIGDIR=/tmp/.cache

WORKDIR /

COPY . .
RUN pip3 install -r requirements.txt


CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--debug" ]
