from rest_framework.serializers import ModelSerializer, CharField, IntegerField
from rest_framework.validators import UniqueTogetherValidator
from .models import (
    Profile, Teacher, Admin, Class,
    SuperAdmin, Faculty, Department,
)
from alumnus.models import Student, Job, Scholarship, Subject, ResultSheet


class FacultySerializer(ModelSerializer):

    class Meta:
        fields = (
            'id',
            'name',
        )
        model = Faculty

        extra_kwargs = {
            'name': {'required': True, 'allow_blank': False},
        }
    

class DepartmentSerializer(ModelSerializer):

    faculty_info = FacultySerializer(source='faculty', required=False)

    class Meta:
        fields = (
            'id',
            'name',
            'faculty',
            'faculty_info',
        )
        model = Department

        extra_kwargs = {
            'name': {'required': True, 'allow_blank': False},
            'faculty': {'required': True, 'write_only': True},
            'faculty_info': {'required': False, 'read_only': True},
        }

    
class SubjectSerializer(ModelSerializer):

    class Meta:
        fields = (
            'id',
            'subject_code',
            'subject_name',
            'number_of_credits',
            'teacher',
            'subject_class',
            'semester',
        )
        model = Subject

        validators = [
            UniqueTogetherValidator(
                queryset=Subject.objects.all(),
                fields=['subject_code', 'semester', 'subject_class'],
                message='Subject with given subject_code and semester already exists.',
            ),
        ]

class ResultSheetSerializer(ModelSerializer):

    subject_info = SubjectSerializer(source='subject', required=False)

    class Meta:
        fields = (
            'id',
            'student',
            'subject',
            'subject_info',
            'mark',
        )
        model = ResultSheet
        
        extra_kwargs = {
            'subject': {'required': True, 'write_only': True},
            'student': {'required': True, 'write_only': True},
        }

        validators = [
            UniqueTogetherValidator(
                queryset=ResultSheet.objects.all(),
                fields=['student', 'subject', ],
                message='Student with given subject has been already registered.',
            ),
        ]


class ClassSerializer(ModelSerializer):

    department_info = DepartmentSerializer(source='department', required=False)
    subject_list = SubjectSerializer(source='subjects', many=True, required=False)
    year = IntegerField(required=True)

    class Meta:
        fields = (
            'id',
            'year',
            'name',
            'department',
            'department_info',
            'subject_list',
        )
        model = Class

        extra_kwargs = {
            'department': {'required': True, 'write_only': True},
            'department_info': {'read_only': True},
            'subject_list': {'read_only': True},
        }

        validators = [
            UniqueTogetherValidator(
                queryset=Class.objects.all(),
                fields=['name', 'department', 'year'],
                message='Class with given name already exists in this department.',
            ),
        ]


class ProfileSerializer(ModelSerializer):

    password = CharField(min_length=8, write_only=True)
    
    class Meta:
        model = Profile
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'password',
            'phone',
            'gender',
            'is_active',
            'profile_type',
            'date_of_birth',
            'personal_photo',
        )
        extra_kwargs = {
            'email': {'required': True, },
            'gender': {'required': True, },
            'date_of_birth': {'required': True, },
            'profile_type': {'required': False, 'read_only': True},
            'personal_photo': {'required': True},
        }


class JobSerializer(ModelSerializer):
    
    class Meta:
        fields = (
            'id',
            'title',
            'company',
            'description',
            'start_date',
            'end_date',
        )
        model = Job

        extra_kwargs = {
            'start_date': {'required': True},
        }


class ScholarshipSerializer(ModelSerializer):

    class Meta:
        fields = (
            'id',
            'degree',
            'country',
            'university',
            'study_field',
            'description',
            'start_date',
            'end_date',
        )
        model = Scholarship


class StudentSerializer(ModelSerializer):

    student_profile = ProfileSerializer(source='profile', required=False)
    job_list = JobSerializer(source='jobs', required=False, many=True)
    scholarship_list = ScholarshipSerializer(source='scholarships', required=False, many=True)
    resultsheets = ResultSheetSerializer(source='students', required=False, many=True)

    class Meta:
        fields = (
            'profile',
            'student_profile',
            'student_class',
            'university_id',
            'father_name',
            'university_id_photo',
            'graduated',
            'status',
            'job_list',
            'resultsheets',
            'scholarship_list',
        )
        model = Student
        extra_kwargs = {
            'student_profile': {'read_only': True},
            'job_list': {'read_only': True},
            'scholarship_list': {'read_only': True},
            'profile': {'required': True, 'write_only': True},
            'student_class': {'required': True, 'write_only': True},
            'resultsheets': {'read_only': True},
            'university_id_photo': {'required': True},
        }


class TeacherSerializer(ModelSerializer):
    teacher_profile = ProfileSerializer(source='profile', required=False)
    department_info = DepartmentSerializer(source='department', required=False)

    class Meta:
        fields = (
            'profile',
            'teacher_profile',
            'department',
            'department_info',
        )
        model = Teacher

        extra_kwargs = {
            'teacher_profile': {'read_only': True},
            'department_info': {'read_only': True},
            'profile': {'required': True, 'write_only': True},
            'department': {'required': True, 'write_only': True},
        }



class AdminSerializer(ModelSerializer):

    admin_profile = ProfileSerializer(source='profile', required=False)
    faculty_info = FacultySerializer(source='faculty', required=False)

    class Meta:
        fields = (
            'profile',
            'admin_profile',
            'faculty',
            'faculty_info',
        )
        model = Admin

        extra_kwargs = {
            'faculty_info': {'read_only': True},
            'admin_profile': {'read_only': True},
            'profile': {'required': True, 'write_only': True},
            'faculty': {'required': True, 'write_only': True},
        }

        validators = [
            UniqueTogetherValidator(
                queryset=Admin.objects.all(),
                fields=['profile', 'faculty'],
                message='A profile with this faculty is already exists.',
            ),
        ]


class SuperAdminSerializer(ModelSerializer):

    superadmin_profile = ProfileSerializer(source='profile', required=False)

    class Meta:
        fields = (
            'profile',
            'superadmin_profile',
        )
        
        model = SuperAdmin

        extra_kwargs = {
            'profile': {'required': True, 'write_only': True},
            'superadmin_profile': {'read_only': True},
        }
    
