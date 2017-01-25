import logging
import time
from rabbitmq_consumer import launch_rabbitmq, example

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
                '-35s %(lineno) -5d: %(message)s')


logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

LOGGER = logging.getLogger(__name__)

def on_message(unused_channel, basic_deliver, properties, body):
    """Invoked by pika when a message is delivered from RabbitMQ. The
    channel is passed for your convenience. The basic_deliver object that
    is passed in carries the exchange, routing key, delivery tag and
    a redelivered flag for the message. The properties passed in is an
    instance of BasicProperties with the message properties and the body
    is the message that was sent.

    :param pika.channel.Channel unused_channel: The channel object
    :param pika.Spec.Basic.Deliver: basic_deliver method
    :param pika.Spec.BasicProperties: properties
    :param str|unicode body: The message body

    """
    LOGGER.info('Received message # %s from %s: %s',
                basic_deliver.delivery_tag, properties.app_id, body)
    
    
    example.on_message_ack(basic_deliver)
    LOGGER.info('Work in progress')

    time.sleep( 90 )

    LOGGER.info('Work end !')


def on_reconnect(self, unused_frame):
        """Invoked by pika when the queue.Bind method has completed. At this
        point we will start consuming messages by calling start_consuming
        which will invoke the needed RPC commands to start the process.

        :param pika.frame.Method unused_frame: The queue.BindOk response frame

        """
        LOGGER.info('queue bound')
        example.start_consuming('reader', on_message)


launch_rabbitmq.start()

LOGGER.info('test blabla')
example.start_consuming('vm_delete', on_message)
example.start_consuming('vm_create', on_message)


example.on_bindok = on_reconnect