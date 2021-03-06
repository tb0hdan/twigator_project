FROM python:3.6-alpine
WORKDIR /
COPY requirements.txt ./
RUN apk update
RUN apk add --no-cache bash busybox-extras gcc libc-dev make
RUN pip install -U pip
RUN pip install --no-cache-dir -r requirements.txt
ADD ./bin /bin
ADD ./etc /etc
RUN mkdir /twigator
ADD ./twigator /twigator
# Security :-)
ARG TWITTER_CONSUMER_KEY
ENV TWITTER_CONSUMER_KEY=$TWITTER_CONSUMER_KEY
ARG TWITTER_CONSUMER_SECRET
ENV TWITTER_CONSUMER_SECRET=$TWITTER_CONSUMER_SECRET
ARG TWITTER_OAUTH_KEY
ENV TWITTER_OAUTH_KEY=$TWITTER_OAUTH_KEY
ARG TWITTER_OAUTH_SECRET
ENV TWITTER_OAUTH_SECRET=$TWITTER_OAUTH_SECRET
# Insecurity ;-)
EXPOSE 8000
