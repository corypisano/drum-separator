# base image
FROM python:3.7

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# add requirements (to leverage Docker cache)
ADD ./requirements.txt /usr/src/app/requirements.txt

# install requirements, increase timeout for tensorflow
RUN apt-get update && apt-get install -y ffmpeg libsndfile1
RUN pip install --upgrade pip
RUN pip install --default-timeout=100 -r requirements.txt

# copy project
COPY . /usr/src/app

EXPOSE 5000

ENTRYPOINT [ "python" ]

CMD [ "application.py" ]