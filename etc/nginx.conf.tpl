server {
    listen 80;
    server_name {{ domain }};
    root /var/www/html/{{ app_name }};

    location / {
       include proxy_params;
       proxy_pass http://127.0.0.1:8000;
    }
}

server {
   listen 80;
   server_name {{ subdomain }}.{{ domain }};
   return 301 http://{{ domain }}$request_uri;
}
