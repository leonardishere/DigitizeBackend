import json
from student import Student

class InactiveCheckin:
    def __init__(self, item):
        self.item = item
        self.StudentID = item.get('StudentID').get('S')
        self.CheckinTime = int(item.get('CheckinTime').get('N'))
        self.CheckoutTime = int(item.get('CheckoutTime').get('N'))
        self.Student = Student(item.get('Student').get('M'))
        self.CardReaderID = int(item.get('CardReaderID').get('N'))

    def __repr__(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            'StudentID': self.StudentID,
            'CheckinTime': self.CheckinTime,
            'CheckoutTime': self.CheckoutTime,
            'Student': self.Student.to_dict(),
            'CardReaderID': self.CardReaderID,
        }

    def to_json(self):
        return json.dumps({
            'StudentID': self.StudentID,
            'CheckinTime': self.CheckinTime,
            'CheckoutTime': self.CheckoutTime,
            'Student': self.Student.to_dict(),
            'CardReaderID': self.CardReaderID,
        })
