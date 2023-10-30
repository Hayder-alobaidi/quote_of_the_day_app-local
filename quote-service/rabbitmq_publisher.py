import pika
import json
import logging

class RabbitMQPublisher:
    def __init__(self, amqp_url, queue_name='quote_notifications'):
        self.amqp_url = amqp_url
        self.queue_name = queue_name
        self.connect()

    def connect(self):
        try:
            self.connection = pika.BlockingConnection(pika.URLParameters(self.amqp_url))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue_name, durable=True)
        except pika.exceptions.AMQPConnectionError as error:
            logging.error(f"Error connecting to RabbitMQ: {error}")
            # Optional: implement some delay or retry logic here

    def notify_analytics_service(self, quote_id):
        try:
            message = json.dumps({'quote_id': quote_id})
            self.channel.basic_publish(
                exchange='',
                routing_key=self.queue_name,
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                ))
        except (pika.exceptions.ChannelClosedByBroker, pika.exceptions.ConnectionClosedByBroker,
                pika.exceptions.ChannelWrongStateError) as error:
            logging.warning(f"Publishing failed, attempting to reconnect: {error}")
            self.reconnect()
            # Optional: Retry publishing the message here after reconnecting
            # Be cautious to avoid infinite retry loops

    def reconnect(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()
        self.connect()

    def close_connection(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()

# Usage remains the same in your Flask application
# rabbitmq_publisher = RabbitMQPublisher(your_amqp_url)
