FROM python:3.11

# nodemonをインストールするためにNode.jsをインストール
RUN curl -fsSL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get update && \
    apt-get install -y nodejs npm

# nodemonをインストール
RUN npm install -g nodemon

WORKDIR /workspace
ADD .env requirements.txt app.py /workspace/
RUN pip install --upgrade -r /workspace/requirements.txt

EXPOSE 7860
# nodemonを使用してアプリケーションを実行
CMD ["nodemon", "--exec", "python", "app.py"]