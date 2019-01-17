
from jenkins.permission.permission_list import perm_dic
from django.core.urlresolvers import resolve
from jenkins import models
from django.shortcuts import HttpResponse, redirect, render
from account.views import login_auth



def perm(request, *args, **kwargs):
    _username = request.session.get('_username', None)
    if _username:
        user = models.User.objects.get(username=_username)
        if user.is_admin:  # 是管理员
            return True

    if args:
        project_id = args[0]
        if  _username:
            user = models.User.objects.get(username=_username)
            project_perm = ['jenkins.can_show_project', 'jenkins.can_upload_files', 'jenkins.can_del_project', 'jenkins.can_configure_project', 'jenkins.can_build_project', ]
            for k, v in perm_dic.items():
                if k in project_perm:#是项目相关权限
                    url_match = False
                    if v['url_type'] == 0: # url是别名
                        if v['url'] == resolve(request.path).url_name:#url别名相等
                            url_match = True

                    else:#url是绝对地址
                        if v['url'] == request.path:#url绝对路径相等
                            url_match = True


                    if url_match and v['method'] == request.method:#url和方法都匹配上了
                        perm_list = user.permiss.all()
                        for perm in perm_list:
                            if perm.project.id == int(project_id) and getattr(perm, v['action'], 0) == 1:  # 就是这个项目了
                                    return True




    return False


def check_perm(func):
    def inner(request, *args, **kwargs):
        if perm(request, *args, **kwargs):#有权限
            return func(request, *args, **kwargs)
        else:
            return HttpResponse('没权限！')
    return inner