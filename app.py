import telebot
import config
import os
import io
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from flask import Flask, request

server = Flask(__name__)
bot = telebot.TeleBot(config.token, parse_mode=None)

@server.route("/", methods=["POST"])
def recieve_update():
	bot.process_new_updates(
		[telebot.types.Update.de_json(request.stream.read().decode("utf-8"))]
	)
	return {"ok": True}

@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
	bot.reply_to(message, message.text)

@bot.message_handler(content_types=["photo"])
def photo(message):
	word = message.caption
	if not word:
		word = 'Souluon'
	fileID = message.photo[-1].file_id
	file_info = bot.get_file(fileID)
	downloaded_file = bot.download_file(file_info.file_path)
	font = ImageFont.truetype('fonts/SSS.Ghoul.ttf', size=100)
	img = Image.open(io.BytesIO(downloaded_file))
	draw_text = ImageDraw.Draw(img)
	size = draw_text.textsize('©'+' '+word, font=font)
	draw_text.text(
		(img.width-(size[0]+7), img.height-(size[1]+7)),
		'©'+' '+word,
		font=font,
		fill=('#808080')
		)
	bot.send_photo(message.chat.id, img, reply_to_message_id=message.message_id)

@server.route("/" + config.token, methods=["POST"])
def getMessage():
	bot.process_new_updates(
		[
			telebot.types.Update.de_json(
				request.stream.read().decode("utf-8")
			)
		]
	)
	return "!", 200

if __name__ == "__main__":
	server.run(host="0.0.0.0", port = int(os.environ.get("PORT", 5000)))
