from collections import UserDict
import re
from datetime import datetime, timedelta 
from dataclasses import dataclass, field

@dataclass
class Field:
    value: str

    def __str__(self):
        return self.value

@dataclass    
class Name(Field):
    pass

@dataclass 
class Phone(Field):
    def __post_init__(self):
        if not re.match(r"^\d{10}$", self.value):
            raise ValueError("Invalid phone number format. Must be 10 digits")

@dataclass 
class Birthday(Field):
    def __post_init__(self):
        try:
            datetime.strptime(self.value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
            
@dataclass 
class Record:
        name: Name
        phone: list[Phone] = field(default_factory=list)
        birthday: Birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.pnones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                return
        
        raise ValueError("Phone number not found")
    
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p.value
        
        return None
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def show_birthday(self):
        if self.birthday:
            return self.birthday.value
        return None
    
    def __str__(self):
        phones_str = ";".join(p.value for p in self.phones)
        birthday_str = f", birthday: {self.birthday.value}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones_str}{birthday_str}"
    
class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
    
    def find(self, name):
        return self.data.get(name)
    
    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError("Record not found")
    
    def get_upcoming_birthday(self) -> str:
         today = datetime.today().date()
         next_week = today + timedelta(days=7)
         birthdays_per_week = {i:[] for i in range(5)}

         for record in self.data.values():
              if record.birthday:
                   birthday_date = record.birthday.value.replace(year=today.year)
                   if today <= birthday_date <= next_week:
                        day_of_week = birthday_date.weekday()
                        if day_of_week >= 5:
                             day_of_week = 0
                        birthdays_per_week[day_of_week].append(record.name.value)






# book = AddressBook()
# john_record = Record("John")
# john_record.add_phone("1234567890")
# john_record.add_phone("5555555555")
# book.add_record(john_record)
# jane_record = Record("Jane")
# jane_record.add_phone("9876543210")
# book.add_record(jane_record)

# for name, record in book.data.items():
#     print(record)

# john = book.find("John")
# john.edit_phone("1234567890", "1112223333")

# print(john)

# found_phone = john.find_phone("5555555555")
# print(f"{john.name}: {found_phone}")

# book.delete("Jane")

# print(book.data)