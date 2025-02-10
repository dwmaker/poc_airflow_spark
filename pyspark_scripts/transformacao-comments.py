import urllib
import requests
from pyspark.sql import SparkSession

#TRANSFORMACAO
def main():
    from pyspark.sql import SparkSession
    from pyspark.conf import SparkConf
    from pyspark.sql import SparkSession
    import os
    
    conf = SparkConf()
    #conf.set("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.2,com.amazonaws:aws-java-sdk-pom:1.12.365")
    conf.set('spark.hadoop.fs.s3a.aws.credentials.provider', 'org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider')
    conf.set("spark.hadoop.fs.s3a.access.key", os.getenv("AWS_ACCESS_KEY_ID"))
    conf.set("spark.hadoop.fs.s3a.secret.key", os.getenv("AWS_SECRET_ACCESS_KEY"))
    spark = SparkSession.builder.config(conf=conf).appName("transformacao-comments").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    
    df = spark.read.json('s3a://farmarcasbucket/comments-raw')
    df = df.withColumnRenamed("postId", "postagem_id")
    df = df.withColumnRenamed("id", "comentario_id")
    df = df.withColumnRenamed("name", "nome_comentario")
    df = df.withColumnRenamed("email", "email_comentario")
    df = df.withColumnRenamed("body", "conteudo_comentario")
    
    df.show()

    df.write.mode("overwrite").json('s3a://farmarcasbucket/comments-consolidado')

    spark.stop()
    
if __name__ == "__main__":
    main()


    