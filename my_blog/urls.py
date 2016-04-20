from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

blog_urls = [
    url(r'^', include('zinnia.urls.capabilities')),
    url(r'^search/', include('zinnia.urls.search')),
    url(r'^sitemap/', include('zinnia.urls.sitemap')),
    url(r'^trackback/', include('zinnia.urls.trackback')),
    url(r'^tags/', include('zinnia.urls.tags')),
    url(r'^feeds/', include('zinnia.urls.feeds')),
    url(r'^random/', include('zinnia.urls.random')),
    url(r'^authors/', include('zinnia.urls.authors')),
    url(r'^categories/', include('zinnia.urls.categories')),
    url(r'^comments/', include('zinnia.urls.comments')),
    url(r'^', include('zinnia.urls.entries')),
    url(r'^', include('zinnia.urls.archives')),
    url(r'^', include('zinnia.urls.shortlink')),
    url(r'^', include('zinnia.urls.quick_entry'))
]

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'my_blog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^', include(blog_urls, namespace='zinnia')),
    (r'^ckeditor/', include('ckeditor.urls')),
    #url(r'^', include('zinnia.urls', namespace='zinnia')),
)
