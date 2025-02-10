from common.serializers import ModelSerializer
from subjects import models

from professors.models import Professor
from students.serializers import StudentSerializer
from professors.serializers import ProfessorSerializer

from rest_framework import serializers


class StudentFinishSubjectSerializer(serializers.Serializer):

    id = serializers.UUIDField()
    note = serializers.FloatField()


class SubjectRegistrationStatusSerializer(ModelSerializer):
    class Meta:
        model = models.SubjectStatus
        exclude = ["uuid"]


class SubjectSerializer(ModelSerializer):
    class Meta:
        model = models.Subject
        exclude = ["uuid"]


class SubjectRegistrationSerializer(ModelSerializer):

    subject = serializers.SlugRelatedField(
        slug_field="uuid", queryset=models.Subject.objects.all(), required=False
    )
    professor = serializers.SlugRelatedField(
        slug_field="uuid", queryset=Professor.objects.all(), required=False
    )

    class Meta:
        model = models.SubjectRegistration
        exclude = ["uuid", "note", "student", "status"]


class SubjectRegistrationDetailSerializer(ModelSerializer):

    student = StudentSerializer(read_only=True)
    professor = ProfessorSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)
    status = SubjectRegistrationStatusSerializer(read_only=True)

    class Meta:
        model = models.SubjectRegistration
        exclude = ["uuid"]


class FinishSubjectSerializer(serializers.Serializer):

    subject = serializers.UUIDField()

    students = StudentFinishSubjectSerializer(many=True)
