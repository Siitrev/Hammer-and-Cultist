from django import forms
from .models import TagsToPost, Post, Tag
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit

class TagsToPostForm(forms.ModelForm):
    model = TagsToPost
    
    def clean(self):
        cleaned_data = self.cleaned_data
        number_of_tags = TagsToPost.objects.filter(post_id=cleaned_data.get("post").pk).count()
        
        if number_of_tags == 3:
            raise forms.ValidationError("Post can have only 3 tags.")
        
        is_set = TagsToPost.objects.filter(post_id=cleaned_data.get("post").pk, tag_id=cleaned_data.get("tag").pk).count()
        if is_set:
            raise forms.ValidationError("Post already have this tag set.")
        
        super(TagsToPostForm, self).clean()
        return cleaned_data
    
class CreatePostForm(forms.Form):
    title = forms.CharField(max_length=200, label="Title")
    content = forms.CharField(widget=forms.Textarea(attrs={"rows" : "15"}))
    image = forms.ImageField(label="Thumbnail", allow_empty_file=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('title'),
            Field('content', css_class="resize-0"),
            Field('image'),
            Submit('create-btn', 'Create', css_class='btn btn-primary mb-2 d-inline'),
            Submit('draft-btn', 'Draft', css_class='btn btn-primary mb-2 d-inline')
        )
        
    def clean_content(self):
        content : str = self.cleaned_data["content"]
        content = content.strip()
        return content