import telebot
import config
import uuid
import scripts
import os

bot = telebot.TeleBot(config.token, parse_mode=None)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
	bot.reply_to(message, message.text)

@bot.message_handler(content_types=['photo'])
def photo(message):
	print(message)
	word = message.caption
	fileID = message.photo[-1].file_id
	file_info = bot.get_file(fileID)
	downloaded_file = bot.download_file(file_info.file_path)
	save_way = "source_images/"+str(uuid.uuid1())+".jpg"    
	with open(save_way, 'wb') as new_file:
		new_file.write(downloaded_file)
	way = scripts.signature(save_way, word)
	os.remove(save_way)
	img = open(way, 'rb')
	bot.send_photo(message.chat.id, img, reply_to_message_id=message.message_id)
	os.remove(way)

bot.polling()