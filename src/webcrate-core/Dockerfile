FROM archlinux:latest
RUN echo "Set disable_coredump false" >> /etc/sudo.conf
RUN pacman --noconfirm -Syu
RUN pacman --needed --noconfirm -S git nano openssh base-devel unzip composer npm mariadb-clients dnsmasq mc iputils cronie inetutils which ruby python-pip python-virtualenv wget
RUN pacman --needed --noconfirm -S php php-fpm php-intl php-sqlite php-gd php-xsl php-tidy php-imagick php-memcached xdebug
RUN useradd -m -s /bin/bash dev
RUN usermod -p "dev" dev
RUN echo 'dev ALL=(ALL) NOPASSWD: ALL' | EDITOR='tee -a' visudo
RUN sed -i "s/#MAKEFLAGS=\"-j2\"/MAKEFLAGS=\"-j6\"/g" /etc/makepkg.conf
USER dev
WORKDIR /home/dev
RUN git clone https://aur.archlinux.org/yay.git
WORKDIR /home/dev/yay
RUN makepkg -scir --noconfirm
WORKDIR /home/dev
RUN yay --noeditmenu --nodiffmenu --noconfirm -S --mflags --nocheck php74 php74-fpm php74-intl php74-sqlite php74-gd php74-xsl php74-tidy php74-imagick php74-memcached php74-xdebug
RUN yay --noconfirm -R msmtp-mta
RUN yay --noeditmenu --nodiffmenu --noconfirm -S --mflags --nocheck php73 php73-fpm php73-intl php73-sqlite php73-gd php73-xsl php73-tidy php73-imagick php73-memcached php73-xdebug
RUN yay --noeditmenu --nodiffmenu --noconfirm -S --mflags --nocheck php56 php56-fpm php56-intl php56-sqlite php56-gd php56-xsl php56-tidy php56-imagick php56-memcached
RUN git clone https://aur.archlinux.org/php56-xdebug.git
WORKDIR /home/dev/php56-xdebug
RUN sed -i '31,38d;51d' PKGBUILD
RUN makepkg -scir --noconfirm
RUN gpg --keyserver keys.gnupg.net --recv-key 32E4B74757B1D65234FC389F293D771241515FE8
RUN yay --noeditmenu --nodiffmenu --noconfirm -S docker-systemctl-replacement-git symfony-cli telegraf-bin tmux fish proftpd
RUN yay --noeditmenu --nodiffmenu --noconfirm --mflags --nocheck -S composer1
RUN yay --noeditmenu --nodiffmenu --noconfirm -S vue-cli
RUN yay --noeditmenu --nodiffmenu --noconfirm -S python38
USER root
RUN wget -O drush.phar https://github.com/drush-ops/drush-launcher/releases/latest/download/drush.phar; \
    chmod +x drush.phar; \
    mv drush.phar /usr/bin/drush
RUN wget -O drush.0.8.0.phar https://github.com/drush-ops/drush-launcher/releases/download/0.8.0/drush.phar; \
    chmod +x drush.0.8.0.phar; \
    mv drush.0.8.0.phar /usr/bin/drush.0.8.0
RUN gem install compass --norc
RUN pip install pyyml munch
RUN pacman --noconfirm -R postfix
RUN pacman --noconfirm -S exim
RUN chown root:root /bin/systemctl.py
RUN chmod a+x /bin/systemctl.py
RUN mv /bin/systemctl /bin/systemctl_original
RUN cp /bin/systemctl.py /bin/systemctl
RUN ssh-keygen -A
RUN systemctl enable php56-fpm; \
    systemctl enable php73-fpm; \
    systemctl enable php74-fpm; \
    systemctl enable php-fpm; \
    systemctl enable sshd; \
    systemctl enable cronie; \
    systemctl enable telegraf; \
    systemctl enable exim; \
    systemctl enable dnsmasq; \
    systemctl enable proftpd
RUN printf "\ninclude=/etc/php56/php-fpm.d/*.conf" >> /etc/php56/php-fpm.conf; \
    sed -i "s/.*open_basedir =.*/open_basedir =/g" /etc/php56/php.ini; \
    sed -i "s/.*open_basedir =.*/open_basedir =/g" /etc/php73/php.ini; \
    sed -i "s/.*open_basedir =.*/open_basedir =/g" /etc/php74/php.ini; \
    sed -i "s/.*open_basedir =.*/open_basedir =/g" /etc/php/php.ini; \
    sed -i "s/;extension=imagick/extension=imagick/g" /etc/php/conf.d/imagick.ini; \
    sed -i "s/;extension=imagick/extension=imagick/g" /etc/php73/conf.d/imagick.ini; \
    sed -i "s/;extension=imagick/extension=imagick/g" /etc/php74/conf.d/imagick.ini; \
    sed -i "s/# urls = \[\"http\:\/\/127\.0\.0\.1\:8086\"\]/urls = \[\"http\:\/\/influxdb\:8086\"\]/g" /etc/telegraf/telegraf.conf; \
    sed -i "s/# skip_database_creation = false/skip_database_creation = true/g" /etc/telegraf/telegraf.conf; \
    sed -i "s/# database = \"telegraf\"/database = \"telegraf\"/g" /etc/telegraf/telegraf.conf;
#    sed -i 's/  interval = "10s"/  interval = "1s"/g' /etc/telegraf/telegraf.conf
WORKDIR /
COPY proftpd.conf /etc/proftpd.conf
RUN printf "no-resolv\nno-poll\nno-hosts\naddn-hosts=/webcrate-dnsmasq/config/hosts_nginx\n" > /etc/dnsmasq.conf
RUN echo ". /etc/profile.d/bashrc.sh" >> /etc/bash.bashrc
RUN echo 'dev ALL=(ALL) NOPASSWD: /bin/crontab' | EDITOR='tee -a' visudo
RUN sed -i 's/test -r /test -e /g' /etc/profile
RUN mkdir -p /webcrate; \
    mkdir -p /webcrate-bin; \
    mkdir -p /webcrate-bin/php; \
    mkdir -p /webcrate-bin/php74; \
    mkdir -p /webcrate-bin/php73; \
    mkdir -p /webcrate-bin/php56; \
    ln -s /bin/php /webcrate-bin/php/php; \
    ln -s /bin/php74 /webcrate-bin/php74/php; \
    ln -s /bin/php73 /webcrate-bin/php73/php; \
    ln -s /bin/php56 /webcrate-bin/php56/php; \
    ln -s /bin/drush.0.8.0 /webcrate-bin/php56/drush; \
    mkdir -p /webcrate-fish; \
    chmod o-rwx /webcrate
WORKDIR /webcrate-fish
RUN git clone https://github.com/oh-my-fish/oh-my-fish
WORKDIR /webcrate-fish/oh-my-fish
RUN bin/install --offline --path=/webcrate-fish/omf --noninteractive --config=/webcrate-fish/omfconf; \
    cp /root/.config/fish/conf.d/omf.fish /etc/fish/conf.d/omf.fish; \
    fish -C "omf install cbjohnson"; \
    cp /webcrate-fish/omf/themes/default/functions/fish_right_prompt.fish /webcrate-fish/omf/themes/cbjohnson/fish_right_prompt.fish;
COPY fish_prompt.fish /webcrate-fish/omf/themes/cbjohnson/fish_prompt.fish
WORKDIR /root
RUN wget https://downloads.ioncube.com/loader_downloads/ioncube_loaders_lin_x86-64.tar.gz; \
    tar xzvf ioncube_loaders_lin_x86-64.tar.gz; \
    cp ioncube/ioncube_loader_lin_7.4.so /usr/lib/php74/modules/ioncube_loader_lin.so; \
    cp ioncube/ioncube_loader_lin_7.3.so /usr/lib/php73/modules/ioncube_loader_lin.so; \
    cp ioncube/ioncube_loader_lin_5.6.so /usr/lib/php56/modules/ioncube_loader_lin.so; \
    rm /etc/php73/conf.d/xdebug.ini; \
    yes | sudo symfony self-update
WORKDIR /
RUN mkdir -p /webcrate-telegraf; \
    chown telegraf:telegraf /webcrate-telegraf; \
    chmod o-rwx /webcrate-telegraf; \
    mkdir -p /webcrate-dnsmasq; \
    chown dnsmasq:dnsmasq /webcrate-dnsmasq; \
    chmod o-rwx /webcrate-dnsmasq
COPY sync_ssh_keys.sh /webcrate/sync_ssh_keys.sh
COPY stats_projects.sh /webcrate-telegraf/stats_projects.sh
COPY stats_pools.sh /webcrate-telegraf/stats_pools.sh
COPY bashrc.sh /etc/profile.d/bashrc.sh
COPY fishrc.fish /etc/fish/conf.d/fishrc.fish
COPY toprc /etc/telegraf/.config/procps/toprc
COPY gunicorn_restart.sh /webcrate-bin/gunicorn_restart.sh
COPY parse-projects.py /webcrate/parse-projects.py
COPY versions.py /webcrate/versions.py
COPY entrypoint.sh /entrypoint.sh
COPY reload.py /webcrate/reload.py
RUN chmod u+x /webcrate/sync_ssh_keys.sh; \
    chmod a+x /webcrate-telegraf/stats_projects.sh; \
    chmod a+x /webcrate-telegraf/stats_pools.sh; \
    mkdir -p /etc/telegraf/.config/procps; \
    rm /etc/mail/exim.conf; \
    chmod a+x /webcrate-bin/gunicorn_restart.sh; \
    chmod u+x /webcrate/parse-projects.py; \
    chmod u+x /webcrate/reload.py; \
    chmod u+x /webcrate/versions.py; \
    chmod u+x /entrypoint.sh
CMD ["/entrypoint.sh"]
