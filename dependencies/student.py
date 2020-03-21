import json

general_notice = 'Required attributes: Name(string), StudentID(string), CardID(string).'
null_notice = 'Could not construct Student: item does not exist. ' + general_notice
missing_notice = 'Could not construct Student: missing attributes. ' + general_notice
req_atts = ['Name', 'StudentID', 'CardID']
type_atts = {'Name': 'S', 'StudentID': 'S', 'CardID': 'S'}

class Student:
    def __init__(self, item):
        print('item:', item)
        self.item = item
        if item is None:
            raise Exception(null_notice)
        for att in req_atts:
            if att not in item:
                raise Exception(missing_notice)
        self.Name = item.get('Name')
        if isinstance(self.Name,dict):
            self.Name = self.Name.get('S')
        self.StudentID = item.get('StudentID')
        if isinstance(self.StudentID,dict):
            self.StudentID = self.StudentID.get('S')
        self.CardID = item.get('CardID')
        if isinstance(self.CardID,dict):
            self.CardID = self.CardID.get('S')

    def __repr__(self):
        return json.dumps(self.to_dict())

    def to_json(self):
        return json.dumps({
            'Name': self.Name,
            'StudentID': self.StudentID,
            'CardID': self.CardID
        })

    def to_dict(self):
        return {
            'Name': self.Name,
            'StudentID': self.StudentID,
            'CardID': self.CardID
        }

    def short_str(self):
        return '"'+self.Name+'"'

    def short_rep(self):
        return self.Name
