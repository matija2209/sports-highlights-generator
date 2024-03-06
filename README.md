# Highlights Generator

Merge all videos into one using HEVC and HEAAC.
`for f in *.mp4; do echo "file '$f'"; done > input.txt && ffmpeg -f concat -safe 0 -i input.txt -c:v libx265 -r 30 -vcodec hevc_videotoolbox -tag:v hvc1 -quality 60 -c:a aac -b:a 40k -ac 1 -y merged_video_3.mp4 && rm input.txt`

## Virtual Env

## Docker stuff
### Mac OS
- `pip freeze > requirements.txt`
- `pip install -r requirements.txt`
- `python3 -m virtualenv venv`
- `source venv/bin/activate`
### Windows 
- `pip freeze > requirements.txt`
- `pip install -r requirements.txt`
- `python -m venv venv`
- `venv\Scripts\activate`


### Upload account
`scp /Users/ziberna/ServiceAccounts/medical-practice-408309-fb7f20c8ed0a.json  matija@23.88.102.236:/home/matija/serviceAccounts`

## Docker

- Build image `sudo docker-compose build --no-cache`
- OR `docker build --platform linux/amd64 -t audio-transcriber-service .`
- Push to Hub `sudo docker-compose push`
— `sudo docker-compose build && sudo docker-compose push`
- Docker pull
  `sudo docker pull matija2209/audio-transcriber-service`
- Run container `sudo docker run -v /home/matija/serviceAccounts/medical-practice-408309-fb7f20c8ed0a.json:/app/key.json -e GOOGLE_APPLICATION_CREDENTIALS=/app/key.json -d -p 4853:80 matija2209/audio-transcriber-service`

_Make sure to create env file to include all variables needed for this microservice to run._

_ENVs_:

## Host

Server should run on `https://audio-transcriber-service.we-hate-copy-pasting.com/`

Nging config file:

```
server {
        server_name audio-transcriber-service.we-hate-copy-pasting.com;
        location / {
            proxy_pass         http://localhost:6543/;
            proxy_redirect     off;

            proxy_set_header   Host             $host;
            proxy_set_header   X-Real-IP        $remote_addr;
            proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
        }


    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/audio-transcriber-service.we-hate-copy-pasting.com/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/audio-transcriber-service.we-hate-copy-pasting.com/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
}
```

Generated cert with:
`sudo certbot --nginx -d audio-transcriber-service.we-hate-copy-pasting.com`
