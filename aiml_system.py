import aiml
import MeCab
from mlask import MLAsk   #感情分析に用いるライブラリ
from telegram_bot import TelegramBot

class AimlSystem:
    def __init__(self):
        # セッションを管理するための辞書 
        self.sessiondic = {}
        # 形態素解析器を用意
        self.tagger = MeCab.Tagger('-Owakati')
        
    def initial_message(self, input):
        sessionId = input['sessionId']
        # AIMLを読み込むためのインスタンスを用意
        kernel = aiml.Kernel()
        # aiml.xmlを読み込む
        kernel.learn("aiml.xml")
        # セッションごとに保存する
        self.sessiondic[sessionId] = kernel

        return {'utt':'はじめまして，雑談を始めましょう', 'end':False}

    def reply(self, input):
        emotion_dic = {'suki': '🥰', 'ikari': '😡', 'kowa': '😱', 'yasu': '😊', 'iya': '😫', 'aware': '😭', 'takaburi': '🤩', 'odoroki': '🙄', 'haji': '🤭', 'yorokobi': '😄'}
        sessionId = input['sessionId']
        utt = input['utt']  #uttにはユーザの入力した文字列が入っている
        # uttに'名前'
        emotion_analyzer = MLAsk()
        json_emot = emotion_analyzer.analyze(utt)
        utt = self.tagger.parse(utt)
        # 対応するセッションのkernelを取り出し，respondでマッチするルールを探す
        response = self.sessiondic[sessionId].respond(utt)
        emotion = json_emot['representative'][0]
        return {'utt': response + emotion_dic[emotion], 'end':False}
    
if __name__ == '__main__':
    system = AimlSystem()
    bot = TelegramBot(system)
    bot.run()
