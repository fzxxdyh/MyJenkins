from jenkins import models
from django import template
from django.utils.safestring import mark_safe
import time
import os
from MyJenkins import settings
from jenkins.enable_tables import enable_tables

register = template.Library()

@register.simple_tag
def display_projects(query_sets):
    row_ele = ''
    for row in query_sets:
        row_ele += '<tr><td>{project_id}</td><td><a href="/jenkins/project/{id}/">{project_name}</a></td><td>{project_note}</td></tr>'.format(
            project_id=row.id, id=row.id, project_name=row.project_name, project_note=row.project_note
        )


    return mark_safe(row_ele)

@register.simple_tag
def display_history(history_query_sets, username, projectname, user): #传过来的file是不带路径的
    # print('开始',history_query_sets, username, projectname, '结束')
    if not history_query_sets:
        return ''
    row_ele = ''
    # files = sorted(files, reverse=True) #倒序
    counts = history_query_sets.paginator.count #所有记录总数
    per_page = history_query_sets.paginator.per_page #每页多少条
    number = history_query_sets.number #当前是第几页

    count = counts - (number-1)*per_page

    for file in history_query_sets: # file=1535xxxx.36412


        try:
            history = models.History.objects.get(projectname=projectname, historyfile=file)
            username = history.username
        except models.History.DoesNotExist:
            username = '' #不存在就为空

        # file_path = os.path.join(settings.HISTORY_DIR, projectname, file)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(file)))
        if user.is_admin:
            row_ele += '''<tr>
            <td><a href="/jenkins/history/?projectname={_projectname}&filename={_filename}">{_id}</a></td>
            <td>{_time}</td>
            <td>{_user}</td>
            <td><a href="/jenkins/history/delete/{_projectname}/{_filename}/"><img src="/static/img/del.png" style="width:30px;height:30px;"></a></td>
            </tr>'''.format(_id=count, _time=t, _user=username, _projectname=projectname, _filename=file)
        else:
            row_ele += '''<tr>
                        <td><a href="/jenkins/history/?projectname={_projectname}&filename={_filename}">{_id}</a></td>
                        <td>{_time}</td>
                        <td>{_user}</td>
                        </tr>'''.format(_id=count, _time=t, _user=username, _projectname=projectname, _filename=file)
        count -= 1
    return mark_safe(row_ele)


@register.simple_tag
def  build_paginators(query_sets):
    '''返回整个分页元素'''
    page_btns = ''

    # added_dot_ele = False #
    # for page_num in query_sets.paginator.page_range:
    #     if page_num < 3 or page_num > query_sets.paginator.num_pages -2 \
    #             or abs(query_sets.number - page_num) <= 2: #代表最前2页或最后2页 #abs判断前后1页
    #         ele_class = ""
    #         if query_sets.number == page_num:
    #             added_dot_ele = False
    #             ele_class = "active"
    #         page_btns += '''<li class="%s"><a href="?page=%s">%s</a></li>''' % (
    #         ele_class, page_num,page_num)
    #
    #     else: #显示...
    #         if added_dot_ele == False: #现在还没加...
    #             page_btns += '<li><a>...</a></li>'
    #             added_dot_ele = True

    dot_flag = True
    for num in query_sets.paginator.page_range: # 如果是12页，就是1--12
        if num == query_sets.number: # query_sets.number代表页面中的当前页数值
            dot_flag = True
            current_page = 'active'
        else:
            current_page = ''

        if num < 3 or abs(num-query_sets.number)<=2 or num > query_sets.paginator.num_pages - 2: #前后两页和中间页
            page_btns += '''<li class="%s"><a href="?page=%s">%s</a></li>''' % (current_page,num, num)
        elif dot_flag:
            page_btns += '''<li><a>...</a></li>'''
            dot_flag = False

    return mark_safe(page_btns)


@register.simple_tag
def display_user_list():
    row_ele = ''
    for user in models.User.objects.all():
        row_ele += '''<tr>
        <td>{username}</td>
        <td><a href="">分配角色</a></td>
        <td><a>分配权限</a></td>
        <td><a>修改密码</a></td>
        </tr>'''.format(username=user.username)
    return mark_safe(row_ele)






@register.simple_tag
def display_table(enable_tables):# table主页
    ele_row = ''
    for app in enable_tables:
        for tablename in enable_tables[app]:
            # db_name = model._meta.app_label
            # table_name = model._meta.model_name
            ele_row += '''<tr><td><a href="/jenkins/admin/{_dbname}/{_tablename}/">{_tablename}</a></td>
            <td><a href="/jenkins/admin/{_dbname}/{_tablename}/add/">add</a></td>
            <td>change</td>
            </tr>'''.format(_dbname=app, _tablename=tablename)
    return mark_safe(ele_row)

@register.simple_tag
def display_table_head(table):
    #models_module = importlib.import_module('%s.models'%(app_name))
    #model_obj = getattr(models_module,table_name)
    # table = enable_tables[dbname][tablename]
    row_ele = ''
    '''
    1、当没有ManyToMany字段时，table._meta.fields 与 table._meta.get_fields()显示一样
    2、table._meta.fields无法显示ManyToMany字段， table._meta.get_fields() 可以显示, 所以推荐使用 get_fields()
    3、没有关联字段的表 table._meta.get_fields()显示<OneToOneRel: monitor.t2>, <ManyToOneRel: monitor.t3>, <ManyToManyRel: monitor.t4>, 注意后面是Rel
    4、在有关联字段的表 table._meta.get_fields()显示<django.db.models.fields.related.OneToOneField: f1>, <django.db.models.fields.related.ForeignKey: f2>,<django.db.models.fields.related.ManyToManyField: f3>
       后面是Field或ForeignKey
    5、主表删除一条记录时，从表(OneToOneField、ForeignKey)默认也会级联删除，但从表(ManyToManyField)不会删除记录，只是将关联字段field.all()中remove(主表记录)
    6、field.get_internal_type() 可以获取字段类型 AutoField、 CharField、 OneToOneField 。。。
    '''
    for field in table._meta.fields:  # 遍历每个字段
        # if field.auto_created:#是否是系统自动创建的字段
        row_ele += '''<td>{fieldname}</td>'''.format(fieldname=field.name)
    return mark_safe(row_ele)

@register.simple_tag
def display_table_detail(table, query_sets):
    # table = enable_tables[dbname][tablename]
    row_ele = ''
    dbname = table._meta.app_label
    tablename = table._meta.model_name
    for row in query_sets:#遍历每行
        for field in table._meta.fields:
            # if field.auto_created:#是否是系统自动创建的字段

            field_data = getattr(row, field.name) #用反射，普通是用row.name  row.age ....
            if field.name == 'id':
                row_ele += '''<td><a href="/jenkins/admin/{_dbname}/{_tablename}/{_rid}/change/">{_field}</a></td>'''.format(
                    _dbname=dbname, _tablename=tablename, _rid=field_data, _field=field_data)
            else:
                row_ele += '''<td>{field}</td>'''.format(field=field_data)

        row_ele = '<tr>%s</tr>' % row_ele #每行加tr

    return mark_safe(row_ele)


@register.simple_tag
def oper_project(user, project_id, oper):

    permiss = user.permiss.all() #查询集

    for perm in permiss:#过滤出某个项目
        if perm.project.id == int(project_id) and getattr(perm, oper) == 1:#就是这个项目了
            # print('can del projecdt,有权限')
            return True


    # print('没权限，can del pro')
    return False





