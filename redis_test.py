from aiogram.filters import StateFilter, Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.redis import RedisStorage, Redis
from aiogram import Bot, Dispatcher
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup

BOT_TOKEN = "6972762642:AAEQ5k5aI_QfR2UqSYhTUE5zhgZxXPjWv_Y"

bot = Bot(BOT_TOKEN, parse_mode="HTML")
redis = Redis(host='localhost')
storage = RedisStorage(redis=redis)
dp = Dispatcher(storage=storage)


class Survey(StatesGroup):
    InputName = State()
    InputAge = State()
    InputAnswer = State()


cancel_state = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Отменить опрос", callback_data="cancel_survey")],
        [
            InlineKeyboardButton(
                text="Вернуться к предыдущему вопросу", callback_data="back_state"
            )
        ],
    ]
)


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer(
        "Привествую! Сейчас я задам тебе пару вопросов\n"
        "Когда будешь готов к опросу используй команду /start_survey"
    )


@dp.message(Command(commands=["start_survey"]))
async def start_fsm(message: Message, state: FSMContext):
    await message.answer("Отлично давай приступим к опросу!")
    await message.answer("Первый вопрос: Как тебя зовут?", reply_markup=cancel_state)
    await state.set_state(Survey.InputName)


@dp.message(StateFilter(Survey.InputName))
async def get_name(message: Message, state: FSMContext):
    await message.answer(f"Приятно познакомиться {message.text}!")
    await state.set_data({"name": message.text})
    await message.answer("Продолжим: Сколько тебе лет?", reply_markup=cancel_state)
    await state.set_state(Survey.InputAge)


@dp.message(StateFilter(Survey.InputAge))
async def fill_age(message: Message, state: FSMContext):
    try:  # Используем try как проверку (можем ли мы сообщение привести к типу int)
        await state.update_data({"age": int(message.text)})
        await message.answer(
            "Итак мы получили от тебя информацию теперь пришло время ответить на главный вопрос:\n"
            "Напиши отзыв о нашем курсе:",
            reply_markup=cancel_state,
        )
        await state.set_state(Survey.InputAnswer)
    except ValueError:
        await message.answer(
            "На этот вопрос нужно отвечать только числом не используй другие символы в ответе!",
            reply_markup=cancel_state,
        )


@dp.message(StateFilter(Survey.InputAnswer))
async def get_answer(message: Message, state: FSMContext):
    await message.answer(f"Спасибо за участие в опросе ваше мнение будет учтено!")
    await state.update_data({"review": message.text})
    state_data = await state.get_data()
    await message.answer(
        f"Ваши ответы:\n"
        f"Имя: {state_data['name']}\n"
        f"Возраст: {state_data['age']}\n"
        f"Отзыв: {state_data['review']}"
    )

    # какое-то действие с полученными данными...
    await state.clear()  # Выход из машины состояний


@dp.callback_query(
    lambda query: query.data == "cancel_survey", ~StateFilter(default_state)
)
async def exit_survey(query: CallbackQuery, state: FSMContext):
    print(query.data)
    await query.message.delete()
    await query.message.answer(
        "Очень жаль что ты хочешь отметить опрос :(\n"
        "Ты можешь всегда начать его заного используя команду: /start_survey"
    )
    await state.clear()


@dp.callback_query(
    lambda query: query.data == "back_state", ~StateFilter(default_state)
)
async def previous_question(query: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state == Survey.InputName:
        await query.message.answer("Это первый вропрос опроса!")
    elif current_state == Survey.InputAge:
        await query.message.answer(
            "Первый вопрос: Как тебя зовут?", reply_markup=cancel_state
        )
        await state.set_state(Survey.InputName)
    elif current_state == Survey.InputAnswer:
        await query.message.answer(
            "Второй вопрос: Сколько тебе лет?", reply_markup=cancel_state
        )
        await state.set_state(Survey.InputAge)


if __name__ == "__main__":
    dp.run_polling(bot)
