from django.db import models

# Create your models here.
class Project(models.Model):
    '''项目表'''
    project_name = models.CharField(max_length=32,unique=True)
    # project_note = models.CharField(max_length=512, null=True, blank=True)
    project_note = models.TextField(null=True, blank=True, default=None)
    project_script = models.CharField(max_length=1024, null=True, blank=True)
    project_status_choice = ( (0, ''), (1, '项目正在构建，请稍等'), (2, '项目上传文件出错'))
    project_status = models.SmallIntegerField(choices=project_status_choice, default=0)

    def __str__(self):
        return self.project_name

    class Meta:
        verbose_name ="项目表"
        verbose_name_plural ="项目表"


class User(models.Model):
    '''用户表'''
    username = models.CharField(max_length=32,unique=True)
    password = models.CharField(max_length=32)
    is_admin = models.BooleanField(default=False)
    permiss = models.ManyToManyField("Permiss",blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name ="用户"
        verbose_name_plural ="用户表"



class Permiss(models.Model):
    project = models.ForeignKey("Project", null=False)
    project_choices = ((0, '没权限'),(1, '有权限'))
    del_project = models.SmallIntegerField(choices=project_choices, default=0)
    conf_project = models.SmallIntegerField(choices=project_choices, default=0)
    build_project = models.SmallIntegerField(choices=project_choices, default=0)
    show_project = models.SmallIntegerField(choices=project_choices, default=0)
    upload_files = models.SmallIntegerField(choices=project_choices, default=0)
    def __str__(self):
        show = ''
        if self.del_project:
            show += '删除 '
        if self.conf_project:
            show += '配置 '
        if self.build_project:
            show += '构建 '
        if self.upload_files:
            show += '上传 '
        if self.show_project:
            show += '可读'
        return '%s权限：%s' % (self.project.project_name, show)

    class Meta:
        verbose_name = "权限表"
        verbose_name_plural = "权限表"



class History(models.Model):
    projectname = models.CharField(max_length=50, default='')
    historyfile = models.CharField(max_length=200)
    username = models.CharField(max_length=20, default='')
    bdate = models.CharField(max_length=20)
    def __str__(self):
        return '%s %s' % (self.project.project_name, self.historyfile)

    class Meta:
        verbose_name = "历史表"
        verbose_name_plural = "历史表"

        unique_together = ("projectname", "historyfile")
