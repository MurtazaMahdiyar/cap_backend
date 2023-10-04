from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import ProfileCreationForm, ProfileChangeForm
from .models import Profile, Faculty, Department, Teacher, Admin, SuperAdmin
from alumnus.models import Student


class ProfileAdmin(UserAdmin):
	add_form = ProfileCreationForm
	form = ProfileChangeForm
	model = Profile
	list_display = ("email", "is_staff", "is_active",)
	list_filter = ("email", "is_staff", "is_active",)
	fieldsets = (
		(None, {"fields": ("email", "password", 'first_name', 'last_name', 'profile_type', 'phone', 'gender', 'date_of_birth', 'personal_photo')}),
		("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
	)
	add_fieldsets = (
		(None, {
			"classes": ("wide",),
			"fields": (
				"email", "password1", "password2", 'first_name', 'last_name', 'profile_type', 'phone', 'gender', 'date_of_birth', 'personal_photo', "is_staff",
				"is_active", "groups", "user_permissions"
			)}
		),
	)
	search_fields = ("email",)
	ordering = ("email",)



admin.site.register(Profile, ProfileAdmin)
admin.site.register(Faculty)
admin.site.register(Department)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Admin)
admin.site.register(SuperAdmin)