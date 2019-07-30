# coding:utf-8
from django.shortcuts import redirect
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils.crypto import get_random_string
import hashlib
import datetime
from users.models import User,Radcheck,ConfirmString,Radacct
from users import forms
from django.shortcuts import render
from django_tables2 import RequestConfig
from users.models import Radpostauth,Radusergroup
from users.tables import AuthLogTable,AccLogTable
# Create your views here.


def send_email(email,subject,html_content):

    text_content = '''欢迎注册'''+settings.COMPANY+'''VPN账号！\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    ConfirmString.objects.create(code=code, user=user,)
    return code

def hash_code(s, salt='mysite'):# 加点盐
    h = hashlib.sha256()
    m = s+salt
    h.update(m.encode())  # update方法只接收bytes类型
    return h.hexdigest()


# Create your views here.
def index(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    username = request.session.get("user_name")
    authlog = AuthLogTable(Radpostauth.objects.filter(username=username))
    RequestConfig(request, paginate={'per_page': 10}).configure(authlog)
    acclog = AccLogTable(Radacct.objects.filter(username=username))
    RequestConfig(request, paginate={'per_page': 10}).configure(acclog)

    return render(request, 'index.html', locals())

def login(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/index/')
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            try:
                user = User.objects.get(name=username)
            except :
                message = '用户不存在！'
                return render(request, 'login.html', locals())

            if not user.has_confirmed:
                message = '该用户还未经过邮件确认！'
                return render(request, 'login.html', locals())

            if not user.in_office:
                message = '该用户已离职！'
                return render(request, 'login.html', locals())

            if user.password == password:
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/index/')
            else:
                message = '密码不正确！'
                return render(request, 'login.html', locals())
        else:
            return render(request, 'login.html', locals())
    message = request.GET.get('message', '')
    login_form = forms.UserForm()
    return render(request, 'login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            if email.split('@')[-1] != settings.EMAIL_HOST_USER.split('@')[-1]:
                message = '请使用'+settings.COMPANY+'公司邮箱！'
                return render(request, 'register.html', locals())

            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'register.html', locals())
            else:
                same_name_user = User.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'register.html', locals())
                same_email_user = User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经被注册了！'
                    return render(request, 'register.html', locals())

                new_user = User()
                new_user.name = username
                new_user.password = password1
                new_user.email = email
                new_user.save()

                subject = settings.COMPANY+'VPN注册确认邮件'
                code = make_confirm_string(new_user)
                addr = settings.VPN_HOST+":"+settings.VPN_WEB_PORT
                html_content = '''
                                    <p>欢迎注册{4}VPN账号！</p>
                                    <p>请点击站点链接完成注册确认！<a href="{0}/confirm/?code={1}" target=blank>{2}</a></p>
                                    <p>此链接有效期为{3}天！</p>
                                    '''.format(addr,code,addr, settings.CONFIRM_DAYS,settings.COMPANY)
                try:
                    send_email(email, subject,html_content)
                except:
                    message = "发送邮件失败，请联系管理员"
                message = '请前往邮箱进行确认！'
                return render(request, 'confirm.html', locals())
        else:
            message = '输入格式有误，后台校验不通过！'
            return render(request, 'register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')

    request.session.flush()
    # del request.session['is_login']
    return redirect("/login/")

def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
        return render(request, 'confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        username = confirm.user.name
        password = confirm.user.password


        # 创建新用户
        vpn_user = Radcheck()
        vpn_user.username = username
        vpn_user.attribute = "Cleartext-Password"
        vpn_user.op = ":="
        vpn_user.value = password
        vpn_user.save()
        # 添加默认组
        vpn_user_group = Radusergroup()
        vpn_user_group.username = username
        vpn_user_group.groupname = "default"
        vpn_user_group.priority = "50"
        vpn_user_group.save()

        message = '感谢确认，请使用账户登录！'
        return render(request, 'confirm.html', locals())


def pwd_change(request):
    if not request.session.get('is_login', None):
        return redirect('/login/?message=登录后更改密码')
    if request.method == "POST":
        pwd_change_form = forms.PwdChangeForm(request.POST)
        message = "请检查填写的内容！"
        if pwd_change_form.is_valid():
            old_password = pwd_change_form.cleaned_data.get('old_password')
            new1 = pwd_change_form.cleaned_data.get('new1')
            new2 = pwd_change_form.cleaned_data.get('new2')
            username = request.session.get("user_name")

            user = User.objects.get(name=username)

            if user.password == old_password:
                if new1 != new2:
                    message = '两次输入的密码不同！'
                    return render(request, 'pwd_change.html', locals())
            else:
                message = '旧密码不对！'
                return render(request, 'pwd_change.html', locals())
            user.password = new1
            user.save()
            vpn_user = Radcheck.objects.get(username=username)
            vpn_user.value = new1
            vpn_user.save()
            request.session.flush()

            return redirect('/login/?message=密码修改成功,请重新登录')
    pwd_change_form = forms.PwdChangeForm()
    return render(request, 'pwd_change.html', locals())

def pwd_reset(request):
    if request.method == "POST":
        pwd_reset_form = forms.PwdResetForm(request.POST)
        message = "请检查填写的内容！"
        if pwd_reset_form.is_valid():
            username = pwd_reset_form.cleaned_data.get('username')
            email = pwd_reset_form.cleaned_data.get('email')
            try:
                user = User.objects.get(name=username)
            except:
                message = '用户不存在！'
                return render(request, 'pwd_reset.html', locals())
            if user.email != email:
                message="用户名与邮件地址不符"
                return render(request, 'pwd_reset.html', locals())
            password = get_random_string(length=12)
            user.password = password
            user.save()
            subject = settings.COMPANY+'VPN密码重置确认邮件'
            addr = settings.VPN_HOST + ":" + settings.VPN_WEB_PORT
            html_content = '''<p>{}您的VPN密码已经被重置，你可以到此链接进行密码更改<a href="{}/pwd_change/" target=blank>{}/pwd_change/</a>，\</p>
                            <p>初始化密码为{} ,重置密码后方可登录VPN。</p>'''.format(username,addr,addr,password)
            try:
                send_email(email, subject, html_content)
            except :
                message="邮件发送失败请联系管理员"
                return render(request, 'pwd_reset.html', locals())

            return redirect('/login/?message=密码已重置，并通过邮件发送')
        return render(request, 'pwd_reset.html', locals())
    pwd_reset_form = forms.PwdResetForm()
    return render(request, 'pwd_reset.html', locals())
