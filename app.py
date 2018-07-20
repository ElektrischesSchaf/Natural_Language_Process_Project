import sys
from io import BytesIO
import telegram
from flask import Flask, request, send_file
##
import time
import requests
import json
import datetime
import sys
from firebase import firebase
import globalstate
import updater
##
import time
firebase=firebase.FirebaseApplication('https://***.firebaseio.com/',None)
sys.path.append("../")
import jieba
jieba.load_userdict("userdict.txt")
import jieba.posseg as pseg


API_TOKEN = '***'
WEBHOOK_URL = 'https://***.herokuapp.com/'
app = Flask(__name__)
bot = telegram.Bot(token='***')

'''
def set_state(x):
    state=x
    print('state has been set to ')
    print (state)
    return x

def show_state():
    if state==1:
        return 1
    if state==2:
        return 2
    if state==3:
        return 3
    if state==0:
        return 0
'''



@app.route('/',methods=['GET'] )
def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))
    return "Hello World<p> This is ElektrischesSchaf NLP Bot Heroku-deployed python program !!!",200



@app.route('/', methods=['POST'])
def webhook_handler():
    if request.method == "POST":
        t=time.time()
        date=datetime.datetime.fromtimestamp(t).strftime('%Y%m%d%H%M%S')

        update = telegram.Update.de_json(request.get_json(force=True),bot)
        chat_id = update.message.chat.id
        username=update.message.chat.last_name
        try:
            text = update.message.text.encode('utf-8')
        except AttributeError:
            text=update.message.text
        #text=update.message.text
        #text=text.encode('utf-8')

        if text:
            text=text.decode('utf-8')
        print(text)
        if text=='NLP':
            bot.sendMessage(chat_id=chat_id, text='yes')
            print('get NLP form')
            print(chat_id)
        if text:
            if text.startswith('$'):
                if username:
                    dict = {'Date': date, 'Emotion': '', 'Intention': '','Username':username};
                else:
                    dict={'Date': date, 'Emotion': '', 'Intention': '','Username':'Unknow'};
                text=text[1:]
                result=pseg.cut(text)
                print(result)
                for w in result:
                    if w.flag=='happy':
                        dict['Emotion']='happy'
                    if w.flag=='sad':
                        dict['Emotion']='sad'
                    if w.flag=='move':
                        dict['Intention']=w.word
                result=firebase.patch('/Telegram'+'/'+str(date),{'Emotion':dict['Emotion'],'Intention':dict['Intention'],'User':dict['Username']})
                bot.sendMessage(chat_id=chat_id,text='Emotion and intention recorded')
            if text.startswith('!result'):
                result = firebase.get('/Telegram',None,params={'print': 'pretty'},headers={'X_FANCY_HEADER': 'very fancy'})
                if result:
                    result=list(result.values())
                    print(result)
                    bot.sendMessage(chat_id=chat_id,text='總共紀錄'+str(len(result))+'條訊息')
                    bot.sendMessage(chat_id=chat_id,text='所記錄情緒:')
                    yoyo=[]
                    for w in range(len(result)):
                        print(result[w]['Emotion'])
                        yoyo.append(result[w]['Emotion'])
                        yoyodiy = ', '.join(yoyo)
                    #print(yoyo)
                    print(yoyodiy)
                    bot.sendMessage(chat_id=chat_id,text=yoyodiy)
                    bot.sendMessage(chat_id=chat_id,text='所記錄動作:')
                    yoyo=[]
                    for w in range(len(result)):
                        print(result[w]['Intention'])
                        yoyo.append(result[w]['Intention'])
                        yoyodiy=', '.join(yoyo)
                    #print(yoyo) 
                    print(yoyodiy)
                    bot.sendMessage(chat_id=chat_id,text=yoyodiy)
                    ############################記錄人
                    bot.sendMessage(chat_id=chat_id,text='記錄人:')
                    yoyo=[]
                    for w in range(len(result)):
                        print(result[w]['User'])
                        yoyo.append(result[w]['User'])
                        yoyodiy=', '.join(yoyo)
                    #print(yoyo) 
                    print(yoyodiy)
                    bot.sendMessage(chat_id=chat_id,text=yoyodiy)
                    ###################################
                else:
                    bot.sendMessage(chat_id=chat_id,text='Firebase Database is empty!')
            if text.startswith('!delete'):
                firebase.delete('/Telegram',None)
                bot.sendMessage(chat_id=chat_id,text='資料庫已經空 Firebase data deleted')
            if text.startswith('seg='):
                #bot.sendMessage(chat_id=chat_id, text=text)
                text=text[4:]
                #text.replace(" ", "")
                result=pseg.cut(text)
                print(result)
                for w in result:
                    if w.word != ' ' and w.word !='　'and w.word!='\n' and w.word !='\r\n':
                        print(w.word)
                        bot.sendMessage(chat_id=chat_id, text=w.word)
            #if text.startswith('pos='):
                #text=text[4:]
                #result=pseg.cut(text)
                #print(result)
                #for w in result:
                    #if(w.flag=='positive'):
                        #bot.sendMessage(chat_id=chat_id,text='tag: positive')
                        #bot.sendMessage(chat_id=chat_id,text=w.word)
                    #if(w.flag=='negative'):
                        #bot.sendMessage(chat_id=chat_id,text='tag: negative')
                        #bot.sendMessage(chat_id=chat_id,text=w.word)
            if text.startswith('play music'):
                print ('playing')
                bot.sendAudio(chat_id=chat_id,audio='CQADBQADOQAD1KPoVHjBXgkKYx1mAg' ,caption='Richard Wagner - Das Rheingold Act II')
            if text.startswith('firebase='):
                text=text[9:]
                print('print to firebase:')
                firebase.post('/Telegram',{'User':'one','Date':date,'Text':text})
                print(text)
            if text.startswith('New security code'):
                bot.sendMessage(chat_id=chat_id,text='Welcome, how may I help you?')
            if text.startswith('How about some music'):
                bot.sendMessage(chat_id=chat_id,text='Selection?')
            if text.startswith('Richard Wagner'):
                bot.sendMessage(chat_id=chat_id,text='Yes, David. As you wish.')
                bot.sendAudio(chat_id=chat_id,audio='CQADBQADOQAD1KPoVHjBXgkKYx1mAg' ,caption='Richard Wagner - Das Rheingold Act II')
            #if text=='show state':
                #bot.sendMessage(chat_id=chat_id,text=str(state))
            if text=='state to 1':
                updater.stuff(1) 
                print('now state=')
                print(globalstate.state)
            if text=='state to 2':
                updater.stuff(2) 
                print('now state=')
                print(globalstate.state)
            if text=='state to 3':
                updater.stuff(3) 
                print('now state=')
                print(globalstate.state)
            if text=='clear state':
                updater.stuff(0) 
                print('now state=')
                print(globalstate.state)
            if text=='show':
                #haha=globalstate.state
                print('show state')
                print(globalstate.state)
                if globalstate.state==1:
                    bot.sendMessage(chat_id=chat_id,text='in state 1')
                if globalstate.state==2:
                    bot.sendMessage(chat_id=chat_id,text='in state 2')
                if globalstate.state==3:
                    bot.sendMessage(chat_id=chat_id,text='in state 3')
                if globalstate.state==0:
                    bot.sendMessage(chat_id=chat_id,text='in state 0')
    print('get message by POST')
    return 'ok'
'''
                print(state)
                if state==0:
                    #print(state)
                    bot.sendMessage(chat_id=chat_id,text='in state 0')
                if state==1:
                    #print(state)
                    bot.sendMessage(chat_id=chat_id,text='in state 1')
                if state==2:
                    #print(state)
                    bot.sendMessage(chat_id=chat_id,text='in state 2')
                if state==3:
                    #print(state)
                    bot.sendMessage(chat_id=chat_id,text='in state 3')
'''


if __name__ == "__main__":
    _set_webhook()
    app.run()