FROM python

WORKDIR /root/

COPY main.py requirements.txt ./
RUN pip install -r requirements.txt

ENTRYPOINT python main.py

EXPOSE 8000/tcp
