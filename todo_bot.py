from aiogram import Bot, Dispatcher, types
import datetime

from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery

# Получите токен своего бота
API_TOKEN = "6972762642:AAEQ5k5aI_QfR2UqSYhTUE5zhgZxXPjWv_Y"

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Словарь для хранения задач
tasks = set()
total_task = 0


# Класс Task для представления задачи
class Task:
    def __init__(self, id, text):
        global total_task
        self.id = id
        self.text = text
        self.task_id = total_task + 1
        self.creation_date = datetime.date.today()
        total_task += 1
        self.task_keyboard = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="Пометить как сделанное", callback_data=f"done:{self.task_id}")
        ]])

    def present_message_text(self):
        return f"Дата создания: {self.creation_date.day}.{self.creation_date.month}\n" \
               f"Задача: {self.text}"


# Функция-обработчик для команды /start
@dp.message(Command(commands=['start']), StateFilter(default_state))
async def start(message: types.Message, state: State):
    await message.answer(
        "Привет! Я бот для управления списком дел. Вот список доступных команд:\n"
        "/newtask - создать новую задачу\n"
        "/list - показать список задач\n"
        "/deletetask - удалить задачу")


class Input(StatesGroup):
    TextTask = State()


# Функция-обработчик для команды /newtask
@dp.message(Command(commands=['newtask']), StateFilter(default_state))
async def new_task(message: types.Message, state: FSMContext):
    await message.answer("Напиши текст для новой задачи:")
    await state.set_state(Input.TextTask)


# Функция-обработчик для команды /newtask
@dp.message(StateFilter(Input.TextTask))
async def create_new_task(message: types.Message, state: FSMContext):
    global tasks
    user_id = message.chat.id
    text = message.text
    tasks |= {Task(user_id, text)}
    await message.answer("Задача успешно создана!")
    await state.set_state(default_state)  # Выход из машины состояний


# Обработчик кнопок на задачах
@dp.callback_query(lambda query: "done" in query.data)
async def close_task(query: CallbackQuery):
    task_id = int(query.data.split(':')[1]) # ['done', '1']
    find_task = [task for task in tasks if task.task_id == task_id]
    if len(find_task) != 0:
        tasks.remove(find_task[0])
        await query.message.edit_text("Задание успешно помечено как сделанное!")
    else:
        await query.message.edit_text("Задание уже было помечено ранее!")


# Функция-обработчик для команды /list
@dp.message(Command(commands=['list']), StateFilter(default_state))
async def list_tasks(message: Message):
    # Логика для вывода списка задач
    user_id = message.chat.id
    user_tasks = []
    for task in tasks:
        if task.id == user_id:
            user_tasks += [task]
    if len(user_tasks) == 0:
        await message.answer("У тебя нет текущих задач :(\n"
                             "Ты можешь создать задачу используя команду /newtask")
    else:
        await message.answer("Вот список текущих задач:")
        for task in user_tasks:
            await message.answer(task.present_message_text(), reply_markup=task.task_keyboard)


if __name__ == '__main__':
    dp.run_polling(bot)
