#INGESTAO
def main():
    import requests
    from pyspark.sql import SparkSession
    from pyspark.conf import SparkConf
    from pyspark.sql import SparkSession
    import os
    
    conf = SparkConf()
    #conf.set("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.2,com.amazonaws:aws-java-sdk-pom:1.12.365")
    conf.set('spark.hadoop.fs.s3a.aws.credentials.provider', 'org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider')
    conf.set("spark.hadoop.fs.s3a.access.key", os.getenv("AWS_ACCESS_KEY_ID"))
    conf.set("spark.hadoop.fs.s3a.secret.key", os.getenv("AWS_SECRET_ACCESS_KEY"))
    spark = SparkSession.builder.config(conf=conf).appName("ingestao-comments").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    url = "https://jsonplaceholder.typicode.com/comments"
    
    response = requests.get(url)        
    response.raise_for_status()  # Lança uma exceção para códigos de status HTTP ruins (4xx ou 5xx)
    
    df = spark.sparkContext.parallelize(response.json()).toDF()
    
    df.write.mode("overwrite").json('s3a://farmarcasbucket/comments-raw')

    spark.stop()

if __name__ == "__main__":
    main()

