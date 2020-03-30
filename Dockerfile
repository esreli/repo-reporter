FROM python:3.7-alpine
RUN adduser -D appuser && \
    apk add openssl
WORKDIR /home/appuser

COPY requirements.txt requirements.txt
COPY run.py run.py
COPY app app
COPY app.sh app.sh
RUN pip install -r requirements.txt

ENV GITHUB_PERSONAL_ACCESS_TOKEN ""
ENV FLASK_ENV production

RUN chown -R appuser:appuser ./
USER appuser
EXPOSE 5002
ENTRYPOINT [ "./app.sh" ]
