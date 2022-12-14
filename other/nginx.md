## Sample Nginx configuration

````
server {
    listen 80;
    server_name my.tld;
    return 301 https://$server_name$request_uri;
}

server {
        listen 443 ssl;
        listen [::]:443 ssl;
        server_name my.tld;

        ssl_certificate          /etc/letsencrypt/live/my.tld/fullchain.pem;
        ssl_certificate_key      /etc/letsencrypt/live/my.tld/privkey.pem;
        ssl_trusted_certificate  /etc/letsencrypt/live/my.tld/chain.pem;

        location / {
                proxy_set_header   X-Forwarded-For $remote_addr;
                proxy_set_header   Host $http_host;
                proxy_pass         http://127.0.0.1:5001;
       }

}
````

*Some values need to be changed!*

also in [this file](/other/nginx)