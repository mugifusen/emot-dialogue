import aiml
import MeCab
from telegram_bot import TelegramBot

class AimlSystem:
  def __init__(self):
    self.sessiondic = {}
    self.tagger = MeCab.Tagger('-Owakati')
  def initial_message(self, input):
    sessionId = input['sessionId']
    kernel = aiml.Kernel()
    kernel.learn("aiml.xml")
    self.sessiondic[sessionId] = kernel
    return {'utt':'はじめまして，雑談を始めましょう',
            'end':False}
  def reply(self, input):
    sessionId = input['sessionId']
    utt = input['utt']
    utt = self.tagger.parse(utt)
    response = self.sessiondic[sessionId].respond(utt)
    return {'utt': response, 'end': False}

if __name__ == '__main__':
    system = AimlSystem()
    bot = TelegramBot(system)
    bot.run()
