FROM apache/airflow:2.10.4

RUN pip install apache-airflow-providers-apache-spark
USER root

RUN apt-get update
RUN apt-get install -y wget

# Instale o Java (necessário para PySpark)
RUN apt-get install -y openjdk-17-jdk
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Instalacao do SPARK
RUN wget "https://archive.apache.org/dist/spark/spark-3.5.4/spark-3.5.4-bin-hadoop3.tgz" && \
    tar -xzvf spark-3.5.4-bin-hadoop3.tgz && \
	mv spark-3.5.4-bin-hadoop3 /opt/spark && \
	rm spark-3.5.4-bin-hadoop3.tgz
ENV SPARK_HOME=/opt/spark
ENV SPARK_VERSION=3.5.4
ENV PATH=$SPARK_HOME/bin:$PATH

# DRIVER POSTGRES NO SPARK
#RUN wget -P /opt/spark/jars https://jdbc.postgresql.org/download/postgresql-42.7.5.jar

USER airflow
