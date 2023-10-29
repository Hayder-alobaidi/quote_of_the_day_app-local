import pika
import json

class RabbitMQPublisher:
    def __init__(self, amqp_url):
        self.amqp_url = amqp_url
        self.connection = pika.BlockingConnection(pika.URLParameters(self.amqp_url))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='quote_notifications', durable=False)

    def notify_analytics_service(self, quote_id):
        message = json.dumps({'quote_id': quote_id})
        self.channel.basic_publish(
            exchange='',
            routing_key='quote_notifications',
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))

    def close_connection(self):
        self.connection.close()
