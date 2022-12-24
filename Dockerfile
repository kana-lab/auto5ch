FROM python:3.9

# ref: https://qiita.com/senth/items/c784fa5458e0de9e0256
RUN apt-get update && apt-get install -y unzip wget vim

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add && \
    wget http://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_108.0.5359.124-1_amd64.deb && \
    apt-get install -y -f ./google-chrome-stable_108.0.5359.124-1_amd64.deb

ADD https://chromedriver.storage.googleapis.com/108.0.5359.71/chromedriver_linux64.zip /opt/chrome/
RUN cd /opt/chrome/ && \
    unzip chromedriver_linux64.zip

# ref: https://community.fly.io/t/sqlite-problem-while-using-builder-full/8937/6
RUN mkdir /app
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/chrome

CMD ["python", "./app.py"]