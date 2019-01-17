from django.shortcuts import render, HttpResponse, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from account.views import login_auth
from jenkins import models
import os
import locale
import subprocess
from MyJenkins import settings
import datetime, time
from jenkins.enable_tables import enable_tables
from jenkins.forms import create_model_form
from django.core.urlresolvers import resolve
from jenkins.permission import check_perm
from jenkins.utils import rmdir_all
import json






@login_auth
def jenkins_index(request):
    _username = request.session.get('_username', None) #即使后面不加None，找不到也会返回默认None
    try:
        user = models.User.objects.get(username=_username) #查不到会报jenkins.models.DoesNotExist异常
    except models.User.DoesNotExist:
        # print('用户不存在！')
        return redirect('/account/login/')

    object_list = []
    if user.is_admin:
        object_list = models.Project.objects.all().order_by('project_name') #id降序
    else:
        permiss = user.permiss.all() # 是一个查询集
        for per in permiss:
            object_list.append(per.project) #p.project是一个model
        # sorted(object_list)
    paginator = Paginator(object_list, 20) # 每页10条
    page = request.GET.get('page')  # 找不到就为None,触发后面PageNotAnInteger异常
    try:
        query_sets = paginator.page(page)
    except PageNotAnInteger:  # 如果page为None，就会触发这个异常
        # If page is not an integer, deliver first page.
        query_sets = paginator.page(1)
    except EmptyPage: #大于paginator.num_pages或者小于1
        # If page is out of range (e.g. 9999), deliver last page of results.
        query_sets = paginator.page(paginator.num_pages)
    return  render(request, 'jenkins/jenkins_index.html', {'username': _username,
                                                    'query_sets': query_sets,
                                                           'user': user,
                                                           })


@login_auth
@check_perm.check_perm
def project_new(request):
    username = request.session.get('_username')
    if request.method == 'POST':
        projectname = request.POST.get('project_name')
        projectnote = request.POST.get('project_note')
        projectscript = request.POST.get('project_script')
        if models.Project.objects.filter(project_name=projectname):
            return HttpResponse('项目[ %s ]已存在！' % projectname)
        else:
            project = models.Project(project_name=projectname, project_note=projectnote, project_script=projectscript)
            project.save()
            folders = [ 'history', 'upload']
            for f in folders:
                project_dir = os.path.join(settings.BASE_DIR, f, projectname)
                # print('要创建的目录：', project_dir)
                if not os.path.exists(project_dir):
                    os.makedirs(project_dir)
            return redirect('/jenkins/')

    return  render(request, 'jenkins/project_new.html', {'username': username})


@login_auth
@check_perm.check_perm
def project_info(request, project_id):
    if request.GET.get('path'):#是ajax发送的查询
        res = {}
        res['folders'] = []
        res['files'] = []
        path = request.GET.get('path')
        # print('后端get接收的path:', path)
        project_name = path.split('>')[0]

        user_folder = os.listdir(  os.path.join(settings.UPLOAD_DIR, project_name) ) #正常情况下当前目录只包含一个子目录,如当前目录不存在，会报FileNotFoundError异常
        if user_folder: # user_folder是一个列表，可能为空，不为空代表目录下有内容
            user_folder = user_folder[0] #正常情况下只有一个目录
        else:
            return HttpResponse(json.dumps(res), content_type="application/json") #没有内容，返回空字典

        path = path.split('>')[1:]#列表，去掉开头的项目名称
        project_home = os.path.join(settings.UPLOAD_DIR, project_name, user_folder)
        current_path = os.path.join(project_home, os.sep.join(path))
        for f in sorted(os.listdir(current_path)):
            if os.path.isdir(os.path.join(current_path, f)):
                res['folders'].append(f)
            else:
                res['files'].append(f)
        # print('path里',res)
        return HttpResponse(json.dumps(res), content_type="application/json" )



    # file_project = ["test_trade", "test_auction", "online_trade", "online_auction",]
    # print('resolve-->', resolve(request.path).url_name) #把url解释成别名
    noupload_project = ["online_manage", "online_datang_backend1", "online_datang_backend2"]
    username = request.session.get('_username')
    if request.method == 'POST':#上传文件
        type = request.POST.get('type')
        path = request.POST.get('path')
        # print('后端POST接收到的path', path)
        file_list = request.FILES.getlist('file_list')
        if not file_list:#发送了一个空的post
            return HttpResponse('没有选择文件！')
        # print('共有：%s 已接收：%s' % (file_sum, file_send))
        project = models.Project.objects.get(id=project_id)
        project.project_status = 2  # 项目正在上传文件
        project.save()

        upload_dir = os.path.join(settings.BASE_DIR, 'upload', project.project_name)
        # print('upload_dir>>>', upload_dir)
        if  type == 'full':#全目录上传
            # print(request.META['PATH_INFO'])
            # print('getlist-->', request.FILES.getlist('file_list'))
            # print('get--->', request.FILES.get('file_list'))
            '''
            print(dir(list_files[0]))
            ['DEFAULT_CHUNK_SIZE', '__bool__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__enter__', '__eq__', '__exit__', '__format__', 
            '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__iter__', '__le__', '__len__', '__lt__', '__module__', '__ne__', '__new__',
             '__nonzero__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_get_closed',
              '_get_name', '_get_size', '_get_size_from_underlying_file', '_name', '_set_name', '_set_size', '_size',
    
             'charset', 'chunks', 'close', 'closed', 'content_type', 'content_type_extra', 'encoding', 'field_name', 'file', 'fileno', 
             'flush', 'isatty', 'multiple_chunks', 'name', 'newlines', 'open', 'read', 'readinto', 'readline', 'readlines', 'seek', 
             'seekable', 'size', 'softspace', 'tell', 'truncate', 'write', 'writelines', 'xreadlines']
    
            DEFAULT_CHUNK_SIZE--> 65536
            '''
            # obj = request.FILES.get('upload_files')  这种方式只能获取到一个文件

            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)


            rmdir_all(upload_dir)  # 清空目录，不删除目录本身

            for fobj in file_list:
                # print('文件名：', fobj.name) # 测试<:>sub1<:>sub2#upload.inf
                # start_ind = fobj.name.find('|')
                end_ind = fobj.name.rfind('#')  # 找不到会返回 -1
                # str_fdate = fobj.name[0:start_ind]
                # print('修改日期', str_fdate)
                # str_fdate = format_date(str_fdate)
                file_path_rel = os.sep.join(fobj.name[0:end_ind].split("<:>"))  # 字符串，文件相对路径,包括用户自定义的目录
                file_path_abs = os.path.join(upload_dir, file_path_rel)  #文件绝对路径，不包括文件名

                filename = fobj.name[end_ind+1:]  #仅仅是文件名


                folder = os.path.exists(file_path_abs)
                if not folder:
                    os.makedirs(file_path_abs) # 如果不存在，会递归创建
                # print('创建的文件夹：',dir_path)

                server_file = os.path.join(file_path_abs, filename)  #绝对路径+文件名
                # if os.path.exists(server_file): # 服务端已经有这个文件
                #     p = subprocess.Popen("stat -c %y %s|awk -F '.' '{print $1}'" % server_file, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                #     server_file_mtime = p.stdout.readlines()
                #     print('server_file_mtime:', server_file_mtime)
                #     print('client_file_mtime:', str_fdate)
                #     if str_fdate == server_file_mtime:
                #         continue # 文件没变，继续

                # print('更新文件：', server_file)
                f = open(server_file, 'wb') #如果文件存在，会清空，不存在便创建
                for chunk in fobj.chunks():
                    # print('打印chenk', chunk)
                    f.write(chunk)
                    # print('222',chunk.decode('gbk'))

                f.close()
                # touch_time = touch_date(str_fdate)
                # subprocess.Popen("touch -m -t %s %s|awk -F '.' '{print $1}'" % (touch_time,server_file), shell=True,
                #                  stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        else:#type=inc，只上传部分文件
            # path = testabc>WEB-INF>classes
            file_path = path.split('>')[1:] #返回列表，不要开头的项目名称,如果是项目根目录，返回空列表
            user_folder = os.listdir(upload_dir)[0]  # 用户目录，正常情况只有一个
            project_home = os.path.join(upload_dir, user_folder)
            if file_path:
                file_abs_path = os.path.join(project_home, os.sep.join(file_path))  #文件的绝对目录，但不包括文件名
            else:
                file_abs_path = project_home #是在项目根目录下上传文件

            for fobj in file_list:
                server_file = os.path.join(file_abs_path, fobj.name)
                f = open(server_file, 'wb')
                for chunk in fobj.chunks():
                    # print('打印chenk', chunk)
                    f.write(chunk)
                    # print('222',chunk.decode('gbk'))

                f.close()
        project.project_status = 0
        project.save()
        return HttpResponse("文件上传完成！")  # 使用ajax发送后，此处重定向无效

    query_sets = models.Project.objects.filter(id=project_id)
    project = models.Project.objects.get(id=project_id)

    # os.listdir(os.path.join(settings.HISTORY_DIR, project.project_name)) 目录不存在，会报异常
    try:
        files = sorted(os.listdir(os.path.join(settings.HISTORY_DIR, project.project_name)), reverse=True)#倒序
    except Exception as e:# 捕获os.listdir目录存在异常
        print('目录不存在' , e)
        return HttpResponse('项目目录不存在')

    paginator = Paginator(files, 10) #每页5条, paginator.per_page=5
    page = request.GET.get('page')



    try:
        history_query_sets = paginator.page(page)
    except PageNotAnInteger:  # 如果page为None，就会触发这个异常
        # If page is not an integer, deliver first page.
        history_query_sets = paginator.page(1)
    except EmptyPage:  # 大于paginator.num_pages或者小于1
        # If page is out of range (e.g. 9999), deliver last page of results.
        history_query_sets = paginator.page(paginator.num_pages)  # 最后一页

    # print('有多少条历史记录', history_query_sets.number, )

    user = models.User.objects.get(username=username)
    return render( request, 'jenkins/project_info.html' , {'username': username, 'project_id':project_id,
                                                           'project_name':project.project_name,
                                                          'query_sets':query_sets,
                                                           'files':files,
                                                           'history_query_sets':history_query_sets,
                                                           'user': user,
                                                           'noupload_project': noupload_project,

                                                           })

@login_auth
@check_perm.check_perm
def project_build(request, project_id):
    username = request.session.get('_username')
    if request.method == 'POST':# 执行项目构建

        err_msg = ''
        project = models.Project.objects.get(id=project_id)
        if project.project_status != 0:
            err_msg = project.get_project_status_display()
            return render(request, 'jenkins/project_build_err.html', {'username': username,
                                                                      'err_msg': err_msg,})


        project.project_status = 1  # 项目正在构建
        project.save()
        # script_name = project.project_script
        # script_file = os.path.join(settings.SCRIPT_DIR, project.project_name, script_name)
        script_file = project.project_script

        '''
        >>> t = time.time()
        >>> t
        1535598301.9339
        >>>
        >>> time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
        '2018-08-30 11:05:01'
        >>>
        '''

        t = time.time() #当前时间戳

        history_file = os.path.join(settings.HISTORY_DIR, project.project_name,  str(t) )
        loc, char = locale.getdefaultlocale()
        if char == 'cp936':  # OS是gbk编码
            f = open(history_file, 'w+', encoding='gbk' )
        else:
            f = open(history_file, 'w+', encoding='utf-8')

        p = subprocess.Popen(script_file, shell=True, stdout=f, stderr=f)

        p.wait()

        # f.seek(0)
        # out = f.readlines()

        f.close()

        project.project_status = 0
        project.save()

        # 记录构建用户
        history = models.History(projectname=project.project_name, historyfile=str(t), username=username, bdate=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t)))
        history.save()
        return redirect('/jenkins/history/?projectname=%s&filename=%s'  % (project.project_name, str(t))   )

    return redirect('/jenkins/%s/' % project_id)

@login_auth
@check_perm.check_perm
def project_modify(request, project_id):
    username = request.session.get('_username')

    project = models.Project.objects.get(id=project_id)

    if request.method == 'POST':
        project.project_note = request.POST.get('project_note')
        project.project_script = request.POST.get('project_script')
        project.save()
        return redirect('/jenkins/')

    return render(request, 'jenkins/project_modify.html',{
        'username': username,
        'project': project,
    })

@login_auth
@check_perm.check_perm
def project_delete(request, project_id):
    username = request.session.get('_username')
    try:
        project = models.Project.objects.get(id=project_id)
    except models.Project.DoesNotExist:
        return redirect('/jenkins/')

    project_name = project.project_name
    if request.method == 'POST':
        project.delete()
        # project.save()  # 一保存又回来了
        folders = ['history', 'upload']
        for folder in folders:
            print(os.path.join(settings.BASE_DIR, folder, project_name))
            rmdir_all( os.path.join(settings.BASE_DIR, folder, project_name) )  # 不会删除项目目录本身
            os.rmdir(os.path.join(settings.BASE_DIR, folder, project_name))     # 删除项目目录本身

        return redirect('/jenkins/')
    return render(request, 'jenkins/project_delete.html', {'username': username,
                   'project_id':project_id,
                  'project_name':project_name})

@login_auth
def history(request):
    username = request.session.get('_username')
    projectname = request.GET.get('projectname')
    filename = request.GET.get('filename')

    f = open(os.path.join(settings.HISTORY_DIR, projectname, filename), 'r')
    lines = f.readlines()
    f.close()
    return render(request, 'jenkins/history_select.html', {'username':username,
                                                            'projectname':projectname,
                                                            'lines': lines})


# @login_auth
# @check_perm.check_perm

@login_auth
@check_perm.check_perm
def history_del(request ,projectname, filename):

    username = request.session.get('_username')
    project = models.Project.objects.get(project_name=projectname)
    ctime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(filename)))
    # return HttpResponse('del history...%s %s' % (projectname, filename))

    try:
        project_dir = os.path.join(settings.HISTORY_DIR, projectname)
    except Exception as e:
        return HttpResponse('异常')
    if request.method == 'POST':
        file = os.path.join(project_dir, filename)
        if os.path.exists(file):
            os.remove(file)
        return redirect('/jenkins/project/%d/' % project.id)



    return render(request, 'jenkins/history_del.html', {'username': username,
                                                           'project_id':project.id,
                                                           'ctime': ctime,
                   'projectname':projectname,
                  'filename':filename,

                                                        })

# @login_auth
# @check_perm.check_perm
# def admin(request):
#     # table_list = []
#     # for app in enable_tables:
#     #     for tablename, tablemodel in enable_tables[app].items():
#     #     # table_list.append(table._meta.verbose_name) #中文名
#     #         table_list.append(tablemodel._meta.model_name)
#
#     # print(table_list)
#     return render(request, 'jenkins/table_index.html',{
#         'enable_tables':enable_tables,
#
#     })
#
#
# @login_auth
# @check_perm.check_perm
# def table_detail(request, dbname, tablename):
#     table = enable_tables[dbname][tablename]
#     object_list = table.objects.all()
#     paginator = Paginator(object_list, 20)
#     page = request.GET.get('page')
#     try:
#         query_sets = paginator.page(page)
#     except PageNotAnInteger:  # 如果page为None，就会触发这个异常
#         # If page is not an integer, deliver first page.
#         query_sets = paginator.page(1)
#     except EmptyPage:  # 大于paginator.num_pages或者小于1
#         # If page is out of range (e.g. 9999), deliver last page of results.
#         query_sets = paginator.page(paginator.num_pages)  # 最后一页
#     return render(request, 'jenkins/table_detail.html',{
#         'dbname': dbname,
#         'tablename': tablename,
#         'query_sets':query_sets,
#         'table':table,
#
#     })
#
# @login_auth
# @check_perm.check_perm
# def table_change(request, dbname, tablename, rid):
#     table = enable_tables[dbname][tablename]
#     model_form_class = create_model_form(request,table)
#
#     obj = table.objects.get(id=rid)
#     if request.method == "POST":
#         print("change form",request.POST)
#         form_obj = model_form_class(request.POST,instance=obj) #更新
#         if form_obj.is_valid():
#             form_obj.save()
#             return redirect('/jenkins/admin/{_dbname}/{_tablename}/'.format(_dbname=dbname, _tablename=tablename))
#     else:
#
#         form_obj = model_form_class(instance=obj)
#
#     return render(request,"jenkins/table_change.html",{"form_obj":form_obj,
#                                                               "table":table,
#                                                               "app_name":dbname,
#                                                               "table_name":tablename})
#
#
# @login_auth
# @check_perm.check_perm
# def table_add(request, dbname, tablename):
#     table = enable_tables[dbname][tablename]
#     table.is_add_form = True
#     model_form_class = create_model_form(request,table)
#
#     if request.method == "POST":
#         form_obj = model_form_class(request.POST)  #
#         if form_obj.is_valid():
#             form_obj.save()
#             return  redirect(request.path.replace("/add/","/"))
#     else:
#         form_obj = model_form_class()
#
#     return render(request, "jenkins/table_add.html", {"form_obj": form_obj,
#                                                              "table": table})
