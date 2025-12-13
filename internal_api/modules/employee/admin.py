from django import forms
from django.contrib import admin
from core.utils.permissions_mixin import BaseAdminPermission, admin_site
# from validate_docbr import CPF

from internal_api.modules.employee.models import Employee, Role

class EmployeeForm(forms.ModelForm):
    """
    Classe que define o formulário para o modelo Employee
    """

    class Meta:
        model = Employee
        fields = [
            'is_active',
            'full_name',
            'cpf',
            'email',
            'birth_date',
            'cellphone',
            'address',
            'is_system_user',
            'role',
            'oab',
            'oab_status',
            'specialty',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].queryset = Role.objects.filter(is_active=True)

    def clean_cpf(self):
        get_cpf = self.cleaned_data.get('cpf')
        cpf = CPF()
        if not cpf.validate(get_cpf):
            raise forms.ValidationError('CPF inválido')
        return get_cpf
    

@admin.register(Employee)
class EmployeeAdmin(BaseAdminPermission):
    
    form = EmployeeForm

    # module_slug = 