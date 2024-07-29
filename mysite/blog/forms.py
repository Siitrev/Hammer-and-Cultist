from django import forms
from .models import TagsToPost, Post, Tag
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, Button

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
    image = forms.ImageField(label="Thumbnail", allow_empty_file=False, required=False)
    tags = forms.ModelChoiceField(queryset=Tag.objects.order_by("name"), label="Tags", required=False, empty_label="Choose a tag:")
    chosen_tag_0 = forms.CharField(max_length=40, required=False, widget=forms.HiddenInput())
    chosen_tag_1 = forms.CharField(max_length=40, required=False, widget=forms.HiddenInput())
    chosen_tag_2 = forms.CharField(max_length=40, required=False, widget=forms.HiddenInput())
    draft = forms.BooleanField(required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('title'),
            Field('content', css_class="resize-0"),
            Field('tags'),
            Div(
                Div(
                "chosen_tag_0", 
                "chosen_tag_1",
                "chosen_tag_2",
                css_id="hidden_inputs"
                ), css_id="chosen_tags", css_class="mb-3"),
            Field('image'),
            Field('draft'),
            Submit('submit', 'Create', css_class='btn btn-primary mb-2 d-inline'),
            Button('cancel', 'Cancel', css_id="cancel-btn", css_class='btn btn-danger mb-2 d-inline'),
            
        )
 
        
class UpdatePostForm(forms.Form):
    title = forms.CharField(max_length=200, label="Title")
    content = forms.CharField(widget=forms.Textarea(attrs={"rows" : "15"}))
    image = forms.ImageField(label="Thumbnail", allow_empty_file=False, required=False)
    tags = forms.ModelChoiceField(queryset=Tag.objects.order_by("name"), label="Tags", required=False, empty_label="Choose a tag:")
    chosen_tag_0 = forms.CharField(max_length=40, required=False, widget=forms.HiddenInput())
    chosen_tag_1 = forms.CharField(max_length=40, required=False, widget=forms.HiddenInput())
    chosen_tag_2 = forms.CharField(max_length=40, required=False, widget=forms.HiddenInput())
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('title'),
            Field('content', css_class="resize-0"),
            Field('tags'),
            Div(
                Div(
                "chosen_tag_0", 
                "chosen_tag_1",
                "chosen_tag_2",
                css_id="hidden_inputs"
                ), css_id="chosen_tags", css_class="mb-3"),
            Field('image'),
            Button('publish', 'Publish', css_id="publish-btn", css_class='btn btn-primary mb-2 me-1 d-inline'),
            Submit('submit', 'Update', css_class='btn btn-primary mb-2 mx-1 d-inline'),
            Button('cancel', 'Cancel', css_id="cancel-btn", css_class='btn btn-danger mb-2 mx-1 d-inline'),
        )
        

class CreateCommentForm(forms.Form):
    content = forms.CharField(max_length=1000,required=False, widget=forms.Textarea(attrs={"placeholder":"Leave a comment...", "rows" : "3"}))
    
    def __init__(self, *args, **kwargs):
        super(CreateCommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.fields['content'].label = False
        self.helper.layout = Layout(
            Field('content', css_class="resize-0"),
            Submit('submit', 'Create', css_class='btn btn-primary mb-2'),
        )