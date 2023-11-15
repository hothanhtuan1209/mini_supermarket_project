from django import forms


class CreateRoleForm(forms.Form):
    role_name = forms.CharField(max_length=50)
