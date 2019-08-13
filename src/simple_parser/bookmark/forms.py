from django import forms
from url_normalize import url_normalize

from .models import Bookmark


class BookmarkForm(forms.ModelForm):
    url = forms.URLField(
        label='Адрес сайта',
        max_length=500,
        widget=forms.TextInput(attrs={'placeholder': "https://http"})
    )

    class Meta:
        model = Bookmark
        fields = ('url',)

    def __init__(self, *args, **kwargs):
        self.context = kwargs.pop('context', {})
        super().__init__(*args, **kwargs)

    def clean_url(self):
        url = url_normalize(self.cleaned_data['url'])
        user = self.context.get('user')

        if user.bookmarks.filter(url__iexact=url).exists():
            raise forms.ValidationError('Данный урл уже был добавлен')

        return url
