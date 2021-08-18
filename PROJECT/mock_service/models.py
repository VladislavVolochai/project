from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.encoding import smart_str, smart_bytes
from django.core.validators import ValidationError


def headers_validation(value):
    try: str(value).encode('iso-8859-1') # Python39\lib\wsgiref\headers.py  line 142     return str(self).encode('iso-8859-1')
    except: raise ValidationError(f'Bad headers for iso-8859-1')


class OurRequest(models.Model):
    method = models.CharField(max_length=7, verbose_name='Request method', null=True, blank=True, editable=False)
    url = models.TextField(verbose_name='Request url',null=True, blank=True, editable=False, help_text='decoded with urllib.parse.unquote()')
    body = models.TextField(verbose_name='Request body', null=True, blank=True, editable=False, help_text='decoded with urllib.parse.unquote()')
    encoding=models.CharField(verbose_name='Encoding',max_length=50, null=True, blank=True, editable=False)
    headers = models.JSONField(verbose_name='Request headers', null=True, blank=True, editable=False)
    time = models.DateTimeField(verbose_name='Created', auto_now_add=True, null=True,editable=False)

    def __str__(self):
        return f'{self.method} {self.url}'

    class Meta:
        ordering = ['-time']
        verbose_name = 'Request'
        verbose_name_plural = 'Reauests'


class Group(models.Model):
    active = models.BooleanField(default=False, verbose_name='Group active', null=False, blank=False)
    title = models.CharField(verbose_name='Title', max_length=100, null=False, blank=False)
    slug = models.SlugField(verbose_name='Slug', null=True, blank=False)
    description = models.TextField(null=True, blank=True)
    update_time = models.DateTimeField(verbose_name='Updated', auto_now=True, null=True,editable=False)
    update_user = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name='Updated by', on_delete=models.SET_NULL, null=True,blank=True, editable=False)
    #mocks <- Mock

    def __str__(self):
        return self.title

    def get_admin_url(self):
        return reverse('admin:mock_service_group_change', args=[self.id])

    class Meta:
        ordering = ['-active','title']
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'
    

class Mock(models.Model):
    ALL_ANY = (
            (True,'All'),
            (False,'Any'),
        )
    active = models.BooleanField(default=False, verbose_name='Mock active', null=False, blank=False)
    all_words = models.BooleanField(default=True, verbose_name='All/Any matches', null=False, blank=False, choices=ALL_ANY)
    number = models.PositiveIntegerField(default=0, verbose_name='Mock number', null=False, blank=False, help_text='A higher number will be returned, but not exceeding the number of duplicate requests in short time.')
    request_method = models.CharField(verbose_name='Request methods', default='any', max_length=100, null=False, blank=False, help_text='any, GET, HEAD, POST, PUT, DELETE, CONNECT, OPTIONS, TRACE, PATCH')
    title = models.CharField(verbose_name='Title', max_length=100, null=True, blank=False)
    group = models.ForeignKey(Group,verbose_name='Group', on_delete=models.CASCADE, blank=False, related_name='mocks')
    description = models.TextField(null=True, blank=True)
    #words <- Word 
    response_status_code = models.PositiveIntegerField(verbose_name='Response status code', default=200, null=False, blank=False)
    response_headers = models.JSONField(verbose_name='Response headers', null=True, blank=True, validators=[headers_validation])
    response_content = models.TextField(verbose_name='Response content',null=True, blank=True)
    update_time = models.DateTimeField(verbose_name='Updated', auto_now=True, null=True,editable=False)
    update_user = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name='Updated by', on_delete=models.SET_NULL, null=True, editable=False)
    ordering = models.PositiveIntegerField(default=0,null=False,blank=False, unique=False, editable=True)

    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)

    def group_activity(self):
        try: return self.group.active
        except Group.DoesNotExist: False
    group_activity.short_description = 'Group activity'
    group_activity.boolean = True

    class Meta:
        ordering = ['ordering']
        verbose_name = 'Mock'
        verbose_name_plural = 'Mocks'


class Word(models.Model):
    content = models.CharField(max_length=50, verbose_name='Word', null=True, blank=False)
    mock = models.ForeignKey(Mock, verbose_name='Mock', related_name='words', on_delete=models.CASCADE)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['content']
        verbose_name = 'Word'
        verbose_name_plural = 'Words'
