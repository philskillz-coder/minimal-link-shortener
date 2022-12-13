# minimal-link-shortener

Bug/issue reports are appreciated.
You can report a bug via
- the repositories [issues page](https://github.com/philskillz-coder/minimal-link-shortener/issues)
- [Mail](mailto:philipp@theskz.dev) (Please add `gh-LhAwk` in the subject)
- my [Discord Server](https://discord.gg/QjntPW9fHc)
- Discord direct message to `Philskillz_#0266`

thanks in advance.

# Install:
### Available database drivers (needed in the installation step):
- json
- postgresql
- <font color="orange">sqlite</font> (in work)

other drivers will be added soon


### How to install:
````
git clone https://github.com/philskillz-coder/minimal-link-shortener.git
cd minimal-link-shortener
pip3 install -r requirements.txt
pip3 install markupsafe==2.0.1
python3 configure.py
````

### How to (re)configure the app:
````
python3 configure.py [--driver] [--authorization] [--http-bind] [--http-port]
````

### Nginx config:
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
