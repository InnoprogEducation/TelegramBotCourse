import random

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ContentType
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.types import Message, FSInputFile, KeyboardButton
from catalogs import CatalogManager

BOT_TOKEN = "6972762642:AAEQ5k5aI_QfR2UqSYhTUE5zhgZxXPjWv_Y"

bot = Bot(BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()


class Inputs(StatesGroup):
    # save_photo
    Photo = State()
    CatalogForSave = State()
    # make_catalog
    CatalogName = State()
    # show
    ShowCatalogName = State()
    PhotoName = State()

cm = CatalogManager()  # Инициализация менеджера каталогов

# Обработчик команды старт
@dp.message(Command(commands=['start']))
async def show_start_message(message: Message):
    await message.answer(f"Приветсвую это бот работает как общая фотогалерея!\n"
                         f"Список команд:\n"
                         f"- /save_photo  (Сохранить фотографию)\n"
                         f"- /make_catalog (Создать каталог)\n"
                         f"- /show (Показать фотографию (с выбором каталога и фото))\n"
                         f"- /show_random (Показать случайную фотографию)\n")


# Обработчик команды make_catalog
@dp.message(Command(commands=['make_catalog']), StateFilter(default_state))
async def make_catalog(message: Message, state: FSMContext):
    await message.answer(f"Введите имя каталога:")
    await state.set_state(Inputs.CatalogName)


# Получение имени каталога и его создание
@dp.message(StateFilter(Inputs.CatalogName))
async def create_catalog(message: Message, state: FSMContext):
    catalog_name = message.text
    msg = cm.make_catalog(catalog_name)
    await message.answer(msg)
    await state.set_state(default_state)  # Выход из машины состояний


# Обработчик команды save_photo
@dp.message(Command(commands=['save_photo']), StateFilter(default_state))
async def save_photo(message: Message, state: FSMContext):
    await message.answer(f"Хорошо, теперь пришлите мне фотографию:")
    await state.set_state(Inputs.Photo)


# Получение фотографии
@dp.message(StateFilter(Inputs.Photo), F.content_type.in_({ContentType.PHOTO}))
async def get_photo(message: Message, state: FSMContext):
    await state.set_data({"photo-id": message.photo[-1].file_id})
    await message.answer("Выбери каталог ты хочешь его сохранить фотографию:",
                         reply_markup=cm.generate_catalogs_keyboard())
    await state.set_state(Inputs.CatalogForSave)


# Получение имени каталога и сохранение фотографиии
@dp.message(StateFilter(Inputs.CatalogForSave))
async def get_catalog_for_save(message: Message, state: FSMContext):
    state_data = await state.get_data()
    photo_id = state_data['photo-id']
    photo = await bot.get_file(file_id=photo_id)
    catalog = cm.get_catalog(message.text)
    if catalog is None:
        await message.answer("Такого каталога не существует")
    else:
        await catalog.save_photo(bot, photo)
        await message.answer("Фото успешно сохранено!")

    await state.set_state(default_state)  # Выход из машины состояний

# Обработчик команды show
@dp.message(Command(commands=['show']), StateFilter(default_state))
async def show_photo(message: Message, state: FSMContext):
    keyboard = cm.generate_catalogs_keyboard()
    keyboard.keyboard.append([KeyboardButton(text="Отменить просмотр")])
    await message.answer("Выбери каталог из которого хочешь посмотреть фотографию:",
                         reply_markup=keyboard)
    await state.set_state(Inputs.ShowCatalogName)


# Завершение просмотра каталога
@dp.message(lambda m: m.text == "Отменить просмотр", StateFilter(Inputs.ShowCatalogName))
async def cancel_photo_display(message: Message, state: FSMContext):
    await message.answer("Просмотр фотографий отменен")
    await state.set_state(default_state)


# Вывод клавиатуры для выбора фотографии
@dp.message(StateFilter(Inputs.ShowCatalogName))
async def display_catalog_keyboard(message: Message, state: FSMContext):
    catalog_name = message.text
    catalog = cm.get_catalog(catalog_name)
    if catalog is None:
        await message.answer("Такого каталога не существует")
        await state.set_state(default_state)
    else:
        await state.set_data({"catalog": catalog.name})
        await message.answer("Выбери фотографию которую хочешь посмотреть:",
                             reply_markup=catalog.generate_photos_keyboard())
        await state.set_state(Inputs.PhotoName)


# Завершение просмотра каталога
@dp.message(lambda m: m.text == "Закончить просмотр", StateFilter(Inputs.PhotoName))
async def cancel_photo_display(message: Message, state: FSMContext):
    keyboard = cm.generate_catalogs_keyboard()
    keyboard.keyboard.append([KeyboardButton(text="Отменить просмотр")])
    await message.answer("Выбери каталог из которого хочешь посмотреть фотографию:",
                         reply_markup=keyboard)
    await state.set_state(Inputs.ShowCatalogName)


# Отображение выбранной фотографии
@dp.message(StateFilter(Inputs.PhotoName))
async def display_photo(message: Message, state: FSMContext):
    photo_name = message.text
    state_data = await state.get_data()
    catalog_name = state_data['catalog']
    catalog = cm.get_catalog(catalog_name)
    photo_path = catalog.get_photo_path(photo_name)
    print(photo_path)
    if photo_path is None:
        await message.answer("Такой фотографии нет в каталоге")
    else:
        await bot.send_photo(chat_id=message.chat.id, photo=FSInputFile(photo_path))


# Обработчик команды show_random
@dp.message(Command(commands=['show_random']))
async def show_random(message: Message):
    all_photos = []
    for catalog in cm.catalogs:
        all_photos += catalog.get_photo_paths()
    if len(all_photos) == 0:
        await message.answer("В каталогах нет фотографий")
    else:
        random_photo = random.choice(all_photos)
        await message.answer("Случайное фото из галлереи:")
        await bot.send_photo(chat_id=message.chat.id, photo=FSInputFile(random_photo))



if __name__ == "__main__":
    dp.run_polling(bot)
