
# KBE_SERVER
#
# VERSION              0.0.1
# TIPS: this file should be change cautiously, the docker-compose rely this file.

# Base image to use, this must be set as the first lime
FROM ubuntu

# Maintainer: docker_user <docker_user email>
MAINTAINER honglimin 693749857@qq.com

# conmands to update the image and install some neccessary software
RUN apt update
RUN apt install -y vim
RUN apt install -y lsb-release
RUN apt install -y gcc
RUN apt install -y libmysqlclient20
RUN apt install -y telnet
RUN apt install -y python
RUN apt install -y sudo

#RUN chmod -R 777 /kbengine
RUN useradd -r -u {uid} -G root kbe
USER kbe

# new volume in docker
VOLUME ["/kbengine/assets", "/kbengine/assets/logs", "/kbengine/kbe/"]

# expose this docker inner port
##### EXPOSE 20013 20015 20016 20017 40000 50000

# enter the directory after the build
WORKDIR /kbengine/assets/



# excute command after build
##### CMD ["sh" ,"/kbengine/assets/start_server.sh"]
