cd /usr/local/apache2/htdocs/poll-monitor && \
    sed -i "s/<replace_prod_server_url>/$OPAL_SERVER_IP/g" main.*

httpd-foreground