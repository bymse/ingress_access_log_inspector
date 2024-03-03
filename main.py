import os
import time

import psycopg2
from kubernetes import client, config
from kubernetes.client.rest import ApiException
import storage
import parser


def get_env(env_var_name):
    return os.environ.get(env_var_name)


def inspect(namespace):
    config.load_kube_config()
    api = client.CoreV1Api()

    while True:
        try:
            pod_list = api.list_namespaced_pod(namespace=namespace,
                                               label_selector='app.kubernetes.io/component=controller',
                                               field_selector='status.phase=Running'
                                               )
            if not pod_list:
                print("Running ingress Nginx pod not found.")
                time.sleep(10)
                continue

            if len(pod_list.items) > 1:
                print("More than one Running ingress nginx pod found. Exit.")
                exit(-1)

            nginx_pod = pod_list.items[0].metadata.name
            print(f"Watching logs from {nginx_pod} pod.")

            logs = api.read_namespaced_pod_log(name=nginx_pod, namespace=namespace, follow=True,
                                               _preload_content=False)
            for log in logs:
                parsed_log = parser.parse_log(log.decode("utf-8").strip())
                if parsed_log:
                    storage.save_log(parsed_log)
        except KeyboardInterrupt:
            break
        except ApiException as e:
            if e.status == 404:
                print("Ingress Nginx pod not found.")
            else:
                print(f"Kubernetes API error: {e}")
            time.sleep(10)
        except psycopg2.OperationalError as e:
            print(f"PostgreSQL connection error: {e}")
            time.sleep(10)
        except Exception as e:
            print(f"Error occurred: {e}")
            time.sleep(10)


if __name__ == "__main__":
    config.load_kube_config()
    storage.ensure_connected(
        get_env('PG_HOST'),
        get_env('PG_PORT'),
        get_env('PG_DB'),
        get_env('PG_USER'),
        get_env('PG_PASSWORD')
    )
    inspect(get_env('K8S_INGRESS_NAMESPACE'))
    storage.close_connection()
