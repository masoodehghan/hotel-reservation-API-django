FROM python:3.10.4-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN adduser hotel_admin --disabled-password

RUN su hotel_admin

WORKDIR /home/hotel_admin/code
COPY --chown=user:hotel_admin Pipfile Pipfile.lock /home/hotel_admin/code/
RUN pip install pipenv && pipenv install --system

USER hotel_admin


COPY --chown=user:hotel_admin src /home/hotel_admin/code/

