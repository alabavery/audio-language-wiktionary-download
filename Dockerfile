FROM python:3.8.7-slim-buster
RUN pip install --upgrade requests
RUN mkdir target_directory_mount && mkdir word_list_directory_mount && mkdir code
COPY ./code /code
WORKDIR /code
ENV LANGUAGE=not_provided
ENTRYPOINT python3 index.py "/word_list_directory_mount" "/target_directory_mount"