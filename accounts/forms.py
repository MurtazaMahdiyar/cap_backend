from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile



class ProfileCreationForm(UserCreationForm):
	class Meta(UserCreationForm):
		model = Profile
		fields = ('first_name', 'last_name', 'phone', 'gender', 'date_of_birth', 'personal_photo')


class ProfileChangeForm(UserChangeForm):
	class Meta:
		model = Profile
		fields = ('first_name', 'last_name', 'phone', 'gender', 'date_of_birth', 'personal_photo')