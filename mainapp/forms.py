from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)

class ChoiceQuestionForm(forms.Form):
    choice = forms.ModelChoiceField(queryset=None, widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        queryset = kwargs.pop('choices')
        super(ChoiceQuestionForm, self).__init__(*args, **kwargs)
        self.fields['choice'].queryset = queryset
