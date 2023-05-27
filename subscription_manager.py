class Subscription:
  def __init__(self, db):
    self.subscriptions = {}
    self.db = db

  def is_subscribed(self, username):
    return username in self.subscriptions

  def subscribe(self, username, channel):
    self.subscriptions[username] = {
      'channel': channel, 
      'stream': []
    }

  def unsubscribe(self, username):
    del self.subscriptions[username]

  def dispatch(self, channel, message):
    for subscription in self.subscriptions:
      if self.subscriptions[subscription]['channel'] == channel:
        self.subscriptions[subscription]['stream'].append(message)

  def get_stream(self, username):
    # little bit of processing to ensure that the avatars are updated
    data = self.subscriptions[username]['stream']
    account_data = self.db.load()['accounts']
    for i, message in enumerate(data):
      if not isinstance(message['author'], dict):
        data[i]['author'] = {
          'avatar': account_data[message['author']]['avatar'],
          'username': message['author']
        }
    return data  

  def ack(self, username):
    self.subscriptions[username]['stream'] = []
