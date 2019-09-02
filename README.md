# OpenTracing Boto 3 Demo

This demo shows instrumentation of Boto 3 for span collecting.  
You can find all the code at [demo.py](demo.py).

## Requirements

* python
* pip
* docker
* docker-compose

## Running

```bash
docker-compose up -d
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python demo.py
```

Now you can go to the UI and check out a demo trace:
[http://localhost:16686](http://localhost:16686)

![Jaeger UI](https://raw.githubusercontent.com/Jamim/opentracing-boto3-demo/master/Boto3%20Demo%20-%20Jaeger%20UI.png)
