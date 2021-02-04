import yagmail

class Mail:
    def sendMail(self,msg,title,receivers):
        yag = yagmail.SMTP(
            host='smtp.office365.com',port='587',user='ikangbow@outlook.com',password='131468kbw',smtp_ssl=False
        )
        try:
            yag.send(receivers,title,msg)
            print("send success")
        except BaseException as e:
            print(e)
            print("error send fail")

if __name__ == '__main__':
    Mail().sendMail("wowowo","hello","1078162876@qq.com")