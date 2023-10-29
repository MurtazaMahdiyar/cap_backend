from rest_framework.serializers import ModelSerializer, ListSerializer, PrimaryKeyRelatedField
from .models import Complaint
from accounts.serializers import ProfileSerializer



class ComplaintSerializer(ModelSerializer):

	profile_info = ProfileSerializer(source='profile', required=False)

	class Meta:
		fields = (
			'id',
			'profile_info',
			'title',
			'description',
			'status',
			'comment',
			'complaint_against',
			'attachment',
			'date_created',
			'private',
		)
		model = Complaint

		extra_kwargs = {
            'profile_info': {'required': False, 'read_only': True},
        }
