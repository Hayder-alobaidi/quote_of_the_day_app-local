import pika
import json

class RabbitMQPublisher:
    def __init__(self, amqp_url, queue_name='quote_notifications'):
        self.amqp_url = amqp_url
        self.queue_name = queue_name
        self.connection = pika.BlockingConnection(pika.URLParameters(self.amqp_url))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=True)

    def notify_analytics_service(self, quote_id):
        message = json.dumps({'quote_id': quote_id})
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))

    def close_connection(self):
        self.connection.close()
