import telegram
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
import datetime

# Set your bot token, group chat ID and user ID to send here
BOT_TOKEN = 'YOUR_BOT_TOKEN'
GROUP_CHAT_ID = YOUR_GROUP_ID  # Replace with your group ID
USER_ID_TO_SEND_TO = YOUR_USER_ID # Replace with the ID of the user you want to send messages to

def send_message_to_user(bot, user_id, message_text):
    bot.send_message(chat_id=user_id, text=message_text)

def forward_messages_to_user(update: telegram.Update, context: CallbackContext) -> None:
    # Getting the message object
    message = update.message

    # Checking whether the message was sent to the desired group
    if message.chat_id == GROUP_CHAT_ID:
        # Получаем текущую дату и время
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Determine the username (first username, and then first_name)
        if message.from_user.username:
            user_name = message.from_user.username
        else:
            user_name = message.from_user.first_name

        # Send a message with date, time, username and text in private messages
        message_text = f"⏰ Date and time: {current_time}\n💾 Group ID: {message.chat_id}\n👨‍💻 User: {user_name} User-id: ({message.from_user.id})\n💬 Message:\n\n > {message.text}"

        send_message_to_user(context.bot, USER_ID_TO_SEND_TO, message_text)

def main() -> None:
    bot = telegram.Bot(token=BOT_TOKEN)
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Text message handler
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, forward_messages_to_user))

    # Launch the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
