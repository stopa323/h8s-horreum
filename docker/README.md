docker build --file docker/Dockerfile --tag h8s-horreum:0.1 .
docker run -itd --name h8s-horreum --network host h8s-horreum:0.1