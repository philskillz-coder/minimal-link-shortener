# minimal-link-shortener

## Available (working) database drivers:
- json
- other drivers will be added soon

## How to install:
````
git clone https://github.com/philskillz-coder/minimal-link-shortener.git
cd minimal-link-shortener
pip3 install -r requirements.txt
pip3 install markupsafe==2.0.1
python3 main.py
````

## How to reconfigure the app:
````
python3 main.py --configure
````

## Nginx config:
If you haven't changed the http bind and port you only have to change your domain and ssl certificate path here.
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
