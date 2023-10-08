import re
from collections import UserDict
import sys
from pathlib import Path
import shutil
import os.path
import os

current_path = Path('.')


class Trans:  # класс створює словник відповідності символів латиниці та кирилиці
    cyrillic_symbol = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
    latin_symbol = (
    "a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
    "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")
    TRANS = {}

    def trans_dict(self):
        for c, l in zip(self.cyrillic_symbol, self.latin_symbol):
            self.TRANS[ord(c)] = l
            self.TRANS[ord(c.upper())] = l.upper()
        return self.TRANS


class Normalize(Trans):  # функція видаляє непотрібні символи з назви файлу
    def normalize(self, name: str):
        t_name = name.translate(self.TRANS)
        t_name = re.sub(r'[^a-zA-Z0-9.]', '_', t_name)
        return t_name


class Scan:  # сканування  папки та запис файлів в списки відповідних типиві
    JPEG_IMAGES = []
    JPG_IMAGES = []
    PNG_IMAGES = []
    SVG_IMAGES = []

    AVI_VIDEO = []
    MP4_VIDEO = []
    MOV_VIDEO = []
    MKV_VIDEO = []

    DOC_DOCUMENTS = []
    DOCX_DOCUMENTS = []
    TXT_DOCUMENTS = []
    PDF_DOCUMENTS = []
    XLSX_DOCUMENTS = []
    PPTX_DOCUMENTS = []

    MP3_AUDIO = []
    OGG_AUDIO = []
    WAV_AUDIO = []
    AMR_AUDIO = []

    ZIP_ARCHIVES = []
    GZ_ARCHIVES = []
    TAR_ARCHIVES = []

    FOLDERS = []
    MY_OTHER = []

    EXTENSION = set()
    UNKNOWN = set()

    REGISTER_EXTENSION = {
        'JPEG': JPEG_IMAGES, 'JPG': JPG_IMAGES, 'PNG': PNG_IMAGES, 'SVG': SVG_IMAGES,
        'MP3': MP3_AUDIO, 'OGG': OGG_AUDIO, 'WAV': WAV_AUDIO, 'AMR': AMR_AUDIO,
        'AVI': AVI_VIDEO, 'MP4': MP4_VIDEO, 'MOV': MOV_VIDEO, 'MKV': MKV_VIDEO,
        'DOC': DOC_DOCUMENTS, 'DOCX': DOCX_DOCUMENTS, 'TXT': TXT_DOCUMENTS, 'PDF': PDF_DOCUMENTS,
        'XLSX': XLSX_DOCUMENTS, 'PPTX': PPTX_DOCUMENTS,
        'ZIP': ZIP_ARCHIVES, 'GZ': GZ_ARCHIVES, 'TAR': TAR_ARCHIVES,
    }

    def get_extension(filename: str) -> str:
        return Path(filename).suffix[1:].upper()

    def scan(self, folder: Path) -> None:
        for item in folder.iterdir():
            if item.is_dir():
                if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'MY_OTHER'):
                    self.FOLDERS.append(item)
                    self.scan(item)
                continue

            ext = Scan.get_extension(item.name)
            fullname = folder / item.name
            if not ext:
                self.MY_OTHER.append(fullname)
            else:
                try:
                    container = self.REGISTER_EXTENSION[ext]
                    self.EXTENSION.add(ext)
                    container.append(fullname)
                except KeyError:
                    self.UNKNOWN.add(ext)
                    self.MY_OTHER.append(fullname)


class ReplaseFile(Normalize):  # перенесення файлів до папок які відповідають типу фйлу
    def __init__(self, folder: Path):
        self.folder = folder

    def input_error(input_func):
        def output_func(*args):
            try:
                result = input_func(*args)
                return result
            except KeyError:
                return "KeyError"
            except ValueError:
                return "ValueError"
            except IndexError:
                return "ndexError"
            except FileNotFoundError:
                return "FileNotFoundError"

        return output_func

    @input_error
    def handle_pictures(filename: Path, target_folder: Path) -> None:
        target_folder.mkdir(exist_ok=True, parents=True)
        filename.replace(target_folder / normalize_init.normalize(filename.name))

    @input_error
    def handle_media(filename: Path, target_folder: Path) -> None:
        target_folder.mkdir(exist_ok=True, parents=True)
        filename.replace(target_folder / normalize_init.normalize(filename.name))

    @input_error
    def handle_audio(filename: Path, target_folder: Path) -> None:
        target_folder.mkdir(exist_ok=True, parents=True)
        filename.replace(target_folder / normalize_init.normalize(filename.name))

    @input_error
    def handle_documents(filename: Path, target_folder: Path) -> None:
        target_folder.mkdir(exist_ok=True, parents=True)
        filename.replace(target_folder / normalize_init.normalize(filename.name))

    @input_error
    def handle_other(filename: Path, target_folder: Path) -> None:
        target_folder.mkdir(exist_ok=True, parents=True)
        filename.replace(target_folder / filename.name)

    @input_error
    def handle_archive(filename: Path, target_folder: Path) -> None:
        target_folder.mkdir(exist_ok=True, parents=True)
        folder_for_file = target_folder / normalize_init.normalize(filename.name.replace(filename.suffix, ''))
        folder_for_file.mkdir(exist_ok=True, parents=True)
        try:
            shutil.unpack_archive(filename, folder_for_file)
        except shutil.ReadError:
            print('Данний файл не є архівом')
            folder_for_file.rmdir()
        filename.unlink()

    @input_error
    def handle_folder(folder: Path):
        try:
            folder.rmdir()
        except OSError:
            print(f"Не млжливо видалити архів: {folder}")

    @input_error
    def replasefile_main(self):
        for file in Scan.JPEG_IMAGES:
            ReplaseFile.handle_pictures(file, self.folder / 'images' / 'JPEG')
        for file in Scan.JPG_IMAGES:
            ReplaseFile.handle_pictures(file, self.folder / 'images' / 'JPG')
        for file in Scan.PNG_IMAGES:
            ReplaseFile.handle_pictures(file, self.folder / 'images' / 'PNG')
        for file in Scan.SVG_IMAGES:
            ReplaseFile.handle_pictures(file, self.folder / 'images' / 'SVG')

        for file in Scan.MP3_AUDIO:
            ReplaseFile.handle_audio(file, self.folder / 'audio' / 'MP3')
        for file in Scan.OGG_AUDIO:
            ReplaseFile.handle_audio(file, self.folder / 'audio' / 'OGG')
        for file in Scan.WAV_AUDIO:
            ReplaseFile.handle_audio(file, self.folder / 'audio' / 'WAV')
        for file in Scan.AMR_AUDIO:
            ReplaseFile.handle_audio(file, self.folder / 'audio' / 'AMR')

        for file in Scan.AVI_VIDEO:
            ReplaseFile.handle_media(file, self.folder / 'video' / 'AVI')
        for file in Scan.MP4_VIDEO:
            ReplaseFile.handle_media(file, self.folder / 'video' / 'MP4')
        for file in Scan.MOV_VIDEO:
            ReplaseFile.handle_media(file, self.folder / 'video' / 'MOV')
        for file in Scan.MKV_VIDEO:
            ReplaseFile.handle_media(file, self.folder / 'video' / 'MKV')

        for file in Scan.DOC_DOCUMENTS:
            ReplaseFile.handle_documents(file, self.folder / 'documents' / 'DOC')

        for file in Scan.DOCX_DOCUMENTS:
            ReplaseFile.handle_documents(file, self.folder / 'documents' / 'DOCX')
        for file in Scan.TXT_DOCUMENTS:
            ReplaseFile.handle_documents(file, self.folder / 'documents' / 'TXT')
        for file in Scan.PDF_DOCUMENTS:
            ReplaseFile.handle_documents(file, self.folder / 'documents' / 'PDF')
        for file in Scan.XLSX_DOCUMENTS:
            ReplaseFile.handle_documents(file, self.folder / 'documents' / 'XLSX')
        for file in Scan.PPTX_DOCUMENTS:
            ReplaseFile.handle_documents(file, self.folder / 'documents' / 'PPTX')

        for file in Scan.MY_OTHER:
            ReplaseFile.handle_other(file, self.folder / 'MY_OTHER')

        for file in Scan.ZIP_ARCHIVES:
            ReplaseFile.handle_archive(file, self.folder / 'archives' / 'ZIP')
        for file in Scan.GZ_ARCHIVES:
            ReplaseFile.handle_archive(file, self.folder / 'archives' / 'GZ')
        for file in Scan.TAR_ARCHIVES:
            ReplaseFile.handle_archive(file, self.folder / 'archives' / 'TAR')

        for folder in Scan.FOLDERS[::-1]:
            ReplaseFile.handle_folder(folder)


class PrintResult(Scan):
    def print_result(self):
        result_lists = (self.JPEG_IMAGES, self.JPG_IMAGES, self.PNG_IMAGES, self.SVG_IMAGES,
                        self.AVI_VIDEO, self.MP4_VIDEO, self.MOV_VIDEO, self.MKV_VIDEO,
                        self.DOC_DOCUMENTS, self.DOCX_DOCUMENTS, self.TXT_DOCUMENTS, self.PDF_DOCUMENTS,
                        self.XLSX_DOCUMENTS, self.PPTX_DOCUMENTS,
                        self.MP3_AUDIO, self.OGG_AUDIO, self.WAV_AUDIO, self.AMR_AUDIO, self.ZIP_ARCHIVES,
                        self.GZ_ARCHIVES, self.TAR_ARCHIVES,
                        self.FOLDERS,
                        self.MY_OTHER)
        print(f"                    Список знайдених файлів\n \
              ")
        for i in result_lists:

            for _ in i:
                if _:
                    print(f"                {_}")
        print("")


class CleanFolderMain(PrintResult):  # меню користувача
    def run():
        print(F'        Вас вітає сортувальник файлів!\n\
                   ')
        while True:

            value = input(F'\
            -- Введіть "1" - Для сортування папки. \n\
            -- Введіть "0" - Для виходу в попередне меню. \n\
            >>> ')
            if value == "1":
                current_folder = Path(os.getcwd())
                while True:
                    current_dir = ""
                    for item in current_folder.iterdir():
                        if item.is_dir():
                            current_dir += f"                  {item.name}\n"
                    val = Path(input(F'\
              -- Вкажіть шлях до папки з файлами, яку потрібн відсортувати.\n\
              -- Введіть "1" - Для сортування папки в поточній директорії({current_folder}),\n\
              -- Введіть "0" - Для виходу в попередне меню.\n\
            >>> '))
                    if val == Path("0"):
                        break
                    elif val == Path("1"):
                        val = Path(input(F'\
              -- Введіть назву папки в поточній директорії({current_folder}),\n\
                 Cписок папок в поточній директорії\n\
{current_dir}  \n \
              >>> '))
                        check = input(F'\
            -- Введіть "1" - Для підтвердження сортування папки.{val}\n\
            -- Введіть "0" - Для виходу в попередне меню. \n\
            >>> ')
                        val = current_folder / val
                    elif os.path.exists(val) == True:
                        check = input(F'\
            -- Введіть "1" - Для підтвердження сортування папки.{val}\n\
            -- Введіть "0" - Для виходу в попередне меню. \n\
            >>> ')
                    else:
                        print("             Помилка.Такої папки не існує ")
                        continue
                    if check == "1":
                        t = Trans()
                        t.trans_dict()

                        s = Scan()
                        s.scan(val)
                        r = ReplaseFile(val)
                        r.replasefile_main()
                        print(f'            Сортування файлів виконане\n\
                               ')
                        p = PrintResult()
                        p.print_result()
                    elif value == 0:
                        continue
                    else:
                        continue
            elif value == "0":
                break
            else:
                print("            Такої команди не існує,введіть будь ласка повторно\n\
                        ")


t = Trans()

normalize_init = Normalize()


def run():
    CleanFolderMain.run()
# if __name__ == "__main__":
#         normalize_init = Normalize()
#         CleanFolderMain.run()

