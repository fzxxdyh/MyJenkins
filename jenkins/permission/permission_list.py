#__author:  Administrator


#url type : 0 = related , 1 absolute

perm_dic = {
     'jenkins.can_show_project': {
         'alias': '显示项目',
         'url_type':0,
         'url': 'project_info', #url name
         'method': 'GET',
         'action': 'show_project',
         'args': [],
     },
    'jenkins.can_upload_files': {
        'alias': '上传文件',
        'url_type': 0,
        'url': 'project_info',  # url name
        'method': 'POST',
        'action': 'upload_files',
        'args': [],
    },
    'jenkins.can_del_project':{
        'alias': '删除项目',
        'url_type':0,
        'url': 'delete_project',  # url name
        'method': 'POST',
        'action': 'del_project',
        'args': []
    },
    'jenkins.can_configure_project': {
        'alias': '配置',
        'url_type': 0,
        'url': 'project_modify',  # url name
        'method': 'POST',
        'action': 'conf_project',
        'args': []
    },
    'jenkins.can_build_project': {
        'alias': '立即构建',
        'url_type': 0,
        'url': 'project_build',  # url name
        'method': 'POST',
        'action': 'build_project',
        'args': []
    },
    'jenkins.can_manage_user': {
        'alias': '用户管理',
        'url_type': 1,
        'url': '/king_admin/crm/customer/',  # url name
        'method': 'GET',
        'args': []
    },
}