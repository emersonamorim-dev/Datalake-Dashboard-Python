FROM bde2020/spark-master:3.0.0-hadoop3.2
USER root
RUN apt-get update && apt-get install -y python3-pip python3-dev
RUN pip3 install pyspark==3.0.0 pandas

