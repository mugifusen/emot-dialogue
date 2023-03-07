from telegram.ext import (Updater, CommandHandler,
                          MessageHandler, Filters)

TOKEN = "6151058622:AAGq1Yh1iuTWvcsvzMINgetlAaGPrzzQueA"
class TelegramBot:
  def __init__(self, system):
    self.system = system
  def start(self, update, bot):
    input = {'utt':None, 'sessionId':str(update.message.from_user.id)}
    update.message.reply_text(self.system.initial_message(input)["utt"])
  def message(self, update, bot):
    input = {'utt':update.message.text,
             'sessionId':str(update.message.from_user.id)}
    system_output = self.system.reply(input)
    update.message.reply_text(system_output["utt"])
  def run(self):
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", self.start))
    dp.add_handler(MessageHandler(Filters.text, self.message))
    updater.start_polling()
    updater.idle()
