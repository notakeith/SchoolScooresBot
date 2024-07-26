ENV PATH=/root/.local:$PATH
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ="Europe/Moscow"


WORKDIR /app
COPY . /app

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# if Dockerfile in folder schoolscores-main
CMD ["python","main.py"]
# if Dockerfile in folder schoolscores-messages
CMD ["python","message_consumer.py"]
# if Dockerfile in folder schoolscores-scrapper
CMD ["python","scrapper_consumer.py"]
