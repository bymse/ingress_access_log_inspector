import json


def parse_log(log):
    try:
        parsed = json.loads(log)
        path, query = parsed['request_uri'].split('?') if '?' in parsed['request_uri'] else (parsed['request_uri'], '')
        return {
            'host': parsed['host'],
            'request_id': parsed['request_id'],
            'client_ip': parsed['remote_addr'],
            'time': parsed['time_local'],
            'method': parsed['request_method'],
            'path': path,
            'query': query,
            'status': parsed['status'],
            'referer': parsed['http_referer'],
            'user_agent': parsed['http_user_agent']
        }
    except json.JSONDecodeError:
        return None
