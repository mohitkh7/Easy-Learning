from .models import User, Resource
from django import forms
from django.core.exceptions import ValidationError

from django.contrib.auth.forms import UserCreationForm

METHODS=(
	('book','Book'),
	('ebook','eBook'),
	('video','Video'),
	('website','Website'),
	('blog','Blog'),
	('mooc','MOOC'),
	('other','Other'),
)

SORT = (
    ('vhl','Vote: High to Low'),
    ('vlh','Vote: Low to High'),
    ('phl','Price: High to Low'),
    ('plh','Price: Low to High'),
    ('dno','Date: Latest to Oldest'),
    ('don','Date:Oldest to Latest'),
)

def UniqueEmailValidator(value):
    if User.objects.filter(email__iexact=value).exists():
        raise ValidationError('User with this Email already exists.')

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].validators.append(UniqueEmailValidator)

class SignupForm2(forms.ModelForm):
    username = forms.RegexField(regex=r'^[\w.@+-]+$',max_length=30,label='Username')
    email = forms.EmailField(label="E-mail")
    password1 = forms.CharField(widget=forms.PasswordInput,label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput,label="Re-enter Password")

    class Meta:
        model = User
        fields = ('username','email','password1','password2')

    def clean_email(self):
    	#To Ensure Unique Email
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'This email address already exist.')
        password1=self.cleaned_data.get('password1')
        password2=self.cleaned_data.get('password2')
        if password1!=password2:
            raise forms.ValidationError(u'Password Mismatch.')

        return email

class ResourceFilterForm(forms.ModelForm):
    # level = forms.CharField(required=False)
    # method = forms.MultipleChoiceField(
    #     required=False,
    #     widget=forms.SelectMultiple,
    #     choices=METHODS,
    # )
    sort = forms.ChoiceField(required=False,widget=forms.Select,choices=SORT)
    def __init__(self, *args, **kwargs):
        super(ResourceFilterForm, self).__init__(*args, **kwargs)
        self.fields['level'].required = False
        self.fields['method'].required = False

    class Meta:
        model = Resource
        fields = ('level','method')