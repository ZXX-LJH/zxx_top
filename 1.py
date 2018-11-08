#获取个人微信号中朋友信息
#导入itchat包
import itchat

#获取个人微信号好友信息
if __name__=="__main__":
    #登录个人微信，扫码登录
    itchat.login()
    #爬取自己好友相关信息
    friends=itchat.get_friends(update=False)[0:]
    #设置需要爬取的信息字段
    # result=[('RemarkName','备注'),('NickName','微信昵称'),('Sex','性别'),('City','城市'),('Province','省份'),('ContactFlag','联系标识'),('UserName','用户名'),('SnsFlag','渠道标识'),('Signature','个性签名')]
    # for user in friends:
    #     with open('myFriends.txt','a',encoding='utf8') as fh:
    #         fh.write("-----------------------\n")
    #     for r in result:
    #         with open('myFriends.txt','a',encoding='utf8') as fh:
    #             fh.write(r[1]+":"+str(user.get(r[0]))+"\n")

    for user in friends:
        with open('myFriends.txt','a',encoding='utf8') as fh:
            fh.write("-----------------------\n")
        for k, v in user.items():
            with open('myFriends.txt','a',encoding='utf8') as fh:
                fh.write(k +":"+str(v)+"\n")

    print("完成")

# {'MemberList': <ContactList: []>, 'Uin': 0, 'UserName': '@41f5c66a7cbe971d607b25367042db7ebb092e73e519285598c6f6fe1eadd63c', 'NickName': '多尔衮滚滚滚滚滚滚滚滚滚', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=682162114&username=@41f5c66a7cbe971d607b25367042db7ebb092e73e519285598c6f6fe1eadd63c&skey=@crypt_739d6c51_a94cfb8f77b8415001dad1204c481ea0', 'ContactFlag': 3, 'MemberCount': 0, 'RemarkName': '张静啊', 'HideInputBarFlag': 0, 'Sex': 2, 'Signature': '', 'VerifyFlag': 0, 'OwnerUin': 0, 'PYInitial': 'DEGGGGGGGGGG', 'PYQuanPin': 'duoergungungungungungungungungungun', 'RemarkPYInitial': 'ZJA', 'RemarkPYQuanPin': 'zhangjinga', 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 0, 'AttrStatus': 129469, 'Province': '', 'City': '', 'Alias': '', 'SnsFlag': 17, 'UniFriend': 0, 'DisplayName': '', 'ChatRoomId': 0, 'KeyWord': '', 'EncryChatRoomId': '', 'IsOwner': 0}