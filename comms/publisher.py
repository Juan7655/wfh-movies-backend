from google.cloud import pubsub_v1


def run():
    project_id = "hey-movie"
    topic_name = "HeyMovieTema"

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)

    for n in range(1, 2):
        data = u"Message number {}".format(n)
        data = '{ "user": 1, "movie": 1, "rating": 0.9 }'
        data = data.encode("utf-8")
        future = publisher.publish(topic_path, data=data)
        print(f'message: {data}     |   future result: {future.result()}')

    print("Published messages.")


if __name__ == '__main__':
    run()
