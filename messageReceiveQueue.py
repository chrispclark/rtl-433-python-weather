import pika
from loguru import logger
from CleanUpData import CleanData

class RunIt():
    def __init__(self):
        pass

    def StartUp(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.result = 0
        channel = connection.channel()
        channel_name = channel.queue_declare(queue='rtl-433')
        method_frame, header_frame, body = channel.basic_get(queue='rtl-433')
        logger.info("Data: " + str(method_frame), str(header_frame), str(body))
        try:
            if method_frame.NAME == 'Basic.GetEmpty':
                print("Closed")
                connection.close()
                return('Empty')
            else:
                print("Summit")
                channel.basic_ack(delivery_tag=method_frame.delivery_tag)
                message = CleanData.massageData(self, body)
                connection.close()
                return(message)
        except  Exception as e:
            print("Error creating pika blocking connection: " + str(e))
            return("Failed")
        
        def callback(ch, method, properties, body):
            if len(body) != 0:
                self.result = CleanData.massageData(self, body)
                logger.debug("Result: " + str(self.result))
                return(self.result)

        channel.basic_consume(callback, queue='rtl-433', no_ack=True)

        logger.info("MQ Queue: " + str(channel_name.method.message_count))

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

    def MessageCount(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel_name = channel.queue_declare(queue='rtl-433')
        connection.close()
        return(channel_name.method.message_count)


def main():
    z = RunIt()
    y = z.MessageCount()
    logger.info("MQ Queue: " + str(y))

if __name__ == '__main__':
    main()

