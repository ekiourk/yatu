FROM yatu_base

RUN apt-get install -y supervisor
RUN pip3 install celery

RUN rm /etc/supervisor/supervisord.conf

ADD conf /opt/yatu/conf

RUN ln -s /opt/yatu/conf/supervisor-app.conf /etc/supervisor/conf.d/supervisor-app.conf

WORKDIR /opt/yatu

cmd ["supervisord", "-n", "-c", "/opt/yatu/conf/supervisord.conf"]