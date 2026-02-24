from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
    max_length=150,
    widget=forms.TextInput(attrs={'placeholder': 'Tu nombre de usuario', 'class':'main__input'}))
        
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'placeholder':'Tu contraseña', 'class':'main__input'})
    )