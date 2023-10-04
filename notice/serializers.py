from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import (
	 AdminNotice,
	 SuperAdminNotice,
)
from accounts.serializers import AdminSerializer, SuperAdminSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
	@classmethod
	def get_token(cls, user):
		token = super().get_token(user)

		# Add custom claims
		token['first_name'] = user.first_name
		token['last_name'] = user.last_name
		token['email'] = user.email
		token['profile_type'] = user.profile_type
		token['gender'] = user.gender
		if user.date_of_birth:
			token['date_of_birth'] = str(user.date_of_birth)
		if user.personal_photo:
			token['personal_photo'] = user.personal_photo.url
		token['phone'] = user.phone

		return token


class AdminNoticeSerializer(ModelSerializer):

	author_info = AdminSerializer(source='author', required=False)

	class Meta:
		fields = (
			'id',
			'title',
			'description',
			'attachment',
			'registry_date',
			'author',
			'author_info',
			'audience',
		)
		model = AdminNotice

		extra_kwargs = {
			'author_info': {'read_only': True},
			'author': {'required': True, 'write_only': True},
		}


class SuperAdminNoticeSerializer(ModelSerializer):

	author_info = SuperAdminSerializer(source='author', required=False)

	class Meta:
		fields = (
			'id',
			'title',
			'description',
			'attachment',
			'registry_date',
			'author',
			'author_info',
			'audience',
		)
		model = SuperAdminNotice

		extra_kwargs = {
			'author_info': {'read_only': True},
			'author': {'required': True, 'write_only': True},
		}
