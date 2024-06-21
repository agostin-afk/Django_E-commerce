from django.contrib.auth.models import User
from django import forms
from . import models


class PerfilForm(forms.ModelForm):
    class Meta:
        model = models.Perfil
        fields = '__all__'
        exclude = ('usuario',)

class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False, 
        widget=forms.PasswordInput(),
        label='Senha',
        )
    password_confirm = forms.CharField(
        required=False, 
        widget=forms.PasswordInput(),
        label='Confirmar senha',
        )
    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usuario = usuario
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password','password_confirm')
    def clean(self, *args, **kwargs):
        data = self.data
        cleaned = self.cleaned_data
        validation_errors_msgs = {}
        
        usuario_data = cleaned.get('username')
        password_data = cleaned.get('password')
        password2_data = cleaned.get('password_confirm')
        email_data = cleaned.get('email')
        usuario_db = User.objects.filter(username = usuario_data).first()
        email_db = User.objects.filter(email = email_data).first()
        
        error_msg_user_exist = 'Usuario já existe.'
        error_msg_email_exist = 'E-mail já cadastrado.'
        error_msg_password_match = 'As senhas precisam ser iguais.'
        error_msg_password_short = 'Senha muito curta.'
        error_msg_required_field = 'Esse campo é obrigatório.'
        
        
        if self.usuario:
            if usuario_db:
                if usuario_data != usuario_db.username:
                    validation_errors_msgs['username'] = error_msg_user_exist
            if email_db:
                if email_data != email_db.email:
                    validation_errors_msgs['email'] = error_msg_email_exist
            
            if password_data:
                if password_data != password2_data:
                    validation_errors_msgs['password'] = error_msg_password_match
                if len(password_data) < 6:
                    validation_errors_msgs['password'] = error_msg_password_short
        else:
            if usuario_db:
                validation_errors_msgs['username'] = error_msg_user_exist
            if email_db:
                validation_errors_msgs['email'] = error_msg_email_exist
            
            if not password_data:
                validation_errors_msgs['password'] = error_msg_required_field
            
            if not password2_data:
                validation_errors_msgs['password2'] = error_msg_required_field
            
            if password_data != password2_data:
                    validation_errors_msgs['password'] = error_msg_password_match
            # if len(password_data) < 6:
            #     validation_errors_msgs['password'] = error_msg_password_short
        
        if validation_errors_msgs:
            raise (forms.ValidationError(validation_errors_msgs))