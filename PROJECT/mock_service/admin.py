from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Mock, Group, Word, OurRequest
from .forms import MockFormAdmin #, GroupFormAdmin

from adminsortable2.admin import SortableAdminMixin
from django_json_widget.widgets import JSONEditorWidget

class WordInline(admin.TabularInline): #TabularInline
	model = Word
	extra = 1

# class MockInline(admin.StackedInline):
# 	model = Mock
# 	extra = 1

@admin.register(OurRequest)
class OurRequestAdmin(admin.ModelAdmin):
	readonly_fields = [*[i.name for i in OurRequest._meta.get_fields()][1:]]
	


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
	save_on_top = True
	search_fields = ('title__icontains','mocks__title__icontains','slug__icontains')
	list_display = ('title','active')
	actions = ['active_True','active_False']

	#inlines = [MockInline,]

	#form = GroupFormAdmin

	def save_model(self, request, obj, form, change):
		obj.update_user = request.user
		super().save_model(request, obj, form, change)

	@admin.action(description='Active make TRUE', permissions=['change'])
	def active_True(self, request, queryset):
		queryset.update(active=True)
		self.message_user(request,'It was updated',messages.SUCCESS)

	@admin.action(description='Active make FALSE', permissions=['change'])
	def active_False(self, request, queryset):
		queryset.update(active=False)
		self.message_user(request,'It was updated',messages.SUCCESS)


@admin.register(Mock)
class MockAdmin(SortableAdminMixin, admin.ModelAdmin):
	save_on_top = True
	search_fields = ('title__icontains', 'group__title__icontains', 'words__content__icontains', 'group__slug__icontains')
	list_display = ('number','title','group_url','request_method','active','group_activity')
	list_display_links = ('title',)
	list_filter = ('group__active','active')
	actions = ['active_True','active_False']
	readonly_fields = ['update_time','update_user']

	inlines = [WordInline,]

	form=MockFormAdmin

	def save_model(self, request, obj, form, change):
		obj.update_user = request.user
		super().save_model(request, obj, form, change)

	# def o(self, obj):
	# 	return obj.ordering
	# o.short_description = ' '

	def group_url(self, obj):
		return mark_safe(f'<a href="{obj.group.get_admin_url()}">{obj.group}</a>')
	group_url.short_description = Mock._meta.get_field('group').verbose_name

	@admin.action(description='Active make TRUE', permissions=['change'])
	def active_True(self, request, queryset):
		queryset.update(active=True)
		self.message_user(request,'It was updated',messages.SUCCESS)

	@admin.action(description='Active make FALSE', permissions=['change'])
	def active_False(self, request, queryset):
		queryset.update(active=False)
		self.message_user(request,'It was updated',messages.SUCCESS)





# @admin.register(Word)
# class Word(admin.ModelAdmin):
# 	pass