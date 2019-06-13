import pika
from loguru import logger
from CleanUpData import CleanData

class RunIt():
    def __init__(self):
        pass

    @property
    def StartUp(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        # self.result = 0
        channel = connection.channel()
        channel_name = channel.queue_declare(queue='rtl-433')
        method_frame, header_frame, body = channel.basic_get(queue='rtl-433')
        # logger.info("Data: " + str(method_frame) + "Header: " + str(header_frame) + "Body: " + str(body))
        try:
            if method_frame.NAME == 'Basic.GetEmpty':
                logger.warning("No Data In Queue")
                # print("Closed")
                connection.close()
                return('Empty')
            else:
                # logger.warning("Data Coming In ")
                channel.basic_ack(delivery_tag=method_frame.delivery_tag)
                message : dict = CleanData.massageData(self, body)
                # logger.info("Message: " + str(message) + str(type(message)))
                connection.close()
                return(message) # as a dictionary
        except Exception as e:
            z = ("Error " + str(e))
            y = ("Data: " + str(method_frame) + "Header: " + str(header_frame) + "Body: " + str(body))
            return({z, y})

        # channel.basic_consume(callback, queue='rtl-433', no_ack=True)

        # logger.info("MQ Queue: " + str(channel_name.method.message_count))

        # print(' [*] Waiting for messages. To exit press CTRL+C')
        # channel.start_consuming()
        # return (message)  # as a dictionary

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
    z = z.StartUp
    # print(z)

if __name__ == '__main__':
    main()

