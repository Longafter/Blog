from django.shortcuts import render
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType

from .models import Blog, BlogType
from read_statistics.utils import read_statistics_once_read


def get_blog_list_common_data(request, blogs_all_list):
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER)  # 每多少篇进行一次分页
    page_num = request.GET.get('page', 1)  # 获取url的码参数，url中如果没有page这个属性，默认打开第1页
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number  # 获取当前页码
    # 获取当前页码前后各一页范围
    page_range = list(range(max(current_page_num - 1, 1), current_page_num)) + \
                list(range(current_page_num, min(current_page_num + 1, paginator.num_pages) + 1))
    # 加上省略号
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    # 获取博客分类的对应博客数量
    blog_types_list = BlogType.objects.annotate(blog_count=Count('blog'))
    """
    blog_types = BlogType.objects.all()
    blog_types_list= []
    for blog_type in blog_types:
        # 将 blog_count 加到 blog_type 中，是临时的
        blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
        # 放在列表中，临时的变为永久的
        blog_types_list.append(blog_type)
    """

    blogs = page_of_blogs.object_list

    # 获取日期归档对应的博客数量
    blog_dates = Blog.objects.dates('created_time', 'month', order="DESC")
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                                        created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    context = {
        'blogs':blogs,
        'page_of_blogs':page_of_blogs, 
        'page_range':page_range,
        'blog_types':blog_types_list,
        'blog_dates':blog_dates_dict,
    }
    return context


# 博客列表
def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context = get_blog_list_common_data(request, blogs_all_list)
    return render(request, 'blog/blog_list.html', context)


# 博客分类
def blogs_with_type(request, blog_type_pk):
    blog_type = BlogType.objects.get(pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)

    context = get_blog_list_common_data(request, blogs_all_list)
    context['blog_type'] = blog_type
    return render(request, 'blog/blogs_with_type.html', context)


# 日期归档
def blog_with_date(request, year, month):
    blogs_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month)
    blogs_with_date = '%s年%s月' % (year, month)

    context = get_blog_list_common_data(request, blogs_all_list)
    context['blogs_with_date'] = blogs_with_date
    return render(request, 'blog/blogs_with_date.html', context)


# 博客详情
def blog_detail(request, blog_pk):
    blog = Blog.objects.get(pk=blog_pk)
    read_cookie = read_statistics_once_read(request, blog)
    previous_blog = Blog.objects.filter(created_time__gt=blog.created_time).last()
    next_blog = Blog.objects.filter(created_time__lt=blog.created_time).first()

    context = { 
        'blog':blog,
        'previous_blog': previous_blog,
        'next_blog': next_blog,
    }
    response = render(request, 'blog/blog_detail.html', context) # 响应
    response.set_cookie(read_cookie, 'true')  # 阅读cookie标记
    return response
