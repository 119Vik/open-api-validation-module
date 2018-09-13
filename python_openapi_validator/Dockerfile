# According to https://docs.docker.com/engine/examples/running_ssh_service/
FROM ubuntu:18.04
# System setup
RUN apt-get update && apt-get install -y openssh-server python3-pip
# SSH setup
RUN mkdir /var/run/sshd
RUN echo 'root:root' |chpasswd
RUN sed -ri 's/^#?PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config
# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile
EXPOSE 22

# Application setup
ADD . ./python_openapi_validator
WORKDIR /python_openapi_validator
RUN python3 setup.py install

# SSHD run
CMD ["/usr/sbin/sshd", "-D"]

