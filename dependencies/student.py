import json

class Student:
    def __init__(self, item):
        self.item = item
        self.Name = item.get('Name').get('S')
        self.StudentID = item.get('StudentID').get('S')
        self.CardID = item.get('CardID').get('S')

    def __repr__(self):
        return json.dumps(self.to_json())

    def to_json(self):
        return {
            'Name': self.Name,
            'StudentID': self.StudentID,
            'CardID': self.CardID
        }

    def short_str(self):
        return '"'+self.Name+'"'

    def short_rep(self):
        return self.Name
