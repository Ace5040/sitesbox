FROM archlinux:latest
RUN echo "Set disable_coredump false" >> /etc/sudo.conf
RUN pacman --noconfirm -Syu; \
    pacman --needed --noconfirm -S base-devel git unzip mariadb-clients cronie python-pip certbot
RUN useradd -m -s /bin/bash dev; \
    usermod -p "dev" dev; \
    echo 'dev ALL=(ALL) NOPASSWD: ALL' | EDITOR='tee -a' visudo
RUN sed -i "s/#MAKEFLAGS=\"-j2\"/MAKEFLAGS=\"-j6\"/g" /etc/makepkg.conf
USER dev
WORKDIR /home/dev
RUN git clone https://aur.archlinux.org/yay.git
WORKDIR /home/dev/yay
RUN makepkg -scir --noconfirm
WORKDIR /home/dev
RUN yay --noeditmenu --nodiffmenu --noconfirm -S docker-systemctl-replacement-git docker
USER root
RUN pip install pyyml munch
RUN chown root:root /bin/systemctl.py; \
    chmod a+x /bin/systemctl.py; \
    mv /bin/systemctl /bin/systemctl_original; \
    cp /bin/systemctl.py /bin/systemctl
RUN systemctl enable cronie;
WORKDIR /
RUN mkdir -p /webcrate;
COPY ssl.conf /webcrate/ssl.conf
COPY parse-users.py /webcrate/parse-users.py
COPY certbot-renew.py /webcrate/certbot-renew.py
COPY certbot-renew-deploy.py /webcrate/certbot-renew-deploy.py
COPY entrypoint.sh /entrypoint.sh
RUN chmod a+x /webcrate/parse-users.py; \
    chmod a+x /webcrate/certbot-renew.py; \
    chmod a+x /webcrate/certbot-renew-deploy.py; \
    chmod u+x /entrypoint.sh
RUN echo '*/10 * * * * root /webcrate/parse-users.py' > /etc/cron.d/parse-users
RUN echo '0 6 * * * root /webcrate/certbot-renew.py' > /etc/cron.d/certbot-renew
WORKDIR /webcrate
CMD ["/entrypoint.sh"]