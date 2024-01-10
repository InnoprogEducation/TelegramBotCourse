import os

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class Catalog:
    def __init__(self, path: str):
        self.path = path
        self.photos = []
        self.extensions = ["jpg", "png"]
        self.photos = []
        self.name = path.split('/')[-1]

        files = os.listdir(path=self.path)
        for file in files:
            if file.split('.')[1] in self.extensions:
                self.photos += [file]

    def generate_photos_keyboard(self) -> ReplyKeyboardMarkup:
        self.refresh()
        kb = []
        for photo in self.photos:
            kb += [[KeyboardButton(text=photo)]]
        kb += [[KeyboardButton(text="Закончить просмотр")]]
        return ReplyKeyboardMarkup(keyboard=kb)

    def get_photo_path(self, photo_name: str):
        self.refresh()
        if photo_name in self.photos:
            return self.path + '/' + photo_name
        return None

    def generate_photo_name(self):
        return f"photo_{len(self.photos) + 1}"

    async def save_photo(self, bot, photo):
        self.refresh()
        await bot.download(photo, destination=self.path + '/' + f'{self.generate_photo_name()}.png')

    def refresh(self):
        photos = []
        files = os.listdir(path=self.path)
        for file in files:
            if file.split('.')[1] in self.extensions:
                photos += [file]
        self.photos = photos

    def get_photo_paths(self):
        self.refresh()
        return [self.path+'/'+photo for photo in self.photos]

    def __repr__(self):
        return f"Catalog:{self.name} {self.photos=}"


class CatalogManager:

    def __init__(self):
        self.main_dir = 'gallery'
        self.path = './'
        self.catalogs = []
        self.max_catalogs = 9

        dirs = os.listdir(path=self.path)
        if self.main_dir not in dirs:
            os.makedirs(self.main_dir)

        self.refresh()

    def exist(self, catalog_name: str) -> bool:
        self.refresh()
        catalogs_names = [c.name for c in self.catalogs]
        if catalog_name in catalogs_names:
            return True
        return False

    def get_catalog(self, catalog_name: str) -> Catalog | None:
        if self.exist(catalog_name):
            return list(filter(lambda c: c.name == catalog_name, self.catalogs))[0]
        return None

    def make_catalog(self, catalog_name: str) -> str:
        self.refresh()
        if len(self.catalogs) == self.max_catalogs:
            return "Достигнут лимит по каталогам"
        if self.exist(catalog_name):
            return "Каталог с таким именем уже существует"
        os.makedirs(self.path + self.main_dir + '/' + catalog_name)  # Создание каталога
        self.refresh()
        if self.exist(catalog_name):
            return f"Католог {catalog_name} успешно создан"
        return f"Каталог {catalog_name} не создан"

    def refresh(self):
        catalogs = os.listdir(path=self.path + self.main_dir)
        list_catalogs = []
        for catalog in catalogs:
            if catalog.count('.') == 0:  # не имеет расширения (просто папка)
                list_catalogs += [Catalog(
                    path=self.path + self.main_dir + '/' + catalog)]  # Инициализируем каталог и добавляем его в список
        self.catalogs = list_catalogs

    def generate_catalogs_keyboard(self) -> ReplyKeyboardMarkup:
        self.refresh()
        buttons_list = []
        for catalog in self.catalogs:
            buttons_list += [[KeyboardButton(text=catalog.name)]]
        return ReplyKeyboardMarkup(keyboard=buttons_list)
