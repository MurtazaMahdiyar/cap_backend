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


class ClassSerializer(ModelSerializer):

    department_info = DepartmentSerializer(source='department', required=False)
    year = IntegerField(required=True)

    class Meta:
        fields = (
            'id',
            'year',
            'name',
            'department',
            'department_info',
        )
        model = Class

        extra_kwargs = {
            'department': {'required': True, 'write_only': True},
            'department_info': {'read_only': True},
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


class StudentSerializer(ModelSerializer):

    student_profile = ProfileSerializer(source='profile', required=False)
    student_class_info = ClassSerializer(source='student_class', required=False)

    class Meta:
        fields = (
            'profile',
            'student_profile',
            'university_id',
            'father_name',
            'student_class',
            'student_class_info',
            'university_id_photo',
            'graduated',
            'status',
        )
        model = Student
        extra_kwargs = {
            'student_profile': {'read_only': True},
            'student_class_info': {'read_only': True},
            'profile': {'required': True, 'write_only': True},
            'student_class': {'required': True, 'write_only': True},
            'university_id_photo': {'required': True},
        }
        


class JobSerializer(ModelSerializer):
    
    student_info = StudentSerializer(source='student', required=False)

    class Meta:
        fields = (
            'id',
            'student',
            'student_info',
            'title',
            'position',
            'company',
            'description',
            'start_date',
            'end_date',
        )
        model = Job

        extra_kwargs = {
            'student': {'required': True, 'write_only': True},
            'start_date': {'required': True},
            'student_info': {'required': False, 'read_only': True},
        }

        validators = [
            UniqueTogetherValidator(
                queryset=Job.objects.all(),
                fields=['student', 'title', 'start_date'],
                message='Job for this student in this date already exists.',
            ),
        ]


class ScholarshipSerializer(ModelSerializer):

    student_info = StudentSerializer(source='student', required=False)

    class Meta:
        fields = (
            'id',
            'student',
            'student_info',
            'country',
            'university',
            'study_field',
            'description',
            'start_date',
            'end_date',
        )
        model = Scholarship

        extra_kwargs = {
            'student': {'required': True, 'write_only': True},
            'student_info': {'required': False, 'read_only': True},
        }

        validators = [
            UniqueTogetherValidator(
                queryset=Scholarship.objects.all(),
                fields=['student', 'start_date'],
                message='Scholarship for this student in this date already exists.',
            ),
        ]




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


class SubjectSerializer(ModelSerializer):

    subject_class_info = ClassSerializer(source='subject_class', required=False)
    teacher_info = TeacherSerializer(source='teacher', required=False)

    class Meta:
        fields = (
            'id',
            'subject_code',
            'subject_name',
            'number_of_credits',
            'teacher',
            'teacher_info',
            'subject_class',
            'subject_class_info',
            'semester',
        )
        model = Subject

        extra_kwargs = {
            'teacher_info': {'read_only': True},
            'subject_class_info': {'read_only': True},
            'teacher': {'required': True, 'write_only': True},
            'subject_class': {'required': True, 'write_only': True},
        }

        validators = [
            UniqueTogetherValidator(
                queryset=Subject.objects.all(),
                fields=['subject_code', 'semester', 'subject_class'],
                message='Subject with given subject_code and semester already exists.',
            ),
        ]


class ResultSheetSerializer(ModelSerializer):

    student_info = StudentSerializer(source='student', required=False)
    subject_info = SubjectSerializer(source='subject', required=False)

    class Meta:
        fields = (
            'id',
            'student',
            'student_info',
            'subject',
            'subject_info',
            'mark',
        )
        model = ResultSheet
        
        extra_kwargs = {
            'subject': {'required': True, 'write_only': True},
            'subject_info': {'read_only': True},
            'student': {'required': True, 'write_only': True},
            'student_info': {'read_only': True},
        }

        validators = [
            UniqueTogetherValidator(
                queryset=ResultSheet.objects.all(),
                fields=['student', 'subject', ],
                message='Student with given subject has been already registered.',
            ),
        ]

    


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
    
