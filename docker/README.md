## Container operations

### Building image
```
docker build --file docker/Dockerfile --tag h8s-horreum:<TAG> .
```

### Running container
Default run:
```
docker run -itd \
  --name h8s-horreum \
  -e DYNAMODB_ENDPOINT_URL=dynamodb.eu-west-1.amazonaws.com \
  -p 8000:8000 \
  h8s-horreum:0.1.0.dev
```

Passing parameters to uvicorn:
```
docker run -itd \
  --name h8s-horreum \
  -e DYNAMODB_ENDPOINT_URL=dynamodb.eu-west-1.amazonaws.com \
  -p 8000:5000 \
  h8s-horreum:0.1.0.dev \
  --host 0.0.0.0 \
  --port 5000
```