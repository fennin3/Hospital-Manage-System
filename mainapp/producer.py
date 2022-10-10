import pika
import json

params = pika.URLParameters('amqps://xregxoau:gqcHbeVpVyMOUbIT6Xp27DoxtBoFsCfb@jackal.rmq.cloudamqp.com/xregxoau')
# params.heartbeat = 600
# params.blocked_connection_timeout = 500

connection = pika.BlockingConnection(params)
# connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1:8000', heartbeat=600, blocked_connection_timeout=300))

channel = connection.channel()


def publish():
    print("PUBLISHING NOW....")
    data = ""
    with open('./mainapp/SQL_QUERIES.txt', 'r') as file:
        contents = file.readlines()
        data = {
            "queries":contents
        }
    data['node'] = 'node1'
    data = json.dumps(data)
    data.replace("\'", "\"")
    properties = pika.BasicProperties("sql_queries")
    channel.basic_publish(exchange='', routing_key='users', body=json.dumps(data), properties=properties)

    with open('./mainapp/SQL_QUERIES.txt', 'w') as file:
        file.write("")
