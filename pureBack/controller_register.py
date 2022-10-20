import json
import smtplib
import sys
from email.mime.text import MIMEText
from email.header import Header
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from vuedata.models import userTable
from loguru import logger
import bcrypt

logger.remove()  # 这里是不让他重复打印
logger.add(sys.stderr,  # 这里是不让他重复打印
           level="INFO"
           )

@csrf_exempt
def register_format(request):
    req = json.loads(request.body)
    to_addr1 = req['username']
    to_addr2 = req['sex']
    to_addr3 = req['password']
    to_addr4 = req['birthday']
    to_addr5 = req['phone']
    to_addr6 = req['email']
    print(req)
    flag = 0
    li = list(userTable.objects.filter(UserName=to_addr1))

    print(li)
    if len(li)>0:
        flag=1
    for i in li:
        print(i.UserName)
    if flag==0:
        salt=bcrypt.gensalt()
        hashed=bcrypt.hashpw(to_addr3.encode(),salt)
        print(f"salt:{salt}")
        print(f"hashed:{hashed}")
        data=userTable(UserName=to_addr1,Sex=to_addr2,Password=hashed,Birthday=to_addr4,Phone=to_addr5,Email=to_addr6,Salt=salt)
        data.save()


    logger.add('user.log', encoding='utf-8',format="{time}  |   {message}")
    if flag==0:
        logger.info(f'[注册]:{to_addr1}')
        return JsonResponse({
            "success": True,
            "hasB4": False
        })
    else:
        logger.info(f'[注册失败]:')
        return JsonResponse({
            "success": False,
            "hasB4": True
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




