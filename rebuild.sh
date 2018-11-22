docker build -f Dockerfile.poll_gui_server -t ds_poll_gui .
docker build -f Dockerfile.poll_server -t ds_poll ../
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d