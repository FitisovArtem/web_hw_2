import AddressBook.main as ab
import Notes.main as note
import Sorter.sorter as sorter
import Weather.weather as weather
import Game.game as g
from time import sleep

STOP_COMMAND = ["exit"]
MAIN_MENU = ["1", "2", "3", "4", "5"]


def input_error(func):
    def inner(*args, **kwargs):
        print('''Вас вітає, Almost_iPhone! 

    Я можу вам допомогти організувати ваші контакти за допомогою "Книгу контактів"
    або зберегти будь яку інформацію в "Нотатки",
    якщо у Вас є папка в котрій необхідно навести порядок - скристуйтесь "Сортувальником",
    якщо стало нудно - пограйте в гру "Бандеро Гусь",
    і завжди не забудете парасольку бо погода в вас під руко
    можливо скоро в меня зʼявляться інші функції...''')
        sleep(2)
        while True:
            print(''' 
        --  Введіть "1" - Ви відкриєте додаток "Книга контактів"
        --  Введіть "2" - Ви відкриєте додаток "Нотатки"
        --  Введіть "3" - Ви відкриєте додаток "Сортировальик"
        --  Введіть "4" - Ви зможете насолодись грою "Бандеро Гусь"
        --  Введіть "5" - Ви зможете дізнатись поточну погоду"
        --  Введіть "exit" - І я завершу свою роботу
        ''')

            try:
                func()
            except SystemExit:
                break
            except Exception as e:
                print("Вибачте, сталося помилка", e)

    return inner


@input_error
def main():
    result = input("Введіть цифру и я запущу відповідний додаток: ")
    if len(result) == 0:
        print("Ви нічого не ввели, спробуйте ввести цифру.")

    elif result in STOP_COMMAND:
        print("Повертайтеся пізніше, я зможу допомогти Вам!")
        raise SystemExit

    elif not result.isnumeric():
        print("Ви ввели не додатне число, введіть одну цифру!")

    elif result in MAIN_MENU:
        if result == "1":
            ab.main()
        elif result == "2":
            try:
                note.main_1()
            except:
                print(Exception.args[0])
        elif result == "3":
            try:
                sorter.run()
            except:
                print(Exception.args[0])
        elif result == "4":
            print("In future...")
            # try:
            #     score = g.main()
            #     if score > 0:
            #         print(f"Вау, ваш рахунок: {score}")
            #     else:
            #         print("Потренуйтесь і у Вас все вийде.")
            # except:
            #     print(Exception.args[0])

        elif result == "5":
            try:
                weather.weather_main()
                sleep(2)
            except:
                print(Exception.args[0])
        else:
            print("Oops...")

    else:
        print("У Вас вийде, спробуйте ввести цифру від 1 до 4 включно")


main()
