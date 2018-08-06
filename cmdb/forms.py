#-*- coding: utf-8 -*-
from django import forms
from cmdb.models import IDC, ServerAsset
 
class IDCForm(forms.ModelForm):

    class Meta:
        model = IDC
        exclude = ('uuid','create_time','update_time')
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'isp' : forms.Select(attrs={'class':'form-control'}),
            'address' : forms.TextInput(attrs={'class':'form-control'}),
            'contact' : forms.TextInput(attrs={'class':'form-control'}),
            'phone' : forms.TextInput(attrs={'class':'form-control'}),
            'network' : forms.Textarea(attrs={'class':'form-control'}),
            'comment' : forms.Textarea(attrs={'class':'form-control','rows': '7'})
       }


class ServerAssetForm(forms.ModelForm):


    def __init__(self, *args, **kwargs):
        super(ServerAssetForm, self).__init__(*args, **kwargs)
        field = ['salt','manufacturer','productname','virtual','cpu_model','cpu_nums','memory','disk','os','virtual','kernel','shell','selinux', 'locale','saltversion']
        for i in field:
            self.fields[i].required = False 

    class Meta:
        model = ServerAsset
        exclude = ('uuid', 'hostname', 'create_time', 'update_time')
        widgets = {
        
            'ip' : forms.Textarea(attrs={'class':'form-control'}),
            'idc' : forms.Select(attrs={'class':'form-control'}),
            'salt' : forms.Select(attrs={'class':'form-control'}),
            'status' : forms.Select(attrs={'class':'form-control'}),
            
            'ops' : forms.Select(attrs={'class':'form-control'}),
            'dev' : forms.Select(attrs={'class':'form-control'}),

            'manufacturer' : forms.TextInput(attrs={'class':'form-control'}),
            'productname' : forms.TextInput(attrs={'class':'form-control'}),
            'virtual' : forms.TextInput(attrs={'class':'form-control'}),
            'sn' : forms.TextInput(attrs={'class':'form-control'}),

            'cpu_model' : forms.TextInput(attrs={'class':'form-control'}),
            'cpu_nums' : forms.TextInput(attrs={'class':'form-control'}),
            'memory' : forms.TextInput(attrs={'class':'form-control'}),
            'network' : forms.TextInput(attrs={'class':'form-control'}),
            'disk' : forms.TextInput(attrs={'class':'form-control'}),

            'os' : forms.TextInput(attrs={'class':'form-control'}),
            'virtual' : forms.TextInput(attrs={'class':'form-control'}),
            'kernel' : forms.TextInput(attrs={'class':'form-control'}),
            'shell' : forms.TextInput(attrs={'class':'form-control'}),
            'selinux' : forms.TextInput(attrs={'class':'form-control'}),
            'locale' : forms.TextInput(attrs={'class':'form-control'}),

            'saltversion' : forms.TextInput(attrs={'class':'form-control'}),

       }
