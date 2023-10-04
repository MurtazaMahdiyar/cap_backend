from rest_framework.serializers import ModelSerializer
from .models import Complaint, ComplaintDocument
from accounts.serializers import StudentSerializer



class ComplaintSerializer(ModelSerializer):

	student_info = StudentSerializer(source='student', required=False)

	class Meta:
		fields = (
			'id',
			'student',
			'student_info',
			'title',
			'description',
			'status',
			'comment',
			'complaint_against',
			'date_created',
		)
		model = Complaint

		extra_kwargs = {
            'student': {'required': True, 'write_only': True},
            'student_info': {'required': False, 'read_only': True},
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