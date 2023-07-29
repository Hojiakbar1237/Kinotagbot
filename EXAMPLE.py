from Configuration import TOKEN
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import re

pattern = re.compile("^\+?998[0-9]{9}$")
bot = Bot(token=TOKEN)# elonuz_bot tokeni
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
rkb = ReplyKeyboardMarkup(resize_keyboard=True)
rkb2 = ReplyKeyboardMarkup(resize_keyboard=True)
rkb.add(KeyboardButton("Ish joyi kerak"))
rkb2.add(KeyboardButton("Ha"),KeyboardButton("Yo'q"))

class Form(StatesGroup):
    ful_name = State()
    age = State()
    Texnalogiya = State()
    Aloqa = State()
    Hudud = State()
    Kasbi = State()
    Mr_time = State()
    Maqsad = State()

@dp.message_handler(commands=['start'], state="*") # state="*" dastur ishlash davomidaham start bosilsa ishlayveradi
async def start_command(message: types.Message):
    await message.answer(f"<b>Assalom alaykum {message.from_user.first_name} </b>"
                         f"<b>Ustoz-Shogird kanalining rasmiy botiga xush kelibsiz!</b>",
                         reply_markup=rkb,parse_mode="HTML")

@dp.message_handler(Text(equals="Ish joyi kerak"))
async def fill_form(message: types.Message):
    await Form.next()
    await message.answer("Ism_familyangizni kiriting :")

@dp.message_handler(state=Form.ful_name)
async def set_name(message: types.Message, state: FSMContext):
    """
    Set user name
    """
    async with state.proxy() as data:
        data['ful_name'] = message.text

    await  Form.next()
    await message.answer("yoshingizni kiriting : ")
@dp.message_handler(lambda message: not message.text.isdigit(), state=Form.age)
async def avoid_age_format(message: types.Message):
    await message.answer("yosh faqat sonlardan iborat bolishi kerak ! ")

@dp.message_handler(lambda message: message.text.isdigit(), state=Form.age)
async def process_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = int(message.text)
    await Form.next()
    await message.answer("Texnalogiyalarni kiriting : ")

@dp.message_handler(state=Form.Texnalogiya)
async def set_skills(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Texnalogiya'] = message.text
    await Form.next()
    await message.answer("""Aloqa uchun raqamingizni qoldiring
Masalan :+998902821237""")

@dp.message_handler(lambda message: re.match(pattern, message.text), state=Form.Aloqa)
async def process_phone_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Aloqa'] = message.text
    await Form.next()
    await message.answer("Hududni kiriting :")

@dp.message_handler(state=Form.Hudud)
async def set_location(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Hudud'] = message.text
    await Form.next()
    await message.answer("""Kasbi : """)

@dp.message_handler(state=Form.Kasbi)
async def set_job(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Kasbi'] = message.text
    await Form.next()
    await message.answer("""Murojat qilish vaqti : """)

@dp.message_handler(state=Form.Mr_time)
async def set_dtime(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Mr_time'] = message.text
    await Form.next()
    await message.answer("""Maqsad : """)

@dp.message_handler(state=Form.Maqsad)
async def set_goal(message: types.Message, state: FSMContext):
    await state.update_data(Maqsad=message.text)
    await Form.Maqsad.set()
    data = await state.get_data()
    msg = f"👨‍💼Xodim: {data['ful_name']}, \n🕖Yosh: {data['age']}, \n📚Texnalogiya : #{data['Texnalogiya']},\n🇺🇿Telegram : {message.from_user.username}, \n☎️Aloqa: {data['Aloqa']}, \n" \
          f"📍Hudud : {data['Hudud']}, \n💼Kasbi : {data['Kasbi']},\n⏳Murojat qilish vaqti : {data['Mr_time']}, \n🤔Maqsad : {data['Maqsad']}"
    await bot.send_message(chat_id=message.from_user.id, text=msg,reply_markup=rkb2)
    await message.answer("Malumotlarni togriligini tasdiqlash uchun Ha tugmasini bosing")
    await state.reset_state(with_data=False)

@dp.message_handler(lambda message: message.text in ('Ha', "Yo'q"))
async def for_admin(message: types.Message, state:  FSMContext):
    if message.text == "Ha":
        data = await state.get_data()
        await bot.send_message(chat_id=1857890588,text=f"👨‍💼Xodim: {data['ful_name']}, \n🕖Yosh: {data['age']}, \n📚Texnalogiya : #{data['Texnalogiya']},\n🇺🇿Telegram : {message.from_user.username}, \n☎️Aloqa: {data['Aloqa']}, \n 📍Hudud : {data['Hudud']}, \n💼Kasbi : {data['Kasbi']},\n⏳Murojat qilish vaqti : {data['Mr_time']}, \n🤔Maqsad : {data['Maqsad']}")
        await message.answer("Ma'lumot muvofaqiyatli yuborildi")
        await state.reset_state()
    else:
        await message.answer("Ariza bekor qilindi!", reply_markup=rkb)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
