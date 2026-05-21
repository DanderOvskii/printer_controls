description:
this is a web aplictaion that can send gcode to a 3dprinter and stream the procces via multible webcams

initial install
pull from git: https://github.com/DanderOvskii/printer_controls
make .env file with USERNAME PASSWORD and SECRET_KEY
pip install from requirements.txt
make the file app.service in /etc/systemd/system/ so it start on the start of the mashine and fill it with 
[Unit]
Description=Gunicorn server
After=network.target

[Service]
User=dander
Group=www-data
WorkingDirectory=/home/dander/flask_app
Environment="PATH=/home/dander/flask_app/venv/bin"
ExecStart=/home/dander/flask_app/venv/bin/gunicorn --workers 1 --threads 4 --bind 192.168.1.224:5000 pro_app:app

[Install]
WantedBy=multi-user.target


start dev server: python3 app.py
start venv: venv/bin/activate


prod commands:
start: sudo systemctl start app
stop: sudo systemctl stop app
restart: sudo systemctl restart app
edit server: sudo nano /etc/systemd/system/app.service

discription
how to install
useful facts/commands