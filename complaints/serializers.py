from rest_framework.serializers import ModelSerializer
from .models import Complaint, ComplaintDocument
from accounts.serializers import ProfileSerializer



class ComplaintSerializer(ModelSerializer):

	profile_info = ProfileSerializer(source='profile', required=False)

	class Meta:
		fields = (
			'id',
			'profile',
			'profile_info',
			'title',
			'description',
			'status',
			'comment',
			'complaint_against',
			'date_created',
			'private',
		)
		model = Complaint

		extra_kwargs = {
            'profile': {'required': True, 'write_only': True},
            'profile_info': {'required': False, 'read_only': True},
        }


class ComplaintDocumentSerializer(ModelSerializer):

	complaint_info = ComplaintSerializer(source='complaint', required=False)

	class Meta:
		fields = (
			'id',
			'document',
			'complaint',
			'complaint_info',
		)
		model = ComplaintDocument

		extra_kwargs = {
            'complaint': {'required': True, 'write_only': True},
            'complaint_info': {'required': False, 'read_only': True},
        }