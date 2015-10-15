FROM yatu_base

RUN apt-get install -y \
    nginx \
    supervisor

ADD src /opt/yatu/api/
ADD conf /opt/yatu/api/conf

# Clear default configs
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN rm /etc/nginx/sites-enabled/default && \
    rm /etc/supervisor/supervisord.conf

# Symlink our configs in
RUN ln -s /opt/yatu/api/conf/nginx-app.conf /etc/nginx/sites-enabled/ && \
    ln -s /opt/yatu/api/conf/supervisor-app.conf /etc/supervisor/conf.d/supervisor-app.conf && \
    ln -s /opt/yatu/api/conf/supervisord.conf /etc/supervisor/supervisord.conf

# Install python packages
ADD requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

#configure the app
expose 80
cmd ["supervisord", "-n"]
