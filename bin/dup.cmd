cd c:\sitesbox

docker run --rm --env-file=%cd%/.env \
  -v %cd%/var/sites:/sites \
  #-v /etc/passwd:/sitesbox/passwd:ro \
  #-v /etc/shadow:/sitesbox/shadow:ro \
  -v %cd%/sites:/sitesbox/sites_configs:ro \
  -v %cd%/config/php-pool-templates:/sitesbox/custom_templates:ro \
  -v sitesbox_nginx_configs_volume:/sitesbox/nginx_configs \
  -v sitesbox_php7_pools_volume:/sitesbox/php-fpm.d \
  -v sitesbox_php73_pools_volume:/sitesbox/php73-fpm.d \
  -v sitesbox_php5_pools_volume:/sitesbox/php56-fpm.d \
  sitesbox_utils \
  /sitesbox/generate_configs.sh

docker run --rm --env-file=%cd%/.env \
  -v sitesbox_dnsmasq_hosts_volume:/sitesbox/dnsmasq_hosts \
  -v sitesbox_nginx_configs_volume:/sitesbox/nginx_configs:ro \
  sitesbox_utils \
  /sitesbox/generate_hosts.sh

docker-compose up -d
