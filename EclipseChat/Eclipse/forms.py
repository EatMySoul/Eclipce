from django import forms
from string import Template
from django.utils.safestring import mark_safe
from django.forms import ImageField

class PictureWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None, **kwargs):
        html =  Template("""<img src="$link"/>""")
        return mark_safe(html.substitute(link=value))

class UserProfileForm(forms.ModelForm):
    photo = ImageField(widget=PictureWidget)


class JoinChatForm(forms.Form):
    chat_title = forms.CharField(label=False ,max_length=100)
    chat_title.widget = forms.TextInput(attrs={'placeholder' : "chat title"})