FROM python:3.6

EXPOSE 8000

WORKDIR /mc/{{ cookiecutter.project_slug }}

ADD requirements requirements

RUN pip install -r requirements/production.txt

RUN apt-get update && apt-get install -y unzip

RUN wget https://releases.hashicorp.com/envconsul/0.6.1/envconsul_0.6.1_linux_amd64.zip && unzip envconsul_0.6.1_linux_amd64.zip -d /usr/local/bin

ADD . /mc/{{ cookiecutter.project_slug }}

RUN chmod +x run.sh

ENTRYPOINT ["./run.sh"]

CMD ["{{ cookiecutter.project_slug }}"]