from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime

with DAG("dag_farmarcas", start_date=datetime(2025,1,1), schedule_interval=None) as dag:
    
    ingestao_comments = SparkSubmitOperator(
        task_id="ingestao-comments",
        application="/opt/airflow/pyspark_scripts/ingestao-comments.py",
        conn_id="spark_default",
        packages="org.apache.hadoop:hadoop-aws:3.3.2,com.amazonaws:aws-java-sdk-pom:1.12.365",
        verbose=False
    )

    ingestao_posts = SparkSubmitOperator(
        task_id="ingestao-posts",
        application="/opt/airflow/pyspark_scripts/ingestao-posts.py",
        conn_id="spark_default",
        packages="org.apache.hadoop:hadoop-aws:3.3.2,com.amazonaws:aws-java-sdk-pom:1.12.365",
        verbose=False
    )
    
    transformacao_comments = SparkSubmitOperator(
        task_id="transformacao-comments",
        application="/opt/airflow/pyspark_scripts/transformacao-comments.py",
        conn_id="spark_default",
        packages="org.apache.hadoop:hadoop-aws:3.3.2,com.amazonaws:aws-java-sdk-pom:1.12.365",
        verbose=False
    )
    
    transformacao_posts = SparkSubmitOperator(
        task_id="transformacao-posts",
        application="/opt/airflow/pyspark_scripts/transformacao-posts.py",
        conn_id="spark_default",
        packages="org.apache.hadoop:hadoop-aws:3.3.2,com.amazonaws:aws-java-sdk-pom:1.12.365",
        verbose=False
    )
    
    publicacao_comments = SparkSubmitOperator(
        task_id="publicacao-comments",
        application="/opt/airflow/pyspark_scripts/publicacao-comments.py",
        conn_id="spark_default",
        packages="org.apache.hadoop:hadoop-aws:3.3.2,com.amazonaws:aws-java-sdk-pom:1.12.365",
        verbose=False
    )
    
    ingestao_comments >> transformacao_comments
    ingestao_posts >> transformacao_posts
    [transformacao_comments, transformacao_posts] >> publicacao_comments
