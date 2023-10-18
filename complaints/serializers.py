from rest_framework.serializers import ModelSerializer, ListSerializer, PrimaryKeyRelatedField
from .models import Complaint, ComplaintDocument
from accounts.serializers import ProfileSerializer


class ComplaintDocumentSerializer(ModelSerializer):

	class Meta:
		fields = (
			'id',
			'document',
			'complaint',
		)
		model = ComplaintDocument

		extra_kwargs = {
            'complaint': {'required': True, 'write_only': True},
        }


class ComplaintSerializer(ModelSerializer):

	profile_info = ProfileSerializer(source='profile', required=False)
	documents_list = ComplaintDocumentSerializer(source='document', many=True, required=False)

	class Meta:
		fields = (
			'id',
			'profile_info',
			'title',
			'description',
			'status',
			'comment',
			'complaint_against',
			'documents_list',
			'date_created',
			'private',
		)
		model = Complaint

		extra_kwargs = {
            'profile_info': {'required': False, 'read_only': True},
			'documents_list': {'required': False, 'read_only': True},
        }
