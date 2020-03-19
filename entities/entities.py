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

class ActiveCheckin:
    def __init__(self, item):
        self.item = item
        self.CardReaderID = int(item.get('CardReaderID').get('N'))
        self.CheckinTime = item.get('CheckinTime').get('N')
        self.Student = Student(item.get('Student').get('M'))
        self.StudentID = item.get('StudentID').get('S')

    def __repr__(self):
        return json.dumps(self.to_json())

    def to_json(self):
        return {
            'CardReaderID': self.CardReaderID,
            'CheckinTime': self.CheckinTime,
            'Student': self.Student.to_json(),
            'StudentID': self.StudentID
        }

    def short_str(self):
        return '[{},{}]'.format(self.CardReaderID,self.Student.short_str())

    def short_rep(self):
        return [self.CardReaderID,self.Student.short_rep()]
