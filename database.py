import json

class Database:
  def __init__(self, path='db.json'):
    self.path: str = path

  def save(self, data: dict):
    with open(self.path, 'w') as file:
      file.write(json.dumps(data, indent=2))

  def load(self) -> dict:
    with open(self.path, 'r') as file:
      return json.loads(file.read())

  def set(self, key: str, value):
    data = self.load()
    data[key] = value
    self.save(data)
