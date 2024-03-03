import psycopg2

__connection = None


def ensure_connected(host, port, dbname, user, password):
    global __connection
    if __connection is None:
        __connection = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )
        __connection.autocommit = True


def save_log(log_data):
    cursor = __connection.cursor()

    cursor.execute("""
        INSERT INTO access_logs (request_id, host, client_ip, time, method, path, query, status, referer, user_agent)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (log_data['request_id'], log_data['host'], log_data['client_ip'], log_data['time'],
          log_data['method'], log_data['path'], log_data['query'], log_data['status'],
          log_data['referer'], log_data['user_agent']))
