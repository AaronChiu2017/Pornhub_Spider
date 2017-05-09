#@IgnoreInspection BashAddShebang
FROM ubuntu:14.04

RUN sudo apt-get update && sudo apt-get install -y lrzsz python2.7    
RUN sudo apt-get install -y build-essential libssl-dev  libffi-dev python-pip python-dev libxml2-dev libxslt-dev  python-lxml
RUN sudo pip install  six --upgrade && sudo pip install requests pymongo redis twisted scrapy scrapy-redis

COPY . /code
WORKDIR /code
# RUN pip install -r requirements.txt
# COPY spiders.py /usr/local/lib/python3.5/site-packages/scrapy_redis

ENTRYPOINT ["python"]
CMD ["run_spider.py", ]