# minimal-link-shortener

## Issue reports
Issue reports are appreciated.
You can report one via
- the repositories [issues page](https://github.com/philskillz-coder/minimal-link-shortener/issues)
- [Mail](mailto:github@theskz.dev?subject=Issue%20report%20for%20minimal-link-shortener&body=Repository%20link%3A%0D%0Ahttps%3A%2F%2Fgithub.com%2Fphilskillz-coder%2Fminimal-link-shortener)
- my [Discord Server](https://discord.gg/QjntPW9fHc)
- Discord direct message to `Philskillz_#0266`

thanks in advance.

## Installation:

### Pre-Setup:
- [ <font color=GREEN>Required</font> ] Python 3.9 (may work with other versions)
- [ <font color=GREEN>Recommended</font> ] Nginx
- [ <font color=ORANGE>Optional</font> ] Postgres Database

### Available database drivers (needed in the installation step):
- json
- postgresql
- sqlite

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

### Other:
- A sample Nginx configuration can be found [here](/other/nginx.md)
- A sample ShareX configuration can be found [here](/other/sharex.md)
