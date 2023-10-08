from collections import UserDict
from datetime import datetime
import re
import pickle
from pathlib import Path
from time import sleep

class Field:
    def __init__(self, value):
        self.value = value


class Address(Field):
    def __init__(self,value):
        super().__init__(value)
        self.value = value

    def __format__(self, format_spec):
        return '{:^25}'.format(self.value)

    def __getitem__(self, item):
        return self.value

    def __len__(self):
        return len(self.value)


class Email(Field):
    def __init__(self, value):
        super().__init__(value)
        self.get_value = value

    def __format__(self, format_spec):
        return self.value

    @property
    def get_value(self):
        return self.value

    @get_value.setter
    def get_value(self, value):
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if re.fullmatch(regex, value):
            self.value = value
        else:
            raise Exception("Ви ввели не коректний e-mail")

class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        self.get_value = value

    def __format__(self, format_spec):
        return datetime.strftime(self.value, "%d.%m.%Y")

    @property
    def get_value(self):
        return self.value

    @get_value.setter
    def get_value(self, value):
        pattern = "\d\d.\d\d.\d{4}"
        if value == re.search(pattern, value).group():
            now_t = datetime.now()
            old_d = datetime.strptime(value, '%d.%m.%Y')
            diff_date = now_t - old_d
            if diff_date.days >= 0:
                self.value = datetime.strptime(value, "%d.%m.%Y")
            else:
                raise Exception("Дата не може бути у майбутньому!")
        else:
            raise Exception("Будь ласка введіть дату в форматі: 'dd.mm.YYYY'>")


class Name(Field):
    def __init__(self, value):
        super().__init__(value)
        self.get_value = value

    @property
    def get_value(self):
        return self.value

    @get_value.setter
    def get_value(self, value):
        if type(value) == str:
            self.value = value
        else:
            raise TypeError('Імʼя має бути текстом')


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.get_value = value

    @property
    def get_value(self):
        return self.value

    @get_value.setter
    def get_value(self, value):
        if value.isdigit():
            self.value = value
        else:
            raise Exception('Телефон не коректний')

    def __getitem__(self, item):
        return self.value


class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None, address: Address = None, email: Email = None):
        self.name = name
        self.phones = []
        self.birthday = birthday
        self.address = address
        self.email = email

        if phone:
            self.phones.append(phone)

    def add_phone(self, phone):
        new_phone = Phone(phone)
        if new_phone.value not in [ph.value for ph in self.phones]:
            self.phones.append(new_phone)

    def delete_phone(self, phone):
        for ph in self.phones:
            if phone == ph.value:
                self.phones.remove(ph)

    def change_phone(self, old_phone, new_phone):
        for ph in self.phones:
            if old_phone == ph.value:
                self.delete_phone(old_phone)
                self.add_phone(new_phone)

    def edit_birthday(self, new_birthday):
        self.birthday = Birthday(new_birthday)

    def edit_email(self, new_email):
        self.email = Email(new_email)

    def edit_address(self, new_address):
        self.address = Address(new_address)


    def days_to_birthday(self):
        today = datetime.now()
        birthday = self.birthday.value
        days_to_birthday = (birthday - today).days
        if days_to_birthday < 0:
            birthday = birthday.replace(year=today.year + 1)
            days_to_birthday = (birthday - today).days
            return days_to_birthday
        return days_to_birthday

    def __str__(self):
        return f"{self.name.value} {[ph.value for ph in self.phones]} {self.birthday.value.date()}"


class AddressBook(UserDict):
    file_name = 'AddressBook/my_addressBook.bin'
    path_file_name = Path(file_name)

    def save_address_book(self):
        with open(self.path_file_name, 'wb') as file:
            pickle.dump(self.data, file)

    def load_address_book(self):
        if not self.path_file_name.exists():
            return print("\nВаша адресна книга порожня")
        with open(self.path_file_name, 'rb') as file:
            self.data = pickle.load(file)
        return print('-----')

    def search(self, search_str: str):
        result_1 = '\n Результат пошуку :\n'
        result_2 = ''
        result_3 = '{:^15}|  {:^25} | {:^25} | {:^10} | {:^10}\n'.format('"NAME"', '"PHONE"', '"ADDRESS"', '"BIRTHDAY"', '"EMAIL"')
        first_run = 1
        for record_id, records in self.data.items():
            list_phones = [i.value for i in records.phones]
            try:
                phone_join = ','.join(list_phones)
            except:
                phone_join = list_phones[0]
            try:
                len(records.address)
            except:
                records.address = '----'
            try:
                '{:^10}'.format(records.address)
            except TypeError:
                records.address = '----'
            try:
                '{:^10}'.format(records.birthday)
            except TypeError:
                records.birthday = '----'
            try:
                '{:^10}'.format(records.email)
            except:
                records.email = '----'
            if search_str in self.data[record_id].phones or search_str in record_id and first_run == 1:
                result_2 = result_2 + result_1 + result_3 + '{:^15}:  {:^25} | {:^25} | {:^10} | {:^10} \n'.format(record_id, phone_join, records.address, records.birthday, records.email)
                # if len(phone_join) > 10 and len(records.address) > 17:
                #     result_2 = result_2 + result_1 + result_3 + '{:^10}:  {:^15} | {:^20} | {:^10} | {:^10} \n'.format(record_id, phone_join[:10] + "...",records.address[:17] + '...',records.birthday, records.email)
                # elif len(phone_join) > 10 and len(records.address) <= 17:
                #     result_2 = result_2 + result_1 + result_3  + '{:^10}:  {:^15} | {:^20} | {:^10} | {:^10} \n'.format(record_id, phone_join[:10] + "...",records.address[:17],records.birthday, records.email)
                # elif len(phone_join) <= 10 and len(records.address) > 17:
                #     result_2 = result_2 + result_1 + result_3  + '{:^10}:  {:^15} | {:^20} | {:^10} | {:^10} \n'.format(record_id, phone_join[:10],records.address[:17] + '...',records.birthday, records.email)
                # elif len(phone_join) <= 10 and len(records.address) <= 17:
                #     result_2 = result_2 + result_1 + result_3  + '{:^10}:  {:^15} | {:^20} | {:^10} | {:^10} \n'.format(record_id, phone_join[:10],records.address[:17],records.birthday, records.email)
                first_run += 1
            elif search_str in self.data[record_id].phones or search_str in record_id and first_run != 1:
                result_2 = result_2 + '{:^15}:  {:^25} | {:^25} | {:^10} | {:^10} \n'.format(record_id,phone_join,records.address,records.birthday,records.email)
                # if len(phone_join) > 10 and len(records.address) > 17:
                #     result_2 = result_2 + '{:^10}:  {:^15} | {:^20} | {:^10} | {:^10} \n'.format(record_id, phone_join[:10] + "...",records.address[:17] + '...',records.birthday, records.email)
                # elif len(phone_join) > 10 and len(records.address) <= 17:
                #     result_2 = result_2 + '{:^10}:  {:^15} | {:^20} | {:^10} | {:^10} \n'.format(record_id, phone_join[:10] + "...",records.address[:17],records.birthday, records.email)
                # elif len(phone_join) <= 10 and len(records.address) > 17:
                #     result_2 = result_2 + '{:^10}:  {:^15} | {:^20} | {:^10} | {:^10} \n'.format(record_id, phone_join[:10],records.address[:17] + '...',records.birthday, records.email)
                # elif len(phone_join) <= 10 and len(records.address) <= 17:
                #     result_2 = result_2 + '{:^10}:  {:^15} | {:^20} | {:^10} | {:^10} \n'.format(record_id, phone_join[:10],records.address[:17],records.birthday, records.email)
        if len(result_2) < 1:
            return print('Співпадінь не знайденно')
        else:
            return print(result_2)

    # def search(self, search_str: str):
    #     result_1 = '\n Результат пошуку :\n'
    #     result_2 = ''
    #     result_3 = '{:^10}|  {:^15} | {:^20} | {:^10} | {:^10}\n'.format('"NAME"', '"PHONE"', '"ADDRESS"', '"BIRTHDAY"', '"EMAIL"')
    #     first_run = 1
    #     for record_id, records in self.data.items():
    #         record_phone = records.phones
    #         record_email = records.email
    #         record_birthday = records.birthday
    #         record_address = records.address
    #         try:
    #             phone_join = ','.join(record_phone)
    #         except:
    #             phone_join = records.phones[0].value
    #         try:
    #             len(record_address)
    #         except:
    #             record_address = '----'
    #         try:
    #             '{:^10}'.format(record_address)
    #         except TypeError:
    #             record_address = '----'
    #         try:
    #             '{:^10}'.format(record_birthday)
    #         except TypeError:
    #             record_birthday = '----'
    #         try:
    #             '{:^10}'.format(record_email)
    #         except:
    #             record_email = '----'
    #         if search_str in record_phone or search_str in record_id or search_str in record_address or search_str in record_email and first_run == 1:
    #             if len(phone_join) > 10 and len(record_address) > 17:
    #                 result_2 = result_2 + result_1 + result_3 + '{:^10}:  {:^15} | {:^20} | {:^10} | {:^10} \n'.format(record_id, phone_join[:10] + "...",record_address[:17] + '...',record_birthday, record_email)
    #             elif len(phone_join) > 10 and len(record_address) <= 17:
    #                 result_2 = result_2 + result_1 + result_3  + '{:^10}:  {:^15} | {:^20} | {:^10} | {:^10} \n'.format(record_id, phone_join[:10] + "...",record_address[:17],record_birthday, record_email)
    #             elif len(phone_join) <= 10 and len(record_address) > 17:
    #                 result_2 = result_2 + result_1 + result_3  + '{:^10}:  {:^15} | {:^20} | {:^10} | {:^10} \n'.format(record_id, phone_join[:10],record_address[:17] + '...',record_birthday, record_email)
    #             elif len(phone_join) <= 10 and len(record_address) <= 17:
    #                 result_2 = result_2 + result_1 + result_3  + '{:^10}:  {:^15} | {:^20} | {:^10} | {:^10} \n'.format(record_id, phone_join[:10],record_address[:17],record_birthday, record_email)
    #             first_run += 1
    #         elif search_str in record_phone or search_str in record_id or search_str in record_address or search_str in record_email and first_run != 1:
    #             if len(phone_join) > 10 and len(record_address) > 17:
    #                 result_2 = result_2 + '{:^10}:  {:^15} | {:^20} | {:^10} | {:^10} \n'.format(record_id, phone_join[:10] + "...",record_address[:17] + '...',record_birthday, record_email)
    #             elif len(phone_join) > 10 and len(record_address) <= 17:
    #                 result_2 = result_2 + '{:^10}:  {:^15} | {:^20} | {:^10} | {:^10} \n'.format(record_id, phone_join[:10] + "...",record_address[:17],record_birthday, record_email)
    #             elif len(phone_join) <= 10 and len(record_address) > 17:
    #                 result_2 = result_2 + '{:^10}:  {:^15} | {:^20} | {:^10} | {:^10} \n'.format(record_id, phone_join[:10],record_address[:17] + '...',record_birthday, record_email)
    #             elif len(phone_join) <= 10 and len(record_address) <= 17:
    #                 result_2 = result_2 + '{:^10}:  {:^15} | {:^20} | {:^10} | {:^10} \n'.format(record_id, phone_join[:10],record_address[:17],record_birthday, record_email)
    #     if len(result_2) < 1:
    #         return print('Співпадінь не знайденно')
    #     else:
    #         return print(result_2)

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def __str__(self):
        if len(self.data) > 0:
            output = '{:^15}|  {:^25} | {:^25} | {:^10} | {:^10}\n'.format('"NAME"', '"PHONE"', '"ADDRESS"', '"BIRTHDAY"', '"EMAIL"')
            for contact_name, show_content in self.data.items():
                list_phones = [i.value for i in show_content.phones]
                try:
                    join_phone = ','.join(list_phones)
                except:
                    join_phone = show_content.phones[0].value
                try:
                    len(str(show_content.address))
                except:
                    show_content.address = '----'
                try:
                    '{:^10}'.format(show_content.address)
                except TypeError:
                    show_content.address = '----'
                try:
                    '{:^10}'.format(show_content.birthday)
                except TypeError:
                    show_content.birthday = '----'
                try:
                    '{:^10}'.format(show_content.email)
                except:
                    show_content.email = '----'
                output = output + '{:^15}:  {:^25} | {:^25} | {:^10} | {:^10} \n'.format(contact_name, join_phone, show_content.address, show_content.birthday, show_content.email)
                # if len(join_phone) > 10 and len(show_content.address) > 17:
                #     output = output + '{:^10}:  {:^15} | {:^20} | {:^10} | {:^10} \n'.format(contact_name,join_phone[:10] + "...",show_content.address[:17] + '...',show_content.birthday, show_content.email)
                # elif len(join_phone) > 10 and len(show_content.address) <= 17:
                #     output = output + '{:^10}:  {:^15} | {:^20} | {:^10} | {:^10} \n'.format(contact_name,join_phone[:10] + "...",show_content.address[:17],show_content.birthday, show_content.email)
                # elif len(join_phone) <= 10 and len(show_content.address) > 17:
                #     output = output + '{:^10}:  {:^15} | {:^20} | {:^10} | {:^10} \n'.format(contact_name, join_phone[:10],show_content.address[:17] + '...',show_content.birthday, show_content.email)
                # elif len(join_phone) <= 10 and len(show_content.address) <= 17:
                #     output = output + '{:^10}:  {:^15} | {:^20} | {:^10} | {:^10} \n'.format(contact_name, join_phone[:10],show_content.address[:17],show_content.birthday, show_content.email)
            return output
        else:
            output = '{:^10}:  {:^25} | {:^25} | {:^10} | {:^10}\n'.format('"NAME"', '"PHONE"', '"ADDRESS"', '"BIRTHDAY"', '"EMAIL"')
            output = output + '{:^50}'.format('Ваша адресна книга порожня')
            return output


def input_phones():
    while True:
        phones_input = input('Введіть номер телефону (лише один) : ')
        try:
            phone_1 = Phone(phones_input.strip()
                            .replace("+", "")
                            .replace("(", "")
                            .replace(")", "")
                            .replace("-", "")
                            .replace(" ", "")
                            )
        except:
            print('Помилка вводу нома. Спробуйте ще раз')
            sleep(1)
            continue
        return phone_1


def input_email():
    while True:
        email_input = input('\nДля завершення запису введіть 0. Для завершення створення контакту натисніть ENTER\n Введіть e-mail адрессу : ')
        if email_input.strip() == '0':
            return 0
        elif email_input.strip() == "":
            return None
        else:
            try:
                email = Email(email_input.strip())
            except:
                print('Ви ввели некорректний email. Спробуйте ще раз')
                sleep(1)
                continue
            return email


def input_birthday():
    while True:
        birthday_input = input(
            '\nДля завершення запису введіть 0. Для завершення створення контакту натисніть ENTER\n Введіть дату народження (dd.mm.YYYY) : ')
        if birthday_input.strip() == '0':
            return 0
        elif birthday_input.strip() == "":
            return None
        else:
            try:
                birthday = Birthday(birthday_input.strip())
            except:
                print('Ви ввели некорректну дату народження. Спробуйте ще раз')
                sleep(1)
                continue
            return birthday


def input_address():
    while True:
        address_input = input(
            '\nДля завершення запису введіть 0. Для завершення створення контакту натисніть ENTER\n Введіть адресу : ')
        if address_input.strip() == '0':
            return 0
        elif address_input.strip() == "":
            return None
        else:
            try:
                address = Address(address_input.strip())
            except:
                print('Ви ввели некорректну адрессу. Спробуйте ще раз')
                sleep(1)
                continue
            return address


def create_contact(address_class: AddressBook):
    back_button = '\nДля повернення в попередне меню введіть 0'
    while True:
        input_name = input(f"{back_button}\nВведіть ім'я контакту: ")
        if input_name == '0':
            break
        else:
            if input_name not in address_class.data.keys():
                if input_name.strip() != '' and input_name not in address_class.data.keys():
                    name = Name(input_name)
                    phone = input_phones()
                    e_mail = input_email()
                    if e_mail != 0:
                        d_birthday = input_birthday()
                        if d_birthday != 0:
                            address = input_address()
                            if address != 0:
                                contact = Record(name,phone,d_birthday,address,e_mail)
                                address_class.add_record(contact)
                                break
                            elif address == 0:
                                address = None
                                contact = Record(name, phone, d_birthday, address, e_mail)
                                address_class.add_record(contact)
                                break
                        elif d_birthday == 0:
                            address = None
                            d_birthday = None
                            contact = Record(name, phone, d_birthday, address, e_mail)
                            address_class.add_record(contact)
                            break
                    elif e_mail == 0:
                        e_mail = None
                        address = None
                        d_birthday = None
                        contact = Record(name, phone, d_birthday, address, e_mail)
                        address_class.add_record(contact)
                        break

                    print('\nЗапис додано')
                    sleep(1)

                else:
                    print("\nІм'я повинно складатися хоча б з одного символа")
                    sleep(1)
            else:
                print("\nКонтакт з таким імʼям вже є...")
    print('\nКонтакт додано')
    address_class.save_address_book()
    sleep(1)


def delete_contact(addressBook: AddressBook):
    while True:
        input_chat_id_for_delete = input("\nВведіть Імя  контакту який хочете видалити або для повернення введіть 0 : ")
        if input_chat_id_for_delete != '0':
            try:
                del addressBook.data[input_chat_id_for_delete]
            except:
                print('\nВведіть корректний ID нотатку')

            print('\nContact видаленно ')
            addressBook.save_address_book()
            sleep(1)
            break
        else:
            break


def search(addressBook: AddressBook):
    search_mark = True
    while search_mark:
        input_for_search = input('\nДля повернення в попередне меню введіть 0\nВведіть слово обо текст для пошуку : ')
        if input_for_search == '':
            print('\n Запит на пошук повинен складатися хоча б з одного символа')
            sleep(1)
            continue
        elif input_for_search == '0':
            break
        else:
            addressBook.search(input_for_search)
            while True:
                print(''' 
            --  Введить "1" - Пошук по іншому запиту
            --  Введите "0" - Для повернення в попереднє меню"
            ''')
                input_for_search_choice = input('\nВиберіть дію : ')
                if input_for_search_choice not in ['1', '0']:
                    print('\nВиберіть дію зі списка')
                    sleep(1)
                    continue
                elif input_for_search_choice == '1':
                    break
                else:
                    search_mark = False
                    break


def edit_mode(addressbook: AddressBook):
    while True:
        input_chose_id_for_edit = input(
            '\n --  Введить "0" - Для повернення у попереднє меню\nВведіть ім"я контакту яких хочете редагувати : ')
        if input_chose_id_for_edit != '0':
            try:
                addressbook.data[input_chose_id_for_edit]
            except:
                print('Такого імені не існує у Ваших контактах')
                sleep(1)
                continue
            edit_contact(addressbook, input_chose_id_for_edit)
            break
        else:
            break


def edit_contact(addressbook: AddressBook, input_chose_id_for_edit):
    address_book_menu_3 = (''' 
                            --  Введить "1" - Додати номер          
                            --  Введить "2" - Змінити номер          
                            --  Введить "3" - Змінити адрессу
                            --  Введить "4" - Змінити email       
                            --  Введить "5" - Змінити дату народження       

                                            --  Введить "0" - Для повернення у попереднє меню''')
    while True:
        print(address_book_menu_3)
        input_content_for_edit = input('\nВведіть номер бажанної дії : ')
        if input_content_for_edit not in ['1', '2', '3', '4', '0']:
            print('\n Помилка вводу, будь ласка, введіть номер зі списку')
            sleep(2)
            continue
        elif input_content_for_edit == '1':
            while True:
                input_add_number = input('Введіть новий номер : ')
                try:
                    addressbook[input_chose_id_for_edit].add_phone(input_add_number)
                except:
                    'Введіть корректний номер '
                    continue
                print('Номер додано')
                break
        elif input_content_for_edit == '2':
            while True:
                input_change_number = input('Введіть номер який хочете змінити або 0 для повернення: ')
                addressbook_phone = addressbook[input_chose_id_for_edit].phones
                address_phone_list = [i.value for i in addressbook[input_chose_id_for_edit].phones]

                if input_change_number in address_phone_list:
                    while True:
                        input_new_number = input(' Введіть новий номер : ')
                        try:
                            addressbook[input_chose_id_for_edit].change_phone(input_change_number, input_new_number)
                        except:
                            'Введіть корректний номер '
                            continue
                        print('Номер зміненно')
                        break
                    break
                elif input_change_number == "0":
                    break
        elif input_content_for_edit == '3':
            while True:
                input_new_address = input('Введіть нову адрессу : ')
                try:
                    addressbook[input_chose_id_for_edit].edit_address(input_new_address)
                except:
                    'Введіть корректний номер '
                    continue
                print('Адрессу зміненно ')
                break
        elif input_content_for_edit == '4':
            while True:
                input_new_email = input('Введіть новий email : ')
                try:
                    addressbook[input_chose_id_for_edit].edit_email(input_new_email)
                except:
                    'Введіть корректний номер '
                    continue
                print('Email зміненно ')
                break
        elif input_content_for_edit == '5':
            while True:
                input_new_birthday = input('Введіть нову дату народження : ')
                try:
                    addressbook[input_chose_id_for_edit].edit_birthday(input_new_birthday)
                except:
                    'Введіть корректну дату народження'
                    continue
                print('Дату народження зміненно ')
                break
        elif input_content_for_edit == '0':
            break


def show_all_contact(addressBook: AddressBook):
    address_book_menu_2 = (''' 
                --  Введить "1" - Створити новий контакт          
                --  Введить "2" - Редагувати контакт          
                --  Введить "3" - Видилити контакт
                --  Введить "4" - Пошук        

                                --  Введить "0" - Для повернення у попереднє меню''')

    while True:
        print(addressBook)
        print(address_book_menu_2)
        input_todo_func = input('\nВведіть номер бажанної дії : ')
        if input_todo_func not in ['1', '2', '3', '4', '0']:
            print('\n Помилка вводу, будь ласка, введіть номер зі списку')
            sleep(2)
            continue
        elif input_todo_func == '1':
            create_contact(addressBook)
        elif input_todo_func == '2':
            edit_mode(addressBook)
        elif input_todo_func == '3':
            delete_contact(addressBook)
        elif input_todo_func == '4':
            search(addressBook)
        elif input_todo_func == '0':
            break




def main():
    address_book_menu_1 = ''' 
                --  Введить "1" - Додати контакт
                --  Введить "2" - Показати контакти
                --  Введите "3" - Пошук
                --  Введите "0" - Вийти з програми 'Андресна Книга' та зберегти данні
                '''
    address_book = AddressBook()
    address_book.load_address_book()
    # print(address_book)
    while True:
        print(''' 
            -- Вітаємо у застосунку 'Адресна Книга' --
                                    ''')
        print(address_book_menu_1)
        first_choose = input('Оберіть дію зі списка : ')
        if first_choose == '1':
            create_contact(address_book)
            continue
        elif first_choose == '2':
            show_all_contact(address_book)
        elif first_choose == '3':
            search(address_book)
        elif first_choose == '0':
            address_book.save_address_book()
            print('Допобачення ')
            sleep(1)
            break
        else:
            print('Помилка вводу, спробуйте знову')
            sleep(2)


if __name__ == '__main__':
    main()