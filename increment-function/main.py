import json
from google.cloud import firestore
from distributed_counters import Counter

NUM_SHARDS = 10
TOPIC_NAME = "VISITS"

def increment_counter(event, context):
    """Background Cloud Function to be triggered by Pub/Sub.
    Args:
         event (dict):  The dictionary with data specific to this type of
                        event. The `@type` field maps to
                         `type.googleapis.com/google.pubsub.v1.PubsubMessage`.
                        The `data` field maps to the PubsubMessage data
                        in a base64-encoded string. The `attributes` field maps
                        to the PubsubMessage attributes if any is present.
         context (google.cloud.functions.Context): Metadata of triggering event
                        including `event_id` which maps to the PubsubMessage
                        messageId, `timestamp` which maps to the PubsubMessage
                        publishTime, `event_type` which maps to
                        `google.pubsub.topic.publish`, and `resource` which is
                        a dictionary that describes the service API endpoint
                        pubsub.googleapis.com, the triggering topic's name, and
                        the triggering event type
                        `type.googleapis.com/google.pubsub.v1.PubsubMessage`.
    Returns:
        None. The output is written to Cloud Logging.
    """
    import base64

    print("""This Function was triggered by messageId {} published at {} to {}
    """.format(context.event_id, context.timestamp, context.resource["name"]))

    if 'data' in event:
        page = json.loads(base64.b64decode(event['data']).decode())['page']
    else:
        page = 'home'
        
    
    # https://cloud.google.com/firestore/docs/solutions/counters#python_2
    db_counters = firestore.Client()
    counter = Counter(NUM_SHARDS)
    counter.increment_counter(db_counters, page)
    print(f"Increment {page} in one visit")
    