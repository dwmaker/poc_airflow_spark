

#TRANSFORMACAO
def main():
    from pyspark.sql import SparkSession
    from pyspark.conf import SparkConf
    from pyspark.sql.functions import regexp_replace
    import os
    
    conf = SparkConf()
    #conf.set("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.2,com.amazonaws:aws-java-sdk-pom:1.12.365")
    conf.set('spark.hadoop.fs.s3a.aws.credentials.provider', 'org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider')
    conf.set("spark.hadoop.fs.s3a.access.key", os.getenv("AWS_ACCESS_KEY_ID"))
    conf.set("spark.hadoop.fs.s3a.secret.key", os.getenv("AWS_SECRET_ACCESS_KEY"))
    spark = SparkSession.builder.config(conf=conf).appName("transformacao-posts").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    
    
    
    df = spark.read.json('s3a://farmarcasbucket/posts-raw')
    df = df.withColumnRenamed("userId", "usuario_id")
    df = df.withColumnRenamed("id", "postagem_id")
    df = df.withColumnRenamed("title", "titulo_postagem")
    #df = df.withColumnRenamed("body", "conteudo_postagem")
    #df = df.withColumn("conteudo_postagem", regexp_replace("conteudo_postagem", "\n", " "))
    df =  df.drop("body")



    

    df.write.mode("overwrite").json("s3a://farmarcasbucket/posts-consolidado")



    aaa = spark.read.json("s3a://farmarcasbucket/posts-consolidado")
    aaa.printSchema()
    aaa.show()

    spark.stop()
    
if __name__ == "__main__":
    main()


