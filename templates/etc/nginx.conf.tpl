server {
    listen 80;
    server_name 192.168.33.10;
    root /var/www/html/{{ project_name }};

    location / {
       include proxy_params;
       proxy_pass http://127.0.0.1:8000;
    }
}
