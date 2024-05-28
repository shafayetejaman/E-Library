from django.shortcuts import render, redirect
from .models import Book, Comment, Category
from .forms import BookForm, CommentForm
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from transaction.models import Transaction


# Create your views here.


def home(request, category_slug=None):
    books = Book.objects.all()
    categories = Category.objects.all()
    category = None

    if category_slug:
        category = Category.objects.get(slug=category_slug)
        books = Book.objects.filter(category=category)

    return render(
        request,
        "show_books/show_post_list.html",
        {
            "logged": request.user.is_authenticated,
            "books": books,
            "categories": categories,
            "current_category": category,
        },
    )


class CreatePostView(CreateView):
    model = Book
    form_class = BookForm
    template_name = "show_books/add_post.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().is_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["logged"] = self.request.user.is_authenticated
        return context


class DetailPostView(DetailView):
    model = Book
    pk_url_kwarg = "id"
    template_name = "show_books/detail_post.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        comments = book.comments.all().order_by("-created")
        comment_form = CommentForm()

        borrowed = len(
            Transaction.objects.filter(
                account=self.request.user.account, book=book, transaction_type=2
            )
        )
        borrowed += len(
            Transaction.objects.filter(
                account=self.request.user.account, book=book, transaction_type=3
            )
        )

        context["logged"] = self.request.user.is_authenticated
        context["comments"] = comments
        context["comment_form"] = comment_form
        context["borrowed"] = borrowed

        return context

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(data=self.request.POST)
        book = self.get_object()

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.book = book
            new_comment.save()

        return self.get(request, *args, **kwargs)


class DeletePostView(DeleteView):
    model = Book
    pk_url_kwarg = "id"
    template_name = "show_books/delete_post.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["logged"] = self.request.user.is_authenticated
        return context


class UpdatePostView(UpdateView):
    model = Book
    form_class = BookForm
    pk_url_kwarg = "id"
    template_name = "show_books/Update_post.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["logged"] = self.request.user.is_authenticated
        return context
