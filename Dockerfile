FROM ubuntu:latest
LABEL authors="pakvakunchik"

ENTRYPOINT ["top", "-b"]