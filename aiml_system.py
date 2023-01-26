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
        sessionId = input['sessionId']
        utt = input['utt']  #uttにはユーザの入力した文字列が入っている
        print(utt)
        # uttに'名前'が入っていないときは感情分析を行う
        if '名前' not in utt:
            flag = 1
            emotion_analyzer = MLAsk()
            json_emot = emotion_analyzer.analyze(utt)
            #ニュートラルに分類されるときの処理
            if json_emot['emotion'] == None:
                flag = -1
        else:
            flag = 0
        utt = self.tagger.parse(utt)
        # 対応するセッションのkernelを取り出し，respondでマッチするルールを探す
        response = self.sessiondic[sessionId].respond(utt)
        if flag == -1:
            #感情が読み取れなかったとき(ニュートラル)
            return {'utt': response + '😑', 'end':False}
        if flag:
            print(sessionId, utt, response)
            if 'POSITIVE' in json_emot['orientation']:
                return {'utt': response + '😆', 'end':False}
            else:
                return {'utt': response + '😭', 'end':False}
        else:
            print(sessionId, utt, response)
            return {'utt': response, 'end':False}

if __name__ == '__main__':
    system = AimlSystem()
    bot = TelegramBot(system)
    bot.run()
