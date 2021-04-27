from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.html import strip_tags
from django.utils.text import slugify
from django.views.generic import ListView, DetailView
from pure_pagination.mixins import PaginationMixin
from .models import Post, Category, Tag
from .forms import PostForm
import markdown
from markdown.extensions.toc import TocExtension
import re

class IndexView(PaginationMixin, ListView):
  model = Post
  template_name = 'blog/index.html'
  context_object_name = 'post_list'
  paginate_by = 10


class CategoryView(IndexView):
  def get_queryset(self):
    queried_category = get_object_or_404(Category, pk=self.kwargs.get('pk'))
    return super(CategoryView, self).get_queryset().filter(category=queried_category)


class TagView(IndexView):
  def get_queryset(self):
    queried_tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
    return super(TagView, self).get_queryset().filter(tag=queried_tag)


class PostDetailView(DetailView):
  model = Post
  template_name = 'blog/detail.html'
  context_object_name = 'post'

  def get(self, request, *args, **kwargs):
      response = super(PostDetailView, self).get(request, *args, **kwargs)
      self.object.increase_views()
      return response

  def get_object(self, queryset=None):
    post = super().get_object(queryset=None)
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        TocExtension(slugify=slugify),
    ])
    post.body = md.convert(post.body)

    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''

    return post
