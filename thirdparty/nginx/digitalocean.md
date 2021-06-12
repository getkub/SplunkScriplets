https://www.digitalocean.com/community/tools/nginx

### /etc/nginx/nginx.conf
```
# Generated by nginxconfig.io
# https://www.digitalocean.com/community/tools/nginx?domains.0.server.domain=mysite.com&domains.0.server.wwwSubdomain=true&domains.0.server.cdnSubdomain=true

user                 www-data;
pid                  /run/nginx.pid;
worker_processes     auto;
worker_rlimit_nofile 65535;

# Load modules
include              /etc/nginx/modules-enabled/*.conf;

events {
    multi_accept       on;
    worker_connections 65535;
}

http {
    charset                utf-8;
    sendfile               on;
    tcp_nopush             on;
    tcp_nodelay            on;
    server_tokens          off;
    log_not_found          off;
    types_hash_max_size    2048;
    types_hash_bucket_size 64;
    client_max_body_size   16M;

    # MIME
    include                mime.types;
    default_type           application/octet-stream;

    # Logging
    access_log             /var/log/nginx/access.log;
    error_log              /var/log/nginx/error.log warn;

    # SSL
    ssl_session_timeout    1d;
    ssl_session_cache      shared:SSL:10m;
    ssl_session_tickets    off;

    # Diffie-Hellman parameter for DHE ciphersuites
    ssl_dhparam            /etc/nginx/dhparam.pem;

    # Mozilla Intermediate configuration
    ssl_protocols          TLSv1.2 TLSv1.3;
    ssl_ciphers            ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;

    # OCSP Stapling
    ssl_stapling           on;
    ssl_stapling_verify    on;
    resolver               1.1.1.1 1.0.0.1 8.8.8.8 8.8.4.4 208.67.222.222 208.67.220.220 valid=60s;
    resolver_timeout       2s;

    # Load configs
    include                /etc/nginx/conf.d/*.conf;
    include                /etc/nginx/sites-enabled/*;
}
```

### /etc/nginx/sites-available/mysite.com.conf
```
server {
    listen                  443 ssl http2;
    listen                  [::]:443 ssl http2;
    server_name             www.mysite.com;
    set                     $base /var/www/mysite.com;
    root                    $base/public;

    # SSL
    ssl_certificate         /etc/letsencrypt/live/mysite.com/fullchain.pem;
    ssl_certificate_key     /etc/letsencrypt/live/mysite.com/privkey.pem;
    ssl_trusted_certificate /etc/letsencrypt/live/mysite.com/chain.pem;

    # security
    include                 nginxconfig.io/security.conf;

    # index.php
    index                   index.php;

    # index.php fallback
    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    # additional config
    include nginxconfig.io/general.conf;

    # handle .php
    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php-fpm.sock;
        include      nginxconfig.io/php_fastcgi.conf;
    }
}

# CDN
server {
    listen                  443 ssl http2;
    listen                  [::]:443 ssl http2;
    server_name             cdn.mysite.com;
    root                    /var/www/mysite.com/public;

    # SSL
    ssl_certificate         /etc/letsencrypt/live/mysite.com/fullchain.pem;
    ssl_certificate_key     /etc/letsencrypt/live/mysite.com/privkey.pem;
    ssl_trusted_certificate /etc/letsencrypt/live/mysite.com/chain.pem;

    # disable access_log
    access_log              off;

    # gzip
    gzip                    on;
    gzip_vary               on;
    gzip_proxied            any;
    gzip_comp_level         6;
    gzip_types              text/plain text/css text/xml application/json application/javascript application/rss+xml application/atom+xml image/svg+xml;

    # allow safe files
    location ~* \.(?:css(\.map)?|js(\.map)?|ttf|ttc|otf|eot|woff2?|svgz?|jpe?g|png|gif|ico|cur|heic|webp|tiff?|mp3|m4a|aac|ogg|midi?|wav|mp4|mov|webm|mpe?g|avi|ogv|flv|wmv|pdf|docx?|dotx?|docm|dotm|xlsx?|xltx?|xlsm|xltm|pptx?|potx?|pptm|potm|ppsx?)$ {
        add_header Access-Control-Allow-Origin "*";
        add_header Cache-Control "public";
        expires    30d;
    }

    # deny everything else
    location / {
        deny all;
    }
}

# non-www, subdomains redirect
server {
    listen                  443 ssl http2;
    listen                  [::]:443 ssl http2;
    server_name             .mysite.com;

    # SSL
    ssl_certificate         /etc/letsencrypt/live/mysite.com/fullchain.pem;
    ssl_certificate_key     /etc/letsencrypt/live/mysite.com/privkey.pem;
    ssl_trusted_certificate /etc/letsencrypt/live/mysite.com/chain.pem;
    return                  301 https://www.mysite.com$request_uri;
}

# HTTP redirect
server {
    listen      80;
    listen      [::]:80;
    server_name cdn.mysite.com;
    include     nginxconfig.io/letsencrypt.conf;

    location / {
        return 301 https://cdn.mysite.com$request_uri;
    }
}

server {
    listen      80;
    listen      [::]:80;
    server_name .mysite.com;
    include     nginxconfig.io/letsencrypt.conf;

    location / {
        return 301 https://www.mysite.com$request_uri;
    }
}
```


### /etc/nginx/nginxconfig.io/letsencrypt.conf
```
# ACME-challenge
location ^~ /.well-known/acme-challenge/ {
    root /var/www/_letsencrypt;
}
```