FROM python:3.7

EXPOSE 8080

COPY requirements.txt requirements.txt
RUN pip install -U pip
RUN pip install -r requirements.txt


COPY images images
COPY data data
COPY app.py app.py
COPY config.yaml config.yaml
COPY sn.png sn.png
COPY sn2.png sn2.png
COPY viz.jpg viz.jpg

WORKDIR .

# ENTRYPOINT ["streamlit", "run"]
# CMD ["app.py"]

# CMD streamlit run --server.port 8080 --server.enableCORS false app.py

ENTRYPOINT [ "streamlit", "run" ]
CMD [ "app.py","--server.port", "8080", "--server.headless", "true", "--server.fileWatcherType", "none", "--browser.gatherUsageStats", "false"]