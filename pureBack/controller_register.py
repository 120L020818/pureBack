import json
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def register_format(request):
    req = json.loads(request.body)
    to_addr = req['email']
    print(req)
    if True:
        return JsonResponse({
            "success": True,
        })
    else:
        return JsonResponse({
            "success": False,
        })

@csrf_exempt
def register_email(request):

    from_addr = '565852435@qq.com'
    password='gplblhngalnybfhe'

    req=json.loads(request.body)
    to_addr=req['email']

    smtp_server='smtp.qq.com'

    list1=list(range(97,123))
    list2=list(range(65,91))
    list3=list(range(48,58))
    list4=list1+list2+list3
    # 总共62个元素
    space=[chr(i) for i in list4]
    captcha=''
    for i in range(0,5):
        captcha=captcha+(space[random.randint(0, 61)])
    print(captcha)
    msg = MIMEText(f'您的注册验证码为:{captcha},感谢您的使用!','plain','utf-8')
    msg['From']=Header('天际CA管理系统')
    msg['To'] = Header('用户')
    msg['Subject']=Header('天际CA管理系统验证邮件')


    server = smtplib.SMTP_SSL(smtp_server)
    server.connect(smtp_server,465)

    server.login(from_addr, password)

    server.sendmail(from_addr, to_addr, msg.as_string())
    # 关闭服务器
    server.quit()
    return JsonResponse({
        "success": True,
        "captcha":captcha,
    })




