FROM rasa:1.10.16

WORKDIR /app

USER root

COPY ./actions /app/actions

USER 1001
