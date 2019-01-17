
from jenkins import models

# enable_tables = [models.User, models.Role, models.Project] #单个列表无法满足多个app

#enable_tables = {'jenkins':[models.User, models.Role, models.Project]}

enable_tables = {'jenkins':{'user':models.User,
                            'project':models.Project,
                            'permiss': models.Permiss,
                            },}