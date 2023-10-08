from collections import UserDict
from datetime import datetime
# import json
import pickle
from pathlib import Path
from time import sleep


class Note:

    """
    Класс Note использует для обработки текста и тегов к
    тексту для дальнейшей записи в заметки.
    """

    def __init__(self, content: str, tags: str):  # Инициализация текста заметки и тега для дальнейшей обработки
        self.content = content
        self.tags = tags.split(',')
        self.tags = sorted(self.tags)
        self.date = datetime.now().strftime('%d/%m/%Y %H:%M:%S')


class NotesManager(UserDict):
    file_name = 'Notes/my_notes2.bin'
    path_file_name = Path(file_name)

    def save_notes(self):
        with open(self.path_file_name, 'wb') as file:
            pickle.dump(self.data, file)

    def load_notes(self):
        if not self.path_file_name.exists():
            return print("File is empty")
        with open(self.path_file_name, 'rb') as file:
            self.data = pickle.load(file)

    def add_note(self, note: Note):
        self.data[len(self.data) + 1] = note

    def delete_note(self, chosen_id):
        del self.data[chosen_id]
        # if chosen_id < len(self.data):
        for i in range(int(chosen_id), len(self.data) + 1):
            self.data[i] = self.data[i + 1]
            del self.data[i + 1]

    def search_note(self, tag_for_search):
        title_of_result = f'Результати пошуку по запиту "{tag_for_search}" : \n'
        result = '\n'
        if tag_for_search is not None:
            for search_id, content_set in self.data.items():
                if tag_for_search in content_set.tags or tag_for_search in content_set.content:
                    result = result + f'{search_id}: {content_set.content}\n'
            if len(result) > 2:
                print(title_of_result)
                print(result)
            else:
                print('\n По Вашому запиту не знайдено нотатків')
                sleep(1)
                return '0 результатів'

    def sorted_notes(self):
        dict_sorted = {}
        result = '{:^10}:  {:^15} | {:^20} | {:^10}\n'.format('"ID"', '"TAGS"', '"NOTE"', '"DATE"')
        for chat_id, notes_class in self.data.items():
            dict_sorted[notes_class.date] = [chat_id, notes_class.content, notes_class.tags]
        a_dict = dict(sorted(dict_sorted.items(), reverse=True))
        for dict_1, in_dict in a_dict.items():
            join_tags = ','.join(in_dict[2])
            if len(join_tags) > 10 and len(in_dict[1]) > 20:
                result = result + '{:^10}:  {:^15} | {:<20} | {:>10} \n'.format(in_dict[0], join_tags[:10] + "...",
                                                                                in_dict[1][:17] + '...', dict_1)
            elif len(join_tags) > 10 and len(in_dict[1]) <= 20:
                result = result + '{:^10}:  {:^15} | {:<20} | {:>10} \n'.format(in_dict[0], join_tags[:10] + "...",
                                                                                in_dict[1][:17], dict_1)
            elif len(join_tags) <= 10 and len(in_dict[1]) > 20:
                result = result + '{:^10}:  {:^15} | {:<20} | {:>10} \n'.format(in_dict[0], join_tags[:10],
                                                                                in_dict[1][:17] + '...', dict_1)
            elif len(join_tags) <= 10 and len(in_dict[1]) <= 20:
                result = result + '{:^10}:  {:^15} | {:<20} | {:>10} \n'.format(in_dict[0], join_tags[:10],
                                                                                in_dict[1][:17], dict_1)
        return result

    def edit_note(self, new_content, chosen_id_for_edit):
        self.data[chosen_id_for_edit].content = new_content

    def show_note(self, chosen_id):
        output_string = f'\n Дата створення : {self.data[chosen_id].date}\n Теги : {",".join(self.data[chosen_id].tags)}\n\n'
        length_content = len(self.data[chosen_id].content)
        count_lines = length_content // 40
        last_line_counter = length_content % 40
        stop_output_index = 40
        start_output_index = 0
        if count_lines == 0:
            output_string = self.data[chosen_id].content
        elif count_lines > 0 and last_line_counter == 0:
            for i in range(count_lines + 1):
                output_string = output_string + self.data[chosen_id].content[
                                                start_output_index:stop_output_index] + '\n'
                start_output_index += 40
                stop_output_index += 40
        elif count_lines > 0 and last_line_counter != 0:
            for i in range(count_lines + 2):
                output_string = output_string + self.data[chosen_id].content[
                                                start_output_index:stop_output_index] + '\n'
                start_output_index += 40
                stop_output_index += 40
        print(output_string)

    def __str__(self):
        if len(self.data) > 0:
            output = '{:^10}:  {:^15} | {:^20} | {:^10}\n'.format('"ID"', '"TAGS"', '"NOTE"', '"DATE"')
            for id_number, show_content in self.data.items():
                join_content = ','.join(show_content.tags)
                if len(join_content) > 10 and len(show_content.content) > 17:
                    output = output + '{:^10}:  {:^15} | {:<20} | {:>10} \n'.format(id_number,
                                                                                    join_content[:10] + "...",
                                                                                    show_content.content[:17] + '...',
                                                                                    show_content.date)
                elif len(join_content) > 10 and len(show_content.content) <= 17:
                    output = output + '{:^10}:  {:^15} | {:<20} | {:>10} \n'.format(id_number,
                                                                                    join_content[:10] + "...",
                                                                                    show_content.content[:17],
                                                                                    show_content.date)
                elif len(join_content) <= 10 and len(show_content.content) > 17:
                    output = output + '{:^10}:  {:^15} | {:<20} | {:>10} \n'.format(id_number, join_content[:10],
                                                                                    show_content.content[:17] + '...',
                                                                                    show_content.date)
                elif len(join_content) <= 10 and len(show_content.content) <= 17:
                    output = output + '{:^10}:  {:^15} | {:<20} | {:>10} \n'.format(id_number, join_content[:10],
                                                                                    show_content.content[:17],
                                                                                    show_content.date)
            return output
        else:
            return "Ваш нотатник немає записів"


def search_notes(notesBook: NotesManager):
    back_button = 'Для повернення в попередне меню введіть 0'
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
            notesBook.search_note(input_for_search)
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


def create_note(notesBook: NotesManager):
    back_button = '\nДля повернення в попередне меню введіть 0'
    while True:
        input_note = input(f'{back_button}\nВведіть текст для нотатку : ')
        if input_note == '0':
            break
        else:
            if input_note.strip() != '':
                input_tag = input('Введіть теги для нотатку через запятую (Теги не обовязкові) : ')
                note = Note(input_note, input_tag)
                notesBook.add_note(note)
                print('\nЗапис додано')
                notesBook.save_notes()
                sleep(2)
                break
            else:
                print('\nНотаток повинен мати хоча б один символ. Повторіть ввод')
                sleep(3)


def show_all_notes(notesBook: NotesManager):
    note_menu_2 = (''' 
            --  Введить "1" - Створити новий нотаток   --  Введить "4" - Видилити нотаток          
            --  Введить "2" - Відкрити нотаток         --  Введить "5" - Пошук         
            --  Введить "3" - Редагувати нотаток       --  Введить "6" - Сортування по даті ↑

                            --  Введить "0" - Для повернення у попереднє меню''')

    note_menu_22 = (''' 
            --  Введить "1" - Створити новий нотаток   --  Введить "4" - Видилити нотаток          
            --  Введить "2" - Відкрити нотаток         --  Введить "5" - Пошук         
            --  Введить "3" - Редагувати нотаток       --  Введить "6" - Сортування по даті ↓

                            --  Введить "0" - Для повернення у попереднє меню''')


    type_show = 'A'
    while True:
        if type_show == 'A':
            print(notesBook)
            print(note_menu_2)
            input_todo_func = input('\nВведіть номер бажанної дії : ')
            if input_todo_func not in ['1', '2', '3', '4', '0', '5', '6']:
                print('\n Помилка вводу, будь ласка, введіть номер зі списку')
                sleep(2)
                continue
            elif input_todo_func == '1':
                create_note(notesBook)
            elif input_todo_func == '2':
                show_note(notesBook)
            elif input_todo_func == '3':
                edit_mode_note(notesBook)
            elif input_todo_func == '4':
                delete_note(notesBook)
            elif input_todo_func == '5':
                search_notes(notesBook)
            elif input_todo_func == '6':
                notesBook.sorted_notes()
                type_show = 'B'
                continue
            elif input_todo_func == '0':
                break
        else:
            print(notesBook.sorted_notes())
            print(note_menu_22)
            input_todo_func = input('\nВведіть номер дії зі списку : ')
            if input_todo_func not in ['1', '2', '3', '4', '0', '5', '6']:
                print('\n Помилка вводу, будь ласка, введіть номер зі списку')
                sleep(2)
                continue
            elif input_todo_func == '1':
                create_note(notesBook)
            elif input_todo_func == '2':
                show_note(notesBook)
            elif input_todo_func == '3':
                edit_mode_note(notesBook)
            elif input_todo_func == '4':
                delete_note(notesBook)
            elif input_todo_func == '5':
                search_notes(notesBook)
            elif input_todo_func == '6':
                notesBook.sorted_notes()
                type_show = 'A'
                continue
            elif input_todo_func == '0':
                break


def show_note(notesBook: NotesManager):
    note_menu_3 = ''' 
            --  Введить "1" - Редагувати нотаток
            --  Введите "2" - Видалити нотаток
            --  Введите "0" - Для повернення в попереднє меню"
            '''

    while True:
        input_chat_id = input("\nВведіть ID нотатку : ")
        if input_chat_id == '0':
            break
        else:
            try:
                notesBook.show_note(int(input_chat_id))
            except:
                print('\nВведіть існуючий ID')
                continue
            while True:
                print(note_menu_3)
                ink = input('Введіть дію зі списка')
                if ink not in ['1', '2', '0']:
                    print('\nВведіть корректну дію зі списка')
                    sleep(1)
                elif ink == '1':
                    edit_note(notesBook, input_chat_id)
                elif ink == '2':
                    notesBook.delete_note(int(input_chat_id))
                    print('\nНотаток видаленно ')
                    notesBook.save_notes()
                    sleep(1)
                    break
                elif ink == '0':
                    break
            break


def edit_mode_note(notesBook: NotesManager):
    while True:
        input_chose_id_for_edit = input(
            '\n --  Введить "0" - Для повернення у попереднє меню\nВведіть номер нотатку яких хочете редагувати : ')
        if input_chose_id_for_edit != '0':
            try:
                notesBook.data[int(input_chose_id_for_edit)]
            except:
                print('Введіть корректний ID нотатку')
                sleep(1)
                continue
            edit_note(notesBook, input_chose_id_for_edit)
            break
        else:
            break


def edit_note(notesBook: NotesManager, input_chose_id_for_edit):
    while True:
        input_content_for_edit = input(' \nВедіть новий текст нотатку :')
        if input_content_for_edit == '':
            print('\nНотаток не може бути пустим')
            sleep(1)
            continue
        else:
            notesBook.edit_note(input_content_for_edit, int(input_chose_id_for_edit))
            print('\nНотаток зміненний та збереженний')
            notesBook.save_notes()
            sleep(1)
            break


def delete_note(notesBook: NotesManager):
    while True:
        input_chat_id_for_delete = input("\nВведіть ID нотатку : ")
        if input_chat_id_for_delete != '0':
            try:
                notesBook.delete_note(int(input_chat_id_for_delete))

            except:
                print('\nВведіть корректний ID нотатку')

            print('\nНотаток видаленно ')
            notesBook.save_notes()
            sleep(1)
            break
        else:
            break


def main_1():
    note_menu_1 = ''' 
            --  Введить "1" - Створити нотаток
            --  Введите "2" - Показати усі нотатки
            --  Введите "0" - Вийти з програми 'Нотатки' та зберегти данні
            '''

    notesBook = NotesManager()
    notesBook.load_notes()
    while True:
        print(''' 
            -- Вітаємо у застосунку 'Нотатки' --
                                    ''')
        print(note_menu_1)
        first_choose = input('Оберіть дію зі списка : ')
        if first_choose == '1':
            create_note(notesBook)

        elif first_choose == '2':
            show_all_notes(notesBook)
        elif first_choose == '3':
            notesBook.sorted_notes()
        elif first_choose == '0':
            notesBook.save_notes()
            print('Bye')
            sleep(2)
            break
        else:
            print('Помилка вводу, спробуйте знову')
            sleep(2)


if __name__ == "__main__":
    main_1()
