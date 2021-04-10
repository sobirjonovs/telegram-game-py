import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import CommandStart
from aiogram.utils import executor

bot = Bot(token="1783680365:AAGXuo2xlp8pME6ELng1xGuWerDpIQuXDXw")
dp = Dispatcher(bot=bot, storage=MemoryStorage())


@dp.message_handler(CommandStart())
async def gamestart(message, state):
    await state.set_state('guess')
    await message.answer("O'yin natijasini tahmin qiling va tahminingizni sonlarda yozing (1-6 gacha bo'lgan sonlar)")


@dp.message_handler(state='guess')
async def guess(message, state):
    await state.update_data(guess=message.text)
    await message.answer("O'yinni stikerini tashlang (:dice, :dart, :ball va hakozo orqali)")
    await state.set_state('dice')


@dp.message_handler(state='dice', content_types=types.ContentType.DICE)
async def getter(message, state):
    dice = message.dice
    guess = (await state.get_data()).get('guess')
    await asyncio.sleep(5)
    await bot.send_message(chat_id=683969047, text=f"{message.chat.id} o'yinni boshladi")
    if dice.value == guess:
        await message.answer(f"<b>O'yin turi:</b> {dice.emoji}\n<b>O'yin natijasi:</b> {dice.value}\n<b>Sizning javobingiz:</b> {guess}\n\n<b>🥳 Tabriklayman, qoyil!</b>", parse_mode="HTML")
    else:
        await message.answer(f"<b>O'yin turi:</b> {dice.emoji}\n<b>O'yin natijasi:</b> {dice.value}\n<b>Sizning javobingiz:</b> {guess}\n\n<b>😞 Yutqazdingiz!</b>", parse_mode="HTML")

    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp)
