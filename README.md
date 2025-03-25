# Sip and Save
![Project logo](envapp/static/images/logo.png) test
## Welcome
This project is now complete. Thank you for your interest.
This is a sustainability app brought to you by The Procrastinators Dev Team.

# Deployment Guide on AWS EC2 with Custom Domain + SSL

This guide explains how to deploy a Django app from GitHub to AWS EC2 using Gunicorn, Nginx, a custom domain (from Namecheap), and a real SSL certificate (PositiveSSL).

---

## Prerequisites

-   Django app hosted on GitHub
-   AWS EC2 instance (Ubuntu 22.04+)
-   Domain from Namecheap (e.g., `<your-domain>`)
-   PositiveSSL certificate from Namecheap

---

## Step 1: Set Up Your EC2 Instance and Install Python 3.10

```bash
cd ~
sudo apt update && sudo apt install software-properties-common -y
sudo apt install nginx git curl build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget llvm libncurses5-dev \
libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.10 python3.10-venv python3.10-dev python3-pip -y
```

Verify:

```bash
python3.10 --version
```

---

## Step 2: Clone the Django App and Set Up Virtualenv

```bash
cd ~
git clone https://github.com/loco8406/ECM2434-Sustainability-Software.git
cd ECM2434-Sustainability-Software
python3.10 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Step 3: Run Migrations

```bash
python manage.py makemigrations envapp
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```

---

## Step 4: Run with Gunicorn

Install Gunicorn:

```bash
pip install gunicorn
```

Create the service:

```bash
sudo nano /etc/systemd/system/gunicorn.service
```

Paste:

```ini
[Unit]
Description=Gunicorn daemon for Sip&Save Django project
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/ECM2434-Sustainability-Software
ExecStart=/home/ubuntu/ECM2434-Sustainability-Software/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind 127.0.0.1:8000 \
          sipandsave.wsgi:application

[Install]
WantedBy=multi-user.target
```

Then:

```bash
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

---

## Step 5: Connect Domain to EC2

In Namecheap DNS panel:

-   **Type:** A Record
-   **Host:** `@`
-   **Value:** your EC2 public IP
-   **TTL:** Automatic

Repeat for `www` if needed.

---

## Step 6: SSL Certificate (Namecheap PositiveSSL)

### 1. Generate a CSR:

```bash
openssl req -new -newkey rsa:2048 -nodes -keyout <your-domain>.key -out <your-domain>.csr
```

### 2. Submit CSR to Namecheap and choose **DNS Validation**

They'll auto-create the DNS CNAME record.

### 3. Once validated, download your SSL cert ZIP

Upload both files:

```bash
scp -i your-key.pem <your-domain>.crt ubuntu@<ec2-ip>:/home/ubuntu/
scp -i your-key.pem <your-domain>.ca-bundle ubuntu@<ec2-ip>:/home/ubuntu/
```

Then:

```bash
cat <your-domain>.crt <your-domain>.ca-bundle > fullchain.pem
```

---

## Step 7: Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/ECM2434-Sustainability-Software
```

Paste:

```nginx
server {
    listen 80;
    server_name <your-domain> www.<your-domain>;
    return 301 https://$host$request_uri;
}
server {
    listen 443 ssl;
    server_name <your-domain> www.<your-domain>;

    ssl_certificate /home/ubuntu/fullchain.pem;
    ssl_certificate_key /home/ubuntu/<your-domain>.key;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/ubuntu/ECM2434-Sustainability-Software/staticfiles/;
    }

    location /media/ {
        alias /home/ubuntu/ECM2434-Sustainability-Software/envapp/media/;
    }
}
```

Enable the config:

```bash
sudo ln -s /etc/nginx/sites-available/ECM2434-Sustainability-Software /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## Final Check

Open your browser:

```
https://<your-domain>
```

