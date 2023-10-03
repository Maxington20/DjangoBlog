from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 10, 'cols': 80}))
    image_src = forms.CharField(label='Image Source', required=False)

    class Meta:
        model = Post
        fields = ('title', 'content', 'image_src')
