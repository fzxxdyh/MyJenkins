#__author:  Administrator
#date:  2017/1/10

# from django.utils.translation import ugettext as _
from django.forms import forms,ModelForm
# from django.forms import ValidationError
from jenkins import models



def create_model_form(request,model_class):
    '''动态生成MODEL FORM'''
    def __new__(cls, *args, **kwargs):

        # super(CustomerForm, self).__new__(*args, **kwargs)
        #print("base fields",cls.base_fields)
        # print('cls是什么==》', cls)
        for field_name,field_obj in cls.base_fields.items():
            field_obj.widget.attrs['class'] = 'form-control'

            #print(field_name,dir(field_obj))

            # field_obj.widget.attrs['maxlength'] = getattr(field_obj,'max_length' ) if hasattr(field_obj,'max_length') \
            #     else ""



        return ModelForm.__new__(cls)



    class Meta:
        # model = admin_class.model
        model = model_class
        fields = "__all__"
        # exclude = model_class.modelform_exclude_fields
    attrs = {'Meta':Meta}
    _model_form_class =  type("DynamicModelForm",(ModelForm,),attrs)
    setattr(_model_form_class, '__new__', __new__)
    # setattr(_model_form_class,'clean',default_clean)

    print("model form",_model_form_class.Meta.model )
    return _model_form_class