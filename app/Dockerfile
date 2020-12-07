FROM python:3.7.7

ENV ROOTDIR /var/lib/app
WORKDIR ${ROOTDIR}

ADD . ${ROOTDIR}

RUN pip install -r requirements.txt

RUN python manage.py collectstatic --noinput

RUN ln -s ${ROOTDIR}/entrypoint.sh /usr/local/bin/

RUN entrypoint.sh init && \
  entrypoint.sh createsuperuser

ENTRYPOINT ["entrypoint.sh"]
VOLUME /var/lib/app

CMD ["start"]
