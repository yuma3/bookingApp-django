from django.shortcuts import render
from django.views import generic
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404

from .models import Post, Comment, Reply, Tag
from .forms import PostSearchForm, CommentCreateForm, ReplyCreateForm
# Create your views here.


class PublicPostIndexView(generic.ListView):

    model = Post
    paginate_by = 3
    queryset = Post.objects.filter(is_public=True)

    def get_queryset(self):

        queryset = super().get_queryset()
        self.form = form = PostSearchForm(self.request.GET or None)

        if form.is_valid():
            # 選択したタグが含まれた記事
            tags = form.cleaned_data.get('tags')
            if tags:
                for tag in tags:
                    queryset = queryset.filter(tags=tag)

            key_word = form.cleaned_data.get('key_word')
            if key_word:
                for word in key_word.split():
                    queryset = queryset.filter(
                        Q(title__icontains=word) | Q(text__icontains=word))

        queryset = queryset.order_by('-updated_at').prefetch_related('tags')

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['search_form'] = self.form
        return context

class TagView(generic.ListView):

    model = Post
    paginate_by = 7
    template_name = 'blog/post_list.html'
    queryset = Post.objects.filter(is_public=True)

    def get_queryset(self):
        tag = Tag.objects.get(pk=self.kwargs['pk'])
        queryset = Post.objects.filter(is_public=True,tags=tag)
        return queryset


class PrivatePostIndexView(LoginRequiredMixin, PublicPostIndexView):

    raise_exception = True
    queryset = Post.objects.filter(is_public=False)


class PostDetailView(generic.DetailView):

    model = Post

    def get_queryset(self):

        return super().get_queryset().prefetch_related('tags', 'comment_set__reply_set')

    def get_object(self, queryset=None):

        post = super().get_object()
        if post.is_public or self.request.user.is_authenticated:
            return post
        else:
            raise Http404


class CommentCreateView(generic.CreateView):
    """記事へのコメント作成ビュー"""
    model = Comment
    form_class = CommentCreateForm
    # template_name = 'blog/comment_form.html'

    def form_valid(self, form):

        post_pk = self.kwargs['pk']
        post = get_object_or_404(Post, pk=post_pk)
        comment = form.save(commit=False)
        comment.target = post
        comment.request = self.request
        comment.save()
        return redirect('blog:post_detail', pk=post_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        return context


class ReplyCreate(generic.CreateView):

    model = Reply
    form_class = ReplyCreateForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        comment_pk = self.kwargs['pk']
        comment = get_object_or_404(Comment, pk=comment_pk)
        reply = form.save(commit=False)
        reply.target = comment
        reply.save()
        return redirect('blog/post_detail', pk=comment.target.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment_pk = self.kwargs['pk']
        comment = get_object_or_404(Comment, pk=comment_pk)
        context['post'] = comment.target
        return context
