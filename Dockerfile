FROM python:3.11-alpine
COPY requirements.txt /
RUN pip3 install -r requirements.txt

# Non project specific stuff
RUN apk update && apk add ffmpeg && apk add opus
COPY . /bot
WORKDIR /bot

ENTRYPOINT ["python3", "bot/bot.py"]