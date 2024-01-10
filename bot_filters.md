## Обработка сообщения
```python
@dp.message()
```

## Фильтрация команд
```python
from aiogram.filters import CommandStart,Command

@dp.message(CommandStart())
async def command_start(message: Message):
    await message.answer('Вы прописали команду старт')


@dp.message(Command(commands=["start"]))
async def command_start(message: Message):
    await message.answer(
        'Ответ на команду /start То же самое что и хендлер сверху') 
    # Этот код не будет выполнен (хендлер сверху перекрывает его)


@dp.message(Command(commands=["start"], prefix='|')) #Изменение префикса команд
async def c_start(message: Message):
    await message.answer('Ответ на команду |start')
```

## “Магическая” фильтрация
```python
from aiogram import F
```

```python
F.photo                                    # Фильтр для фото
F.voice                                    # Фильтр для голосовых сообщений
F.content_type.in_({ContentType.PHOTO,
                    ContentType.VOICE,
                    ContentType.VIDEO})    # Фильтр на несколько типов контента
F.text == 'привет'                         # Фильтр на полное совпадение текста
F.text.startswith('привет')                # Фильтр на то, что текст сообщения начинается с 'привет'
~F.text.endswith('bot')                    # Инвертирование фильтра
```

```python
lambda message: message.photo                        # Фильтр для фото
lambda message: message.voice                        # Фильтр для голосовых сообщений
lambda message: message.content_type in {ContentType.PHOTO,
                                         ContentType.VOICE,
                                         ContentType.VIDEO}   # Фильтр на несколько типов контента
lambda message: message.text == 'привет'             # Фильтр на полное совпадение текста
lambda message: message.text.startswith('привет')    # Фильтр на то, что текст сообщения начинается с 'привет'
lambda message: not message.text.startswith('bot')   # Инвертирование фильтра
```