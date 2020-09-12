FROM python:3.8-slim-buster as build_stage

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements

RUN apt-get update && apt-get install --no-install-recommends -y \
    # dependencies for building Python packages
    build-essential \
    # psycopg2 dependencies
    libpq-dev \
    # Translations dependencies
    gettext \
    # Uncomment below lines to enable Sphinx output to latex and pdf
    # texlive-latex-recommended \
    # texlive-fonts-recommended \
    # texlive-latex-extra \
    # latexmk \
    # cleaning up unused files
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/* \
	# install python dependencies
    && pip install --no-cache-dir --use-feature=2020-resolver -r /requirements/local.txt -r /requirements/production.txt \
    && rm -rf /requirements


FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1


RUN apt-get update && apt-get install --no-install-recommends -y \
    # dependencies for building Python packages
    build-essential \
    # psycopg2 dependencies
    libpq-dev \
    # Translations dependencies
    gettext \
    # Uncomment below lines to enable Sphinx output to latex and pdf
    # texlive-latex-recommended \
    # texlive-fonts-recommended \
    # texlive-latex-extra \
    # latexmk \
    # cleaning up unused files
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*


# copy python dependencies from python-build-stage
COPY --from=build_stage /usr/local/lib/python3.8/site-packages/ /usr/local/lib/python3.8/site-packages/
COPY --from=build_stage /usr/local/bin/ /usr/local/bin/


WORKDIR /docs

CMD make livehtml
