from datetime import date, datetime

from google.cloud import firestore

from distributed_counters import Counter

NUM_SHARDS = 10


def init_counter(request):
    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return '', 204, headers

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    valid_pages = ["home", "jobs", "about", "about_legals", "about_offices"]

    request_json = request.get_json()

    if request_json and 'page' in request_json and request_json['page'] in valid_pages:
        page = request_json['page']
    else:
        return 'Page not found. Expected ?page=...', 404, headers

    db = firestore.Client()
    counter = Counter(NUM_SHARDS)
    counter.init_counter(db, page)
    return f"Shards created for page: {page} :)"


# L1 GET_COUNT CACHE
get_count_cache = [{}, {}]
# value, last_updated (every one minute it updates)


def get_count(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    global get_count_cache
    valid_pages = ["home", "jobs", "about", "about_legals", "about_offices"]

    request_args = request.args

    if request_args and 'page' in request_args and request_args['page'] in valid_pages:
        page = request_args['page']
    else:
        page = 'home'

    cache_count, cache_last_updated = get_count_cache

    if page not in cache_count or (datetime.now() - cache_last_updated[page]).seconds > 60:
        # Actualizo una vez por minuto la cuenta

        # https://cloud.google.com/firestore/docs/solutions/counters#python_2
        db_counters = firestore.Client()
        counter = Counter(NUM_SHARDS)

        total_count = counter.get_count(db_counters, page)
        cache_count[page] = total_count
        cache_last_updated[page] = datetime.now()

        get_count_cache = [cache_count, cache_last_updated]

        return str(total_count), 200
    else:
        return str(cache_count[page]), 200


################################################################

import json
from collections import defaultdict

from google.cloud import pubsub_v1

publisher = pubsub_v1.PublisherClient()
PROJECT_ID = "taller3-julianferres"
TOPIC_NAME = "VISITS"

# L1 GET_COUNT CACHE
post_visit_lazy_update = [defaultdict(int), {}]
# value, last_submitted (every one minute it updates)



def post_visit(request):
    global post_visit_lazy_update

    valid_pages = ["home", "jobs", "about", "about_legals", "about_offices"]

    request_args = request.args

    if request_args and 'page' in request_args and request_args['page'] in valid_pages:
        page = request_args['page']
    else:
        page = 'home'

    # https://cloud.google.com/functions/docs/calling/pubsub
    topic_name = TOPIC_NAME
    if not topic_name:
        return ('Missing "topic" and/or "message" parameter.', 400)

    print(f'Message message by post_visit, soon it will be dispatched')
    
    # References an existing topic
    topic_path = publisher.topic_path(PROJECT_ID, topic_name)

    post_visit_count, page_last_dispatch = post_visit_lazy_update

    # Publishes a message
    try:
        if page not in post_visit_count:
        # Despacho de forma lazy, como mucho una vez cada 5 segundos 
        # - Esto provoca una disminución fuerte de los mensajes en la cola, y 
        # de la cantidad de escrituras en firestore.
            post_visit_count[page] = 1
            page_last_dispatch[page] = datetime.now() # Init cache
        elif (datetime.now() - page_last_dispatch[page]).seconds < 60:
            post_visit_count[page] += 1
        else:  # Timeout
            message_json = json.dumps({'page': page, 'count': post_visit_count[page]})
            message_bytes = message_json.encode('utf-8')

            publish_future = publisher.publish(topic_path, data=message_bytes)
            publish_future.result()  # Verify the publish succeeded

            print(f"Publishing {message_json} to the queue :)")

            post_visit_count[page] = 0
            page_last_dispatch[page] = datetime.now() # Reset del cache

        post_visit_lazy_update = [post_visit_count, page_last_dispatch] # Actualizo el cache

        return 'Message published.'
    except Exception as e:
        print(e)
        return (e, 500)
