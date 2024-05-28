from .models import Book, Category, Comment
from django import forms


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"

    

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "email","text"]

