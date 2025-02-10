#PUBLICACAO
def main():
    
    from pyspark.sql import SparkSession
    from pyspark.conf import SparkConf
    from pyspark.sql.functions import count
    import os
    
    conf = SparkConf()
    #conf.set("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.2,com.amazonaws:aws-java-sdk-pom:1.12.365")
    conf.set('spark.hadoop.fs.s3a.aws.credentials.provider', 'org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider')
    conf.set("spark.hadoop.fs.s3a.access.key", os.getenv("AWS_ACCESS_KEY_ID"))
    conf.set("spark.hadoop.fs.s3a.secret.key", os.getenv("AWS_SECRET_ACCESS_KEY"))
    spark = SparkSession.builder.config(conf=conf).appName("publicacao-comments").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    
    df_comments = spark.read.json('s3a://farmarcasbucket/comments-consolidado')
    df_posts = spark.read.json('s3a://farmarcasbucket/posts-consolidado')
    
    df_comments = df_comments.groupBy("postagem_id").agg(count("comentario_id").alias("quantidade_comentarios"))
    df_comments = df_comments.withColumnRenamed("postagem_id", "postagem_id_drop")
    
    df = df_posts.join(df_comments, df_posts["postagem_id"] == df_comments["postagem_id_drop"], "left")
    df = df.drop("postagem_id_drop")

    df.write.mode("overwrite").json('s3a://farmarcasbucket/publicado')

    df.show()

    spark.stop()
    
if __name__ == "__main__":
    main()