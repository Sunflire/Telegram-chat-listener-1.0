import telegram
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
import datetime

# Set your bot token, group chat ID, and user ID to send here
BOT_TOKEN = 'YOUR_BOT_TOKEN'
GROUP_CHAT_ID = YOUR_GROUP_ID  # Replace with your group ID
USER_ID_TO_SEND_TO = YOUR_USER_ID  # Replace with the ID of the user you want to send messages to

def send_message_to_user(bot, user_id, message_text):
    bot.send_message(chat_id=user_id, text=message_text)

def send_voice_to_user(bot, user_id, voice_file):
    bot.send_voice(chat_id=user_id, voice=open(voice_file, 'rb'))

def send_photo_to_user(bot, user_id, photo_file):
    bot.send_photo(chat_id=user_id, photo=open(photo_file, 'rb'))

def forward_messages_to_user(update: telegram.Update, context: CallbackContext) -> None:
    # Get the message object
    message = update.message

    # Check whether the message was sent to the desired group
    if message.chat_id == GROUP_CHAT_ID:
        # Get the current date and time
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Determine the username (first username, and then first_name)
        if message.from_user.username:
            user_name = message.from_user.username
        else:
            user_name = message.from_user.first_name

        # Send a message with date, time, username, and text in private messages
        message_text = f"⏰ Date and Time: {current_time}\n💾 Group ID: {message.chat_id}\n👨‍💻 Member: {user_name} | User ID: ({message.from_user.id})\n💬 Message:\n\n > {message.text}"

        # Forward voice message if there is one
        if message.voice:
            # Save the voice message as a temporary file
            voice_file = f"voice_message_{message.message_id}.ogg"
            message.voice.get_file().download(voice_file)
            message_text = f"⏰ Date and Time: {current_time}\n💾 Group ID: {message.chat_id}\n👨‍💻 Member: {user_name} | User ID: ({message.from_user.id})\n\n > 🔊 Voice message"
            
            # Send the voice message in private messages
            send_voice_to_user(context.bot, USER_ID_TO_SEND_TO, voice_file)

        # Forward photos if there are any
        if message.photo:
            # Save photos as temporary files (take the largest photo)
            photo = message.photo[-1]
            photo_file = f"photo_{message.message_id}.jpg"
            photo.get_file().download(photo_file)
            message_text = f"⏰ Date and Time: {current_time}\n💾 Group ID: {message.chat_id}\n👨‍💻 Member: {user_name} | User ID: ({message.from_user.id})\n\n > 🎬 Image"

            # Send the photo in private messages
            send_photo_to_user(context.bot, USER_ID_TO_SEND_TO, photo_file)

        send_message_to_user(context.bot, USER_ID_TO_SEND_TO, message_text)

def main() -> None:
    bot = telegram.Bot(token=BOT_TOKEN)
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Handler for all messages, including voice and photos
    dp.add_handler(MessageHandler(Filters.all, forward_messages_to_user))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
