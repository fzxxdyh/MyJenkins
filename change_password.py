<<<<<<< HEAD


def change_password(_username, _password1, _password2):
    if  _password1 and  _password1 == _password2:
        md5_password = utils.get_md5_value(_password1)
        user = User.objects.get(username=_username)
        user.password = md5_password
        user.save()
        return True


if __name__ == '__main__':
    import os
    import django
    import getpass
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyJenkins.settings')
    django.setup()
    from jenkins.models import User
    from jenkins import utils
    _username = input('请输入用户名：').strip()
    if _username:
        _password1 = getpass.getpass('请输入密码：')
        _password2 = getpass.getpass('请确认密码：')
        if change_password(_username, _password1, _password2):
            print('用户密码重置成功！')
        else:
            print('用户密码重置失败')

=======


def change_password(_username, _password1, _password2):
    if  _password1 and  _password1 == _password2:
        md5_password = utils.get_md5_value(_password1)
        user = User.objects.get(username=_username)
        user.password = md5_password
        user.save()
        return True


if __name__ == '__main__':
    import os
    import django
    import getpass
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyJenkins.settings')
    django.setup()
    from jenkins.models import User
    from jenkins import utils
    _username = input('请输入用户名：').strip()
    if _username:
        _password1 = getpass.getpass('请输入密码：')
        _password2 = getpass.getpass('请确认密码：')
        if change_password(_username, _password1, _password2):
            print('用户密码重置成功！')
        else:
            print('用户密码重置失败')

>>>>>>> '--init--'
