FROM yatu_base
ADD requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt
ADD src /opt/yatu/acceptance-tests/src

WORKDIR /opt/yatu/acceptance-tests
RUN rm -rf /var/opt/yatu
RUN mkdir /var/opt/yatu
CMD ["run-contexts", "src", "--verbose", "--xml", "/var/opt/yatu/acceptance-tests.xml"]
