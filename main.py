import telebot
import os

bot = telebot.TeleBot('5575408189:AAGoFgDByNwwu0nMjz6oWcW5cFph5MH7a04')
toChatID = 548277486

@bot.message_handler(commands=['start']) # старт
def start(message):
    bot.send_message(message.chat.id, 'Привет. Отправляй мне мемы!')

@bot.message_handler(commands=['msg']) # связь
def msg(text):
    gsm = f'{text.text}'
    gsm = gsm.replace('/msg', '')
    gsm = gsm.split('+')
    user = gsm[0]
    info = gsm[1]
    user = user.replace(' ', '')
    bot.send_message(user, info)

@bot.message_handler() # связь с той стороны
def getUser(message):
    text = f'Сообщение от {message.from_user.first_name} {message.from_user.last_name}. ID: {message.from_user.id}. Тэг: @{message.from_user.username}'
    bot.send_message(toChatID, text)
    bot.forward_message(toChatID, message.chat.id, message.message_id)
    bot.send_message(message.chat.id, 'Отправлено!')

@bot.message_handler(content_types=["photo"]) # фото
def echo_msg(message):
    if message.content_type == 'photo':
        raw = message.photo[2].file_id
        name = raw + ".jpg"
        file_info = bot.get_file(raw)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(name, 'wb') as new_file:
            new_file.write(downloaded_file)
        img = open(name, 'rb')
        bot.send_message(toChatID,
                         f"Предложка от {message.from_user.first_name} {message.from_user.last_name}",
                         parse_mode="Markdown")
        if message.from_user.username == None:
            print('')
        else:
            bot.send_message(toChatID, f'Tag: @{message.from_user.username}')
        bot.send_message(toChatID, f'ID: {message.from_user.id}')
        bot.send_photo(toChatID, img)
        bot.send_message(message.chat.id,
                         "Отправлено!",
                         parse_mode="Markdown")
        for root, dirs, files in os.walk("./"):
            for file in files:
                if file.endswith(".jpg"):
                    print(file)
                    os.remove(file)
                    break

@bot.message_handler(content_types=['video']) # видео
def echo_vid(message):
    file_info = bot.get_file(message.video.file_id)
    name = file_info.file_id + '.mp4'
    downloaded_file = bot.download_file(file_info.file_path)
    with open(name, 'wb') as new_file:
        new_file.write(downloaded_file)
    mp4 = open(name, 'rb')
    bot.send_message(toChatID,
                     f"Предложка от {message.from_user.first_name} {message.from_user.last_name}",
                     parse_mode="Markdown")
    if message.from_user.username == None:
        print('')
    else:
        bot.send_message(toChatID, f'Tag: @{message.from_user.username}')
    bot.send_message(toChatID, f'ID: {message.from_user.id}')
    bot.send_video(toChatID, mp4)
    bot.send_message(message.chat.id,
                     "Отправлено!",
                     parse_mode="Markdown")
    for root, dirs, files in os.walk("./"):
        for file in files:
            if file.endswith(".mp4"):
                print(file)
                os.remove(file)
                break

bot.polling(none_stop=True)

