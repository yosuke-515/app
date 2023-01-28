from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Article,Comment
from django.views import generic

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from django.db.models import Q

from .forms import CommentCreateForm
from django.shortcuts import redirect, get_object_or_404

class UpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Article
    fields = ['content', 'title', ]
 
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
 
        if obj.author != self.request.user:
            raise PermissionDenied('You do not have permission to edit.')
 
        return super(UpdateView, self).dispatch(request, *args, **kwargs)
 
class DeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    model = Article
    success_url = reverse_lazy('bbs:index')

class IndexView(generic.ListView):
    def get_queryset(self):
        q_word = self.request.GET.get('query')
 
        selected_title = self.request.GET.get('title')
        selected_article = self.request.GET.get('article')
 
        if q_word:
            if selected_title and selected_article:
                object_list = Article.objects.filter(
                    Q(title__icontains=q_word) | Q(content__icontains=q_word))
            elif selected_title:
                object_list = Article.objects.filter(Q(title__icontains=q_word))
            else:
                object_list = Article.objects.filter(Q(content__icontains=q_word))
        else:
            object_list = Article.objects.all()
 
        return object_list
 
class DetailView(generic.DetailView):
    model = Article
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentCreateForm

        return context

class CreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Article
    fields = ['content', 'title', ]
 
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreateView, self).form_valid(form)

class CommentCreate(LoginRequiredMixin,generic.CreateView):
    model = Comment
    form_class = CommentCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        post_pk = self.kwargs.get('pk')
        post = get_object_or_404(Article, pk=post_pk)

        comment = form.save(commit=False)
        comment.target = post
        comment.save()

        return redirect('bbs:detail', pk=post_pk)

def delete_comment(request, pk, comment_pk):
    comment = Comment.objects.get(id=comment_pk)
    post_id = pk
    comment.delete()
    return redirect('bbs:detail', pk=post_id)
