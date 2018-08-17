from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import AuthUser, Profile, Story, Entry, Comment, Evaluation
from django import forms


class LoginForm(AuthenticationForm):
    """ログインフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label  # placeholderにフィールドのラベルを入れる


class RegisterForm(UserCreationForm):
    class Meta:
        model = AuthUser
        fields = (
            "username", "email", "password1", "password2",
            "age",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'ユーザ名'

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'メールアドレス'

        self.fields['age'].widget.attrs['class'] = 'form-control'
        self.fields['age'].widget.attrs['placeholder'] = '年齢'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'パスワード'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'パスワード（確認）'


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            "profile_text",
        )


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = (
            "name",
            "first_text",
            "tag1",
            "tag2",
            "tag3",
        )


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = (
            'text',
        )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (
            'star',
            'text'
        )