import aiml
import MeCab
from telegram_bot import TelegramBot
from mlask import MLAsk

class AimlSystem:
  def __init__(self):
    self.sessiondic = {}
    self.tagger = MeCab.Tagger('-Owakati')
  def initial_message(self, input):
    sessionId = input['sessionId']
    kernel = aiml.Kernel()
    kernel.learn("aiml.xml")
    self.sessiondic[sessionId] = kernel
    return {'utt':'はじめまして，雑談を始めましょう', 'end':False}
  def reply(self, input):
    sessionId = input['sessionId']
    utt = input['utt']
    utt = self.tagger.parse(utt)
    response = self.sessiondic[sessionId].respond(utt)
    emotion_dic = {'suki':'🥰', 'ikari':'😡', 'kowa':'😱',
                   'yasu':'😊', 'iya':'😫', 'aware':'😭',
                   'takaburi':'🤩', 'odoroki':'🙄', 'haji':'🤭',
                   'yorokobi':'😄'}
    emotion_analyzer = MLAsk()
    json_emot = emotion_analyzer.analyze(utt)
    if json_emot['emotion'] == None:
      return {'utt':response, 'end':False}
    else:
      emotion = json_emot['representative'][0]
      return {'utt':response + emotion_dic[emotion], 'end':False}

if __name__ == '__main__':
    system = AimlSystem()
    bot = TelegramBot(system)
    bot.run()
