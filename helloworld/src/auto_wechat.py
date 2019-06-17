import itchat
import time
import names
import requests
import json
import threading
from apscheduler.schedulers.background import BackgroundScheduler
from MyQueue import MyQueue

global wx_config
words=('你个傻吊','不要回复')

class wx_config(object):
    registerType = ['Picture', 'Recording', 'Attachment', 'Video', 'Text', 'Map', 'Card', 'Note', 'Sharing']
    downType = ['Picture', 'Recording', 'Attachment', 'Video']
    def __init__(self):
        self.myName = ''
        self.filePath = ''
        self.reqbody = {'reqType': 0, 'perception': {}, 'userInfo': {}}
        self.mps = []
        self.queue = MyQueue()
    def initConfig(self):
        self.myName = itchat.get_friends(update=True)[0]['UserName']
        self.filePath = 'E:/wechatFile/'
        self.mps = itchat.search_mps(name='小冰')

    # s1 = str(10006)
    # s2 = str(40006)
    # print(s1.startswith("100"))
    # print(s2.startswith("100"))
    #  invokeApi('天气如何')


# @itchat.msg_register(registerType, isGroupChat=True)
# def group_reply(msg):
#     print(msg)
#     print("=====")

#   调用图灵api
# def invokeApi(input):
#     reqbody['reqType'] = 0
#     reqbody['perception'] = {
#         'inputText': {
#             'text': input
#         },
#         'selfInfo': {
#             'location': {
#                 'city': '北京',
#                 'province': '北京',
#                 'street': '信息路'
#             }
#         }
#     }
#     reqbody['userInfo'] = {
#         'apiKey': '4453d0f556764fac9fdd501c6f0c26bb',
#         'userId': 'tomcatx001'
#     }
#     req = json.dumps(reqbody, ensure_ascii=False)
#     url = 'http://openapi.tuling123.com/openapi/api/v2'
#     response = requests.post(url, req.encode('utf-8'))
#     conetent = response.content.decode('utf-8')
#     conetent = json.loads(conetent)
#     print(conetent)
#     return conetent
# itchat 封装好下载方法 并指定下载路径

def downFile(wx_config, msg):
    if not msg['User']['UserName'] == 'filehelper':
        print('download to path : %s...'%(wx_config.filePath))
        msg.download(wx_config.filePath + msg['FileName'])

# 注册监听消息事件
@itchat.msg_register(wx_config.registerType, isFriendChat=True)
def text_ly(msg):
    print("收到消息,Type : %s" % (msg['Type']))
    #只接收好友的消息，过滤掉自己的消息
    if not msg['FromUserName'] == wx_config.myName:
        wx_config.queue.enqueue(msg['FromUserName'])
        print("enqueue user %s" % (msg['FromUserName']))
    # 如果收到的是图片视频等下载资源，保存到本机
        if msg['Type'] in wx_config.downType:
            downFile(wx_config, msg)
        else:
            # 收到的文字信息，自动回复
            if not msg['FromUserName'] == wx_config.myName:
                # 发送一条提示给文件助手
                itchat.send_msg(u"[%s]收到好友@%s 的信息：%s\n" %
                                (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(msg['CreateTime'])),
                                 msg['User']['NickName'],
                                 msg['Text']), 'filehelper')

                # response = invokeApi(msg['Text'])
                # intent = response['intent']
                # resluts = response['results']
                #
                # code = intent['code']
                # if str(code).startswith("1"):
                #     out = resluts[0]['values']['text']
                #     return out
        send_toXiaoBing(wx_config, msg)
    # return "正在忙，已收到你消息，稍后回复"


# 发送消息给小冰
def send_toXiaoBing(wx_config, msg):
    if msg['Type'] == 'Text':
        itchat.send_msg(msg['Text'], wx_config.mps[0]['UserName'])
        return
    if msg['Type'] == 'Picture':
        itchat.send_image(wx_config.filePath + msg['FileName'], wx_config.mps[0]['UserName'])
        return
    if msg['Type'] == 'Recording':
        itchat.send_file(wx_config.filePath + msg['FileName'], wx_config.mps[0]['UserName'])
        return

@itchat.msg_register(wx_config.registerType, isMpChat=True)
def mp_reply(msg):
    if msg['User']['NickName'] == '小冰':
        recall(wx_config,msg)


def recall(wx_config, msg):
    if wx_config.queue.isEmpty():
        return
    print('recall')
    touser = wx_config.queue.dequeue()
    if touser:
        if msg['Type'] == 'Text':
            itchat.send_msg(msg['Text'], touser)
        elif msg['Type'] == 'Picture':
            downFile(wx_config,msg)
            itchat.send_image(wx_config.filePath + msg['FileName'], touser)
        else:
            downFile(wx_config,msg)
            itchat.send_file(wx_config.filePath + msg['FileName'], touser)
    else:
        return

def send_msg_to_someone(userName):
    itchat.send_msg('你个傻吊，不要回答', toUserName=userName)
    print('发送成功')

def scheduleTask():
    print('线程开启，任务开始')
    userInfo = itchat.search_friends(nickName='黄耀辉')
    print(userInfo[0])
    if len(userInfo) > 0:
        scheduler = BackgroundScheduler()
        scheduler.add_job(send_msg_to_someone, 'interval', seconds=1, args=[userInfo[0]['UserName']])
        scheduler.start()

if __name__ == '__main__':
    wx_config = wx_config()
    itchat.auto_login(hotReload=True);
    wx_config.initConfig()
    #threading.Thread(target=scheduleTask(),args=[]).start()
    print("主线程执行中")
    itchat.run()
    itchat.dump_login_status