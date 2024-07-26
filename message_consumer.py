import asyncio

from utils.message_consumer import message_consumer
from utils.message_queue import MessageQueue

if __name__ == '__main__':
    message_queue = MessageQueue()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(message_consumer(message_queue))
