from django import forms

from . import models


class CategoryForm(forms.ModelForm):
    # required = True  - by default
    name = forms.CharField(help_text='Please enter the category name.',
                           max_length=models.Category.max_lengths.get('name'))

    # because we handle slugs db saving in the overridden 'save()'
    # method inside the Category class (imported from models.py)
    # we manually set required as False
    slug = forms.CharField(widget=forms.HiddenInput(), required=False,
                           max_length=models.Category.max_lengths.get('slug'))

    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = models.Category
        fields = ('name',)


class PageForm(forms.ModelForm):
    title = forms.CharField(help_text='Please enter the title of the page.',
                            max_length=models.Page.max_lengths.get('title'))

    url = forms.URLField(help_text='Please enter the URL of the page.',
                         max_length=models.Page.max_lengths.get('url'))

    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = models.Page
        exclude = ('category',)

    # example of the pre-cleaning of data. after send to validators
    # def clean(self):
    #     cleaned_data = self.cleaned_data
    #     url = cleaned_data.get('url')
    #
    #     if url and not url.startswith('http://'):
    #         url = 'http://' + url
    #         cleaned_data['url'] = url
    #
    #     return cleaned_data
