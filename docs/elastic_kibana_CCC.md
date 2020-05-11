# Café com Código - Elasticsearch Kibana



## Roteiro de apresentação

- [x] Criar cluster básico com elasticsearch e Kibana na mesma versão.
- [x] Indicar que o elasticsearch possui uma REST api .
  - [x] http://localhost:9200
  - [x] curl -X POST http://localhost:9200/index
  - [x] curl -X POST http://localhost:9200/index/test/1 \
     -H 'content-type: application/json' \
     -d '{
       "name": "Adnan Siddiqi",
       "occupation": "Consultant"
     }'
  - [x] http://localhost:9200/company/employees/_search?q=adnan
  - [x] http://localhost:9200/company/employees/_mappings
- [x] Mudanças no projeto utilizando git diff.
- [x] Mudanças no docker-compose editar dependências entre containers, (talvez criar uma rede? TODO: Pesquisar).
- [x] Subir novamente o cluster e mostrar banco populado.
- [ ] Criar visualização básica no kibana.



---



## Cluster mais básico elasticsearch kibana

```yaml
version: '3.3'

services:

  elasticsearch:
    image: blacktop/elasticsearch:latest
    ports: 
     - "9200:9200"

  kibana:
    image: blacktop/kibana:latest
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch
```

TODO: Pesquisar o quanto essas alpines são boas (a melhora de espaço é considerável, o repositório tava bonito).



Acima um docker-compose básico com as configurações mínimas para rodar a última versão do EK já funcionando juntos.

O compose acima descreve dois serviços:

- **Elasticsearch**:  Apenas utiliza a última imagem disponível da versão alpine do elasticsearch. Aqui a porta padrão do elastic (`9200`) está direcionada para a nossa porta `9200`.
- **Kibana**: Assim como o de cima, versão alpine do kibana, para ele a porta padrão de configuração é a `5601` e na linha seguinte é criada uma relação com o elasticsearch, permitindo que o kibana acesse os dados do banco para gerar as visualizações.



---



## Conceitos Elasticsearch

### [Getting started elasticsearch](https://github.com/elastic/elasticsearch/edit/master/docs/reference/getting-started.asciidoc)

An index is a collection of documents that have somewhat similar characteristics. For example, you can have an index for customer data, another index for a product catalog, and yet another index for order data. An index is identified by a name (that must be all lowercase) and this name is used to refer to the index when performing indexing, search, update, and delete operations against the documents in it.



[Document](https://www.elastic.co/guide/en/elasticsearch/reference/current/getting-started-concepts.html#_document)

A document is a basic unit of information that can be indexed. For example, you can have a document for a single customer, another document for a single product, and yet another for a single order. This document is expressed in [JSON](http://json.org/)(JavaScript Object Notation) which is a ubiquitous internet data interchange format. Within an index, you can store as many documents as you want.

## Erros comuns

### [Not Defining Elasticsearch Mappings](https://logz.io/blog/the-top-5-elasticsearch-mistakes-how-to-avoid-them/)

Say that you start Elasticsearch, create an index, and feed it with JSON documents without incorporating schemas. Elasticsearch will then iterate over each indexed field of the JSON document, estimate its field, and create a respective mapping. While this may seem ideal, Elasticsearch mappings are not always accurate. If, for example, the wrong field type is chosen, then indexing errors will pop up.





---



## Pensando na próxima





[Basic Concepts](https://www.elastic.co/guide/en/elasticsearch/reference/current/getting-started-concepts.html)

**Cluster**

A cluster is a collection of one or more nodes (servers) that together holds your entire data and provides federated indexing and search capabilities across all nodes. A cluster is identified by a unique name which by default is "elasticsearch". This name is important because a node can only be part of a cluster if the node is set up to join the cluster by its name.

Make sure that you don’t reuse the same cluster names in different environments, otherwise you might end up with nodes joining the wrong cluster. For instance you could use `logging-dev`, `logging-stage`, and `logging-prod` for the development, staging, and production clusters.

Note that it is valid and perfectly fine to have a cluster with only a single node in it. Furthermore, you may also have multiple independent clusters each with its own unique cluster name.



**Node**

A node is a single server that is part of your cluster, stores your data, and participates in the cluster’s indexing and search capabilities. Just like a cluster, a node is identified by a name which by default is a random Universally Unique IDentifier (UUID) that is assigned to the node at startup. You can define any node name you want if you do not want the default. This name is important for administration purposes where you want to identify which servers in your network correspond to which nodes in your Elasticsearch cluster.

A node can be configured to join a specific cluster by the cluster name. By default, each node is set up to join a cluster named `elasticsearch` which means that if you start up a number of nodes on your network and—assuming they can discover each other—they will all automatically form and join a single cluster named `elasticsearch`.

In a single cluster, you can have as many nodes as you want. Furthermore, if there are no other Elasticsearch nodes currently running on your network, starting a single node will by default form a new single-node cluster named `elasticsearch`.



**Shards & Replicas**

An index can potentially store a large amount of data that can exceed the hardware limits of a single node. For example, a single index of a billion documents taking up 1TB of disk space may not fit on the disk of a single node or may be too slow to serve search requests from a single node alone.

To solve this problem, Elasticsearch provides the ability to subdivide your index into multiple pieces called shards. When you create an index, you can simply define the number of shards that you want. Each shard is in itself a fully-functional and independent "index" that can be hosted on any node in the cluster.



**Sources**: 

- [Getting started with elasticsearch in python](https://towardsdatascience.com/getting-started-with-elasticsearch-in-python-c3598e718380)
- [logzio](https://logz.io/)