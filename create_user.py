<<<<<<< HEAD


def create_user(_username, _password, _is_admin):
    md5_password = utils.get_md5_value(_password)
    if _is_admin.upper() == 'Y':
        admin_flag = True
    else:
        admin_flag = False
    user = User(username=_username, password=md5_password, is_admin=admin_flag)
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
        _is_admin = input('是管理员？, 是【Y】, 不是【N】: ').strip()
        if _password1 and _password1 == _password2:
            if create_user(_username, _password1, _is_admin):
                print('创建用户成功')
            else:
                print('创建用户失败')
        else:
            print('密码不能为空 or 两次密码需一致')
    else:
        print('用户名不能为空')

=======


def create_user(_username, _password, _is_admin):
    md5_password = utils.get_md5_value(_password)
    if _is_admin.upper() == 'Y':
        admin_flag = True
    else:
        admin_flag = False
    user = User(username=_username, password=md5_password, is_admin=admin_flag)
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
        _is_admin = input('是管理员？, 是【Y】, 不是【N】: ').strip()
        if _password1 and _password1 == _password2:
            if create_user(_username, _password1, _is_admin):
                print('创建用户成功')
            else:
                print('创建用户失败')
        else:
            print('密码不能为空 or 两次密码需一致')
    else:
        print('用户名不能为空')

>>>>>>> '--init--'
