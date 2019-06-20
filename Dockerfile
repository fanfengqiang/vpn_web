FROM ubuntu:18.04

ENV LANG zh_CN.UTF-8  
ENV LANGUAGE zh_CN:zh  
ENV LC_ALL zh_CN.UTF-8 

ENV APP_ROOT=/app/vpn \
    VPN_WEB_PORT=8443

RUN apt-get update \
    && apt-get install -y python3 python3-dev python3-pip nginx vim locales \
    && locale-gen zh_CN && locale-gen zh_CN.utf8 \
    && apt-get clean && apt-get autoclean \
    && pip3 install uwsgi \
    && pip3 install supervisor

COPY requirements.txt ${APP_ROOT}/requirements.txt

RUN cd ${APP_ROOT} \
    && pip3 install -r requirements.txt 

COPY . ${APP_ROOT}

RUN cd ${APP_ROOT} \
    && sed "s@#APP_ROOT#@${APP_ROOT}@g" supervisor.conf > /etc/supervisord.conf \
    && echo "daemon off;" >> /etc/nginx/nginx.conf \
    && echo "master_process on;" >> /etc/nginx/nginx.conf \
    && sed -e "s@#PORT#@${VPN_WEB_PORT}@g" -e "s@#APP_ROOT#@${APP_ROOT}@g" nginx.conf > /etc/nginx/sites-available/default

CMD ["supervisord","-n"]
