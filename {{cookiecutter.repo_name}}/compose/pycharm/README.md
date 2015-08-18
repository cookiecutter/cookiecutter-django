docker-pycharm-python [![Docker Build Status](http://hubstatus.container42.com/tehsphinx/docker-pycharm-python)](https://registry.hub.docker.com/u/tehsphinx/docker-pycharm-python/)
====

Easy to use and [fig](http://www.fig.sh/index.html) compatible Python development box to be used with [PyCharm (JetBrains)](https://www.jetbrains.com/pycharm/). 
This box is NOT meant to be used in production. It comes with SSH/SFTP for PyCharm access.

For me this was a test to see if docker could be used as a "vagrant replacement" especially when it comes down to 
running unit tests and debugging from PyCharm IDE. So far it looks promising...

Note: SSH/SFTP User and Password implementation is based on [atmoz/sftp](https://registry.hub.docker.com/u/atmoz/sftp), 
but changed to use ENV variables for fig support.

Usage
-----

Best used with [fig](http://www.fig.sh/index.html).

Example
--------

Dockerfile

```
# Pull base image.
FROM tehsphinx/docker-pycharm-python

# copy application to image
ADD . /data/
WORKDIR /data

# If needed:
# install any python requirements found in requirements.txt (this file must be in root path of your app)
RUN pip install -r requirements.txt
```

Configuration for fig (fig.yml) 

```
web:
  build: .
  command: python app.py
  ports:
   - "8080:8080"
   - "2222:22"
  volumes:
   - .:/data
  environment:
    SFTP_USER: docker
    SFTP_PASS: docker
  links:
   - db
db:
  image: postgres
```

This samples a web server app (app.py) running on port 8080. PyCharm will be able to access the docker image with the
given user and on port 2222. If you do not want to store your password in plain text, you can use the 
Environment Variable "PASS_ENCRYPTED: true" to create the user with the already encrypted password.  
