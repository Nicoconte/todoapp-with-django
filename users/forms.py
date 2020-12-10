from django import forms

class UserRegisterForm(forms.Form):
    name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 
                                                                   'placeholder':'Nombre de usuario'}))
    
    email = forms.EmailField(label="", widget=forms.EmailInput(attrs={"class" : "form-control mt-3",
                                                                      "placeholder" : "Email"}))
    
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={'class':'form-control mt-3', 
                                                                           'placeholder':'Contraseña'}))

class UserLoginForm(forms.Form):
    name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 
                                                                   'placeholder':'Nombre de usuario'}))

    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={'class':'form-control mt-3', 
                                                                           'placeholder':'Contraseña'}))