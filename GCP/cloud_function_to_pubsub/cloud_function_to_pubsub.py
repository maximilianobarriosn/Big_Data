""" Get an HTTP request (from a PUSH Topic with URL to Cloud Function as an entry point) and
    Publish a message to a Pub/Sub topic (with an timeout error handler).
"""

import base64
from concurrent import futures
from google.cloud import pubsub_v1

# TODO(developer)
project_id = "your_project-321019"
topic_id = "group_topic_1"

# Create publish client.
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)
publish_futures = []


def callback_to_catch_timeout_error(publish_future, data):
    '''
        This is a non-blocking function (callback) to handle timeout error when publishing on a topic.
    '''

    def callback(publish_future):
        try:
            # Wait 60 seconds for the publish call to succeed.
            print(publish_future.result(timeout=60))
        except futures.TimeoutError:
            print(f"Publishing {data} timed out.")

    return callback


def publish_to_topic(request):
    """Receive an HTTP request from topic and publish in another one.
    Args:
        request (flask.Request): HTTP request object.
    """

    # Get request in json format.
    request_json = request.get_json()
    # Get 'message' from json
    data_from_body = ''
    data_from_body = base64.b64decode(request_json['message']['data']).decode("utf-8")
    data_from_body = str(data_from_body)

    # Get topic info from request
    sub_from_body = str(request_json['subscription'])
    sub_from_body = sub_from_body.split('/')[-1]

    # Generate dict for response
    message_to_post = {}
    message_to_post['message'] = data_from_body
    message_to_post['topic'] = sub_from_body

    # Convert response to string and encode in UTF-8
    message_encoded = str(message_to_post)
    message_encoded = message_encoded.encode("utf-8")

    # When you publish a message, the client returns a future.
    publish_future = publisher.publish(topic_path, message_encoded)
    # Non-blocking. Publish failures are handled in the callback function.
    publish_future.add_done_callback(callback_to_catch_timeout_error(publish_future, message_encoded))
    publish_futures.append(publish_future)
