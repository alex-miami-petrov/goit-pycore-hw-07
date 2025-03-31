from address_book import AddressBook, Record, Name, Phone, Birthday

def validate_contact_args(args: list) -> str:
    if len(args) != 2:
        return "Invalid command. Usage: add [ім'я] [номер телефону] або change [ім'я] [старий номер] [новий номер]"
    try:
        name, phone = args
        if not phone.isdigit():
            return "Invalid phone number. Phone number must contain only 10 digits. Example: add John 1234567890"
    except ValueError:
        return "Invalid command. Usage: add [ім'я] [номер телефону] або change [ім'я] [старий номер] [новий номер]"
    return None

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError:
            return "Contact not found"
        except IndexError:
            return "Invalid command. Usage: [command] [ім'я] [номер телефону]"
    return inner

@input_error
def add_contact(args: list, book: AddressBook) -> str:
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(Name(name))
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args: list, book: AddressBook) -> str:
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Contact updated."
    else:
        raise KeyError

@input_error
def show_phone(args: list, book: AddressBook) -> str:
    name, *_ = args
    record = book.find(name)
    if record:
        return "; ".join(str(p.value) for p in record.phones)
    else:
        raise KeyError

@input_error
def show_all(book: AddressBook) -> str:
    if not book.data:
        return "No contacts saved."
    else:
        return "\n".join(str(record) for record in book.data.values())

@input_error
def add_birthday(args: list, book: AddressBook) -> str:
    name, birthday, *_ = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    else:
        raise KeyError

@input_error
def show_birthday(args: list, book: AddressBook) -> str:
    name, *_ = args
    record = book.find(name)
    if record and record.birthday:
        return record.show_birthday()
    else:
        raise KeyError

@input_error
def birthdays(args: list, book: AddressBook) -> str:
    return book.get_upcoming_birthdays()
    







