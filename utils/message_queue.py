import pymongo
from aiogram import types
from data.config import HOST, PORT, DB_NAME,DB_MESSAGE

class MessageQueue:
    def __init__(self):
        self.client = pymongo.MongoClient(HOST, PORT)
        self.db = self.client.get_database(DB_NAME)
        self.queue_collection = self.db[DB_MESSAGE]

    async def add_message(self,
                          priority=0,
                          chat_id=None,
                          text=None,
                          reply_markup=None,
                          edit=None,
                          parse_mode=None,
                          delete_reply_markup=None,
                          message_id=None,
                          invoceOrder=None,
                          test=None,
                          photo_url=None):
        message = {'chat_id': chat_id,
                   'text': text,
                   'priority': priority,
                   "reply_markup": reply_markup,
                   "edit": edit,
                   "parse_mode": parse_mode,
                   "delete_reply_markup": delete_reply_markup,
                   "message_id": message_id,
                   "invoceOrder": invoceOrder,
                   "test": test,
                   "photo_url": photo_url}
        self.queue_collection.insert_one(message)

    async def get_next_message(self):
        message = self.queue_collection.find_one_and_delete({}, sort=[('priority', -1)])
        return message
