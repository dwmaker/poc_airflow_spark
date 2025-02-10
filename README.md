# poc_airflow_spark
Esta é uma Prova de Conceito (POC) de desenvolvimento que integra as tecnologias Airflow, Spark e S3. Nesta POC, o Airflow e o Spark serão executados em ambiente local, permitindo o desenvolvimento e teste de fluxos de dados complexos. O S3, por sua vez, será utilizado como armazenamento de dados na nuvem da AWS, demonstrando a capacidade de integração com serviços externos e escalabilidade da solução.

## DAGs

### dag_farmarcas
**Objetivo:** Extrair informações de postagens de dados de origem (https://jsonplaceholder.typicode.com), consolidar essas informações e disponibilizá-las em formato de consultas analíticas.

**Tarefas da DAG:**
- **Ingestão de dados:** Extrai dados de postagens e comentários de APIs e os disponibiliza em formato JSON no S3.
- **Transformação de dados:** Trata nomes de colunas, remove quebras de linhas no conteúdo das postagens e comentários.
- **Publicação de dados:** Agrega a quantidade de comentários por postagem.

As tasks desta DAG estão chamando o Spark via o operador `SparkSubmitOperator`. Este operador permite que o Airflow envie tarefas para serem executadas no cluster Spark. Ele é configurado com os parâmetros necessários para a submissão da aplicação Spark, como o caminho do script, argumentos, e configurações específicas do Spark.

Para acessar o S3, é necessário incluir os pacotes `org.apache.hadoop:hadoop-aws:3.3.2` e `com.amazonaws:aws-java-sdk-pom:1.12.365`. Esses pacotes fornecem as bibliotecas necessárias para que o Spark possa se comunicar com o serviço S3 da AWS, permitindo a leitura e escrita de dados diretamente no armazenamento em nuvem.

## Docker Compose

O Docker Compose possui os seguintes containers:

### Ambiente Airflow
- **postgres:** Banco de dados relacional utilizado pelo Airflow para armazenar metadados, como o estado das DAGs e tarefas.
- **redis:** Broker de mensagens utilizado pelo Airflow para gerenciar a fila de tarefas.
- **airflow-webserver:** Interface web do Airflow, onde é possível visualizar e gerenciar as DAGs e tarefas.
- **airflow-scheduler:** Responsável por agendar a execução das tarefas definidas nas DAGs.
- **airflow-worker:** Executa as tarefas das DAGs em paralelo.
- **airflow-triggerer:** Gerencia os triggers do Airflow, que são responsáveis por iniciar a execução de tarefas com base em eventos.
- **airflow-init:** Inicializa o ambiente do Airflow, configurando o banco de dados e criando as tabelas necessárias (temporário).
- **airflow-cli:** Interface de linha de comando do Airflow, utilizada para executar comandos administrativos (opcional).
- **flower:** Interface web para monitoramento do Celery, que é o sistema de execução de tarefas assíncronas utilizado pelo Airflow (opcional).

### Ambiente Spark
- **spark-master:** Nó mestre do cluster Spark, responsável por gerenciar os recursos e distribuir as tarefas entre os nós trabalhadores.
- **spark-worker:** Nó trabalhador do cluster Spark, responsável por executar as tarefas distribuídas pelo nó mestre.
