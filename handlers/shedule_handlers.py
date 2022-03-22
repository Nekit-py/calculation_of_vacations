
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import *
import logging
from shedule import *


logging.basicConfig(level=logging.INFO)


class SheduleVariables(StatesGroup):
    waiting_for_start_date = State()
    waiting_for_days = State()
    waiting_for_additional = State()
    waiting_for_travel = State()


async def start_shedule(message: types.Message) -> None:
    await message.answer("Введите дату первого дня отпуска (Пример: '01.01.2020'): ")
    await SheduleVariables.waiting_for_start_date.set()


async def start_date_choosen(message: types.Message, state: FSMContext) -> None:
    try:
        start_date = Shedule.start_date_to_datetime(message.text)
        print(start_date)
        await state.update_data(choosen_start_date=start_date)
        await SheduleVariables.next()
        await message.answer("Введите общее кол-во дней отпуска: ")
    except DateException:
        await message.answer("Введене неверный формат даты. Пример: '01.01.2020'\n\n")


async def days_choosen(message: types.Message, state: FSMContext) -> None:
    try:
        days = int(message.text)
        print(days)
        await state.update_data(choosen_days=days)
        await SheduleVariables.next()
        await message.answer("Введите общее кол-во дней отпуска за выслугу: ")
    except ValueError:
        await message.answer("\nОШИБКА! Введденое кол-во дней должной быть целочисленным.\n\n")


async def additional_choosen(message: types.Message, state: FSMContext) -> None:
    try:
        additional = message.text

        if not additional:
            additional = 0
            await message.answer("Кол-во дней отпуска за выслугу = 0\n")
        else:
            additional = int(additional)

        print(additional)
        await state.update_data(choosen_additional=additional)
        await SheduleVariables.next()
        await message.answer("Введите кол-во дней затраченных на дорогу: ")
    except ValueError:
        await message.answer("\nОШИБКА! Введденое кол-во дней должной быть целочисленным.\n\n")


async def travel_choosen(message: types.Message, state: FSMContext) -> None:
    try:
        travel = message.text

        if not travel:
            travel = 0
            await message.answer("Кол-во дней на дорогу = 0\n")
        else:
            travel = int(travel)

        await state.update_data(choosen_travel=travel)

        user_data = await state.get_data()

        print(user_data)
        shedule = Shedule(
            start_date=user_data["choosen_start_date"],
            additional=user_data["choosen_days"],
            travel=user_data["choosen_additional"],
            days=user_data["choosen_travel"],
        )

        shedule.get_vocation_end_date()
        await message.answer(shedule)
        await state.finish()
    except ValueError:
        await message.answer("\nОШИБКА! Введденое кол-во дней должной быть целочисленным.\n\n")


def register_handler_shedule(dp: Dispatcher) -> None:
    dp.register_message_handler(start_shedule, commands="start", state="*")
    dp.register_message_handler(start_date_choosen, state=SheduleVariables.waiting_for_start_date)
    dp.register_message_handler(days_choosen, state=SheduleVariables.waiting_for_days)
    dp.register_message_handler(additional_choosen, state=SheduleVariables.waiting_for_additional)
    dp.register_message_handler(travel_choosen, state=SheduleVariables.waiting_for_travel)