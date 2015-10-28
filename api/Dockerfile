FROM yatu_base

RUN apt-get install -y \
    nginx \
    supervisor

# Clear default configs
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN rm /etc/nginx/sites-enabled/default

# Install python packages
ADD requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

#configure the app
ADD src /opt/yatu/api/
ADD conf/uwsgi.ini /opt/yatu/uwsgi.ini
ADD conf/nginx-app.conf /etc/nginx/sites-enabled/nginx-app.conf
ADD conf/supervisor-app.conf /etc/supervisor/conf.d/supervisor-app.conf

expose 80

cmd ["supervisord"]
