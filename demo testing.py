import telebot
import json
from linkconverter import *
TOKEN = '6365506202:AAGQ_ahTrDyHlkTTMquHz4YRHblMCP4vpbM'

# Replace 'YOUR_CHANNEL_USERNAME' with your channel's username
CHANNEL_USERNAME = 'deals_and_discounts_2'

bot = telebot.TeleBot(TOKEN)
# File to store user IDs who have started the bot
USER_FILE = 'user_data.json'

# Load user IDs from the file if it exists
try:
    with open(USER_FILE, 'r') as f:
        users_data = json.load(f)
except json.JSONDecodeError:
    users_data = []



# Handler for the /start command
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    print(user_id)
    # chat_id = message.chat.id
    # print(chat_id)
    if user_id not in users_data:
        users_data.append(user_id)
        save_user_data()

    user_status = bot.get_chat_member('@' + CHANNEL_USERNAME, user_id).status
    if user_status in ["member", "administrator"]:
        bot.reply_to(message, "Welcome! You have successfully subscribed to the channel. Now your bot can work.")
    else:
        bot.reply_to(message, "Please subscribe to the channel @deals_and_discounts_2 to use this bot.")


def save_user_data():
    with open(USER_FILE, 'w') as f:
        json.dump(users_data, f)


@bot.message_handler(func=lambda message: True)
def process_url(message):
    short_url = message.text.strip()
    affiliate_tag = "highfivesto0c-21"

    unshortened_url = unshorten_url(short_url)
    bot.reply_to(message, f"Unshortened URL: {unshortened_url}")

    if unshortened_url:
        cleaned_url = remove_amazon_affiliate_parameters(unshortened_url)
        bot.reply_to(message, f"Cleaned URL: {cleaned_url}")

        affiliate_url = create_amazon_affiliate_url(cleaned_url, affiliate_tag)
        bot.reply_to(message, f"Affiliate URL: {affiliate_url}")

        short_url = shorten_url_with_tinyurl(affiliate_url)
        bot.reply_to(message, f"Shortened URL: {short_url}")
    else:
        bot.reply_to(message, "Failed to process the URL. Please try again.")

# #################################################### For Admin #########################################################
@bot.message_handler(commands=['broadcast'])
def request_broadcast(message):
    if message.from_user.id == 849188964:
        bot.reply_to(message, "Please send the broadcast message you want to send to all users.")
        bot.register_next_step_handler(message, process_broadcast_text)

def process_broadcast_text(message):
    broadcast_text = message.text
    bot.reply_to(message, "Great! Now, if you want to include media, send it now. Otherwise, just type 'done'.")
    bot.register_next_step_handler(message, process_broadcast_media, broadcast_text)

def process_broadcast_media(message, broadcast_text):
    if message.text and  message.text.lower() == 'done':
        send_message_to_all(broadcast_text, media=None)
        bot.reply_to(message, "Broadcast message sent successfully!")
    elif message.content_type in ['photo', 'video', 'document']:
        send_message_to_all(broadcast_text, media=message)
        bot.reply_to(message, "Media added to the broadcast message.")
    else:
        bot.reply_to(message, "Invalid input. Please send a media file (photo, video, or document), or type 'done' to send the broadcast without media.")
        bot.register_next_step_handler(message, process_broadcast_media, broadcast_text)

def send_message_to_all(message_text, media):
    for user_id in users_data:
        if media:
            if media.content_type == 'photo':
                bot.send_photo(user_id, media.photo[-1].file_id, caption=message_text)
            elif media.content_type == 'video':
                bot.send_video(user_id, media.video.file_id, caption=message_text)
            elif media.content_type == 'document':
                bot.send_document(user_id, media.document.file_id, caption=message_text)
        else:
            bot.send_message(user_id, message_text)

# Handler for unknown commands
@bot.message_handler(func=lambda message: True, content_types=['text'])
def unknown(message):
    bot.reply_to(message, "Sorry, I don't understand this command.")


def main():
    bot.polling()

if __name__ == '__main__':
    main()
