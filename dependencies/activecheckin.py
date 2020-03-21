import json
from student import Student

class ActiveCheckin:
    def __init__(self, item):
        self.item = item
        self.CardReaderID = int(item.get('CardReaderID').get('N'))
        self.CheckinTime = int(item.get('CheckinTime').get('N'))
        self.Student = Student(item.get('Student').get('M'))
        self.CardID = item.get('CardID').get('S')

    def __repr__(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            'CardReaderID': self.CardReaderID,
            'CheckinTime': self.CheckinTime,
            'Student': self.Student.to_dict(),
            'CardID': self.CardID
        }

    def to_json(self):
        return json.dumps({
            'CardReaderID': self.CardReaderID,
            'CheckinTime': self.CheckinTime,
            'Student': self.Student.to_dict(),
            'CardID': self.CardID
        })

    def short_str(self):
        return '[{},{}]'.format(self.CardReaderID,self.Student.short_str())

    def short_rep(self):
        return [self.CardReaderID,self.Student.short_rep()]
