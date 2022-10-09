amqps_url = "amqps://xregxoau:gqcHbeVpVyMOUbIT6Xp27DoxtBoFsCfb@jackal.rmq.cloudamqp.com/xregxoau"

def save_sql_queries(query, model):
    with open('mainapp/SQL_QUERIES.txt', 'a') as file:
        file.write(str(query) + '\n')
