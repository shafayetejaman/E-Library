from django.db import models
from more_itertools import quantify

# Create your models here.
    
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name

class Book(models.Model):
    # title, description,image, borrowing price, user reviews
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to="uploads/")
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(max_length=100, unique=True)
    quantity = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    name = models.CharField(max_length=50)
    text = models.TextField()
    email = models.EmailField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="comments")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
