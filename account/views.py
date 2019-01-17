from django.shortcuts import render, redirect, HttpResponse
from jenkins import utils, models
# Create your views here.


def login_auth(func):
    def inner(request, *args, **kwargs):
        if request.session.get('_username'):
            return func(request, *args, **kwargs)
        else:
            return redirect( '/account/login/') #没session就去登陆吧
    return inner

def login(request):
    # print('-->accout request.session type--', type(request.session))
    # print('-->account request.session--', request.session)
    # for k, v in request.session.items():
    #     print(k, v)
    _username = request.session.get('_username')
    if _username:#已有session
        print('-->session类型',type(request.session))
        print('-->session dir--》', dir(request.session))
        print('--get age',request.session.get_expiry_age())
        print('-->get date',request.session.get_expiry_date())
        return redirect('/jenkins/') #跳到主页

    elif request.method == 'POST':#没有session
        _username = request.POST.get('_username')
        _password = request.POST.get('_password')
        md5_pass = utils.get_md5_value(_password)
        if models.User.objects.filter(username=_username, password=md5_pass):
            request.session['_username'] = _username
            request.session.set_expiry(3600*24) #一天后失效
            return redirect('/jenkins/')

    return render(request, 'account/login.html')  #既没session，用户密码又不对，就继续再登陆吧

def logout(request):
    username = request.session.get('_username')
    if username:
        del request.session['_username']
    return redirect('/account/login/')


def user_index(request, username):
    err_msg = ''
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        md5_old_pass = utils.get_md5_value(old_password)
        user = models.User.objects.get(username=username)

        if md5_old_pass == user.password and new_password1 == new_password2 and new_password1:
            user.password = utils.get_md5_value(new_password1)
            user.save()
            err_msg = '修改密码成功!'
        elif md5_old_pass != user.password:
            err_msg = '原密码不对，修改密码失败!'
        elif not new_password1 or not new_password2:
            err_msg = '密码不能为空，修改密码失败!'
        elif new_password1 != new_password2:
            err_msg = '两次新密码不一致，修改密码失败!'
        else:
            err_msg = '修改密码失败!'


    return render(request, 'account/user_index.html', {
        'username':username,
        'err_msg': err_msg,

    })