from django import forms
from goods.models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Поделитесь вашим мнением о товаре...',
                'maxlength': '100'
            }),
        }
        labels = {
            'text': 'Текст комментария'
        }

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if len(text) < 10:
            raise forms.ValidationError("Комментарий должен содержать минимум 10 символов")
        if len(text) > 100:
            raise forms.ValidationError("Комментарий не должен превышать 100 символов")
        return text