from django import template
from django.db.models.aggregates import Count
from ..models import Post, Category, Tag
import random


register = template.Library()

@register.inclusion_tag('blog/inclusions/_recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):
    return {
        'recent_post_list': Post.objects.all().order_by('-created_time')[:num],
    }

@register.inclusion_tag('blog/inclusions/_random_posts.html', takes_context=True)
def show_random_posts(context, num=2):
    return {
        'random_post_list': Post.objects.all().order_by('?')[:num],
    }

@register.inclusion_tag('blog/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    category_list = Category.objects.annotate(
        num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'category_list': category_list,
    }

@register.inclusion_tag('blog/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    tag_list = Tag.objects.annotate(
        num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'tag_list': tag_list,
    }
