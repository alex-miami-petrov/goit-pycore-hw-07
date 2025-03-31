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
    phones: list[Phone] = field(default_factory=list)
    birthday: Birthday = None

    def add_phone(self, phone_str: str):
        self.phones.append(Phone(phone_str))

    def remove_phone(self, phone):
        if self.phones:
            self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        if self.phones:
            for p in self.phones:
                if p.value == old_phone:
                    p.value = new_phone
                    return
            raise ValueError("Phone number not found")
        else:
            raise ValueError("No phone numbers to edit.")

    def find_phone(self, phone):
        if self.phones:
            for p in self.phones:
                if p.value == phone:
                    return p.value
        return None

    def add_birthday(self, birthday_str: str):
        self.birthday = Birthday(birthday_str)

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

    def get_upcoming_birthdays(self) -> str:
        today = datetime.today().date()
        next_week = today + timedelta(days=7)
        birthdays_per_week = {i: [] for i in range(5)}

        for record in self.data.values():
            if record.birthday:
                birthday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
                birthday_this_year = birthday_date.replace(year=today.year)
                if today <= birthday_this_year <= next_week:
                    day_of_week = birthday_this_year.weekday()
                    if day_of_week >= 5:
                        day_of_week = 0
                    birthdays_per_week[day_of_week].append(record.name.value)

        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        return "\n".join(f"{days_of_week[i]}: {', '.join(names)}"
                        for i, names in birthdays_per_week.items() if names)






