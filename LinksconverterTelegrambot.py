
import telebot
import json
from linkconverter import *
import os
# from dotenv import load_dotenv
#
# # Load environment variables from .env file
# load_dotenv()

TOKEN = "6330410232:AAHz7URjg3-TbbLEE9tksotpodHFPU7WDM8"
# Replace 'YOUR_CHANNEL_USERNAME' with your channel's username
CHANNEL_USERNAME = 'deals_and_discounts_2'

bot = telebot.TeleBot(TOKEN)
# File to store user IDs who have started the bot
USER_FILE = 'user_data.json'

USER_AFFILIATE_FILE='user_affiliate_data.json'
user_affiliate_tags={}
# Load user IDs from the file if it exists
try:
    with open(USER_FILE, 'r') as f:
        users_data = json.load(f)
except json.JSONDecodeError:
    users_data = []

try:
    with open(USER_AFFILIATE_FILE, 'r') as f:
        users_affiliate_data = json.load(f)
        user_affiliate_tags.update(users_affiliate_data)
except json.JSONDecodeError:
    users_affiliate_data = []


###################################################################Reusable Functions ######################################3
def is_user_subscribed(user_id):
    # Check if the user is a member or an admin of the channel
    user_status = bot.get_chat_member('@' + CHANNEL_USERNAME, user_id).status
    return user_status in ["member", "administrator", "creator"]

def save_user_data():
    with open(USER_FILE, 'w') as f:
        json.dump(users_data, f)

def save_user_affiliate_data():
    with open(USER_AFFILIATE_FILE, 'w') as f:
        json.dump(user_affiliate_tags, f)
def get_user_affiliate_tag(user_id):
    return user_affiliate_tags.get(str(user_id))

def delete_user_affiliate_tag(user_id):
    user_affiliate_tags.pop(str(user_id), None)  # Remove the user's affiliate tag if exists
    save_user_data()

################################################################Start command he bro######################################################
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

    # user_status = bot.get_chat_member('@' + CHANNEL_USERNAME, user_id).status
    if is_user_subscribed(user_id):
        bot.reply_to(message, "Welcome! You have successfully subscribed to the channel. Now your bot can work.")
        bot.reply_to(message, "Now set your affiliate tag by the command /set_affiliate_tag")
        #set_affiliate_tag(message)

    else:
        # bot.reply_to(message, "Please subscribe to the channel @deals_and_discounts_2 to use this bot.")
        channel_link = f"https://telegram.me/{CHANNEL_USERNAME}"
        reply_markup = telebot.types.InlineKeyboardMarkup()
        reply_markup.add(telebot.types.InlineKeyboardButton(text="Join Channel", url=channel_link))
        bot.reply_to(message, "Subscribe to the channel to use this bot.", reply_markup=reply_markup)




############################################################################################################################################

@bot.message_handler(commands=['set_affiliate_tag'])
def set_affiliate_tag(message):
    user_id=message.from_user.id
    if user_id not in user_affiliate_tags:
        # Ask the user to enter their affiliate tag if it's not set
        bot.reply_to(message, "Please enter your affiliate tag without any special character:")
        bot.register_next_step_handler(message, process_affiliate_tag)
    else:
        # affiliate_tag =user_affiliate_tags[user_id]
        # Inform the user that the affiliate tag is already set
        bot.reply_to(message, f"Your affiliate tag '{user_affiliate_tags.get(user_id)}' is already set.")

def process_affiliate_tag(message):
    user_id=message.from_user.id
    affiliate_tag = message.text.strip()
    user_affiliate_tags[str(user_id)]= affiliate_tag             # appending to the dictionary
    # users_affiliate_data[user_id]=affiliate_tag
    save_user_affiliate_data()
    bot.reply_to(message, f"Your affiliate tag '{affiliate_tag}' has been saved.Now send me amazon Links for conversion.As of now text with links are not supported")



#####################################################**************************************##############################################
@bot.message_handler(commands=['delete_affiliate'])
def delete_affiliate_tag(message):
    user_id = message.from_user.id
    affiliate_tag = get_user_affiliate_tag(user_id)
    if affiliate_tag:
        # Delete the user's affiliate tag
        delete_user_affiliate_tag(user_id)
        bot.reply_to(message, "Your affiliate tag has been deleted.")
    else:
        bot.reply_to(message, "You don't have an affiliate tag set.")


@bot.message_handler(commands=['contact'])
def show_contact_link(message):
    # Replace 'TARGET_TELEGRAM_USERNAME' with the username of the target Telegram user
    target_username = 'Shashwatkumar01'
    contact_link = f"https://t.me/{target_username}"
    reply_markup = telebot.types.InlineKeyboardMarkup()
    reply_markup.add(telebot.types.InlineKeyboardButton(text="Contact", url=contact_link))
    bot.reply_to(message, f"Contact for Customization or Broadcast your Ads", reply_markup=reply_markup)





# #################################################### For Admin(mera Faida) ############################################################################
@bot.message_handler(commands=['broadcast'])
def request_broadcast(message):
    if message.from_user.id == 849188964:
        bot.reply_to(message, "Please send the broadcast message you want to send to all users.")
        bot.register_next_step_handler(message, process_broadcast_text)
    else:
        bot.reply_to(message, "You are not Authorized . Contact admin")

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


@bot.message_handler(commands=['showlist'])
def show_user_lists(message):
    usercount = len(user_data)
    userlists = str(user_data)
    bot.reply_to(message, f"users lists are: {userlists} ")
    bot reply_to(message, f" number of users :{usercount}")
                 
    

###################################################################################################################################

@bot.message_handler(func=lambda message: True)
def process_url(message):
    user_id = message.from_user.id

    if is_user_subscribed(user_id):
        short_url = message.text.strip()
        affiliate_tag =  user_affiliate_tags.get(user_id)

        unshortened_url = unshorten_url(short_url)
        bot.reply_to(message, f"Unshortened URL: {unshortened_url}")

        if unshortened_url:
            cleaned_url = remove_amazon_affiliate_parameters(unshortened_url)
            # bot.reply_to(message, f"Cleaned URL: {cleaned_url}")

            affiliate_url = create_amazon_affiliate_url(cleaned_url, affiliate_tag)
            bot.reply_to(message, f"Your Affiliate long URL: {affiliate_url}")

            short_url = shorten_url_with_tinyurl(affiliate_url)
            bot.reply_to(message, f"Shortened Affiliate URL: {short_url}")
        else:
            bot.reply_to(message, "Failed to process the URL. Please try again.")
    else:
        channel_link = f"https://telegram.me/{CHANNEL_USERNAME}"
        reply_markup = telebot.types.InlineKeyboardMarkup()
        reply_markup.add(telebot.types.InlineKeyboardButton(text="Join Channel", url=channel_link))
        bot.reply_to(message, "Subscribe to the channel to use this bot.", reply_markup=reply_markup)


# Handler for unknown commands
@bot.message_handler(func=lambda message: True, content_types=['text'])
def unknown(message):
    bot.reply_to(message, "Sorry, I don't understand this command.")


def main():
    bot.polling()

if __name__ == '__main__':
    main()
