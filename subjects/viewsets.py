from common import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from django.db.models import Avg

from subjects.validations import is_required_subjects_approved, is_subject_registered
from subjects.models import SubjectStatus, SubjectRegistration, Subject
from subjects import serializers
from students.serializers import StudentSerializer


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = serializers.SubjectSerializer


# Student subject registrations
class SubjectRegistrationViewSet(
    viewsets.GenericViewSet, CreateModelMixin, ListModelMixin
):
    queryset = SubjectRegistration.objects.all()
    serializer_class = serializers.SubjectRegistrationDetailSerializer

    def perform_create(self, serializer):
        subject_uuid = self.request.data.get("subject")
        student = self.request.user.student

        if is_subject_registered(subject_uuid=subject_uuid, student=student):
            raise ValidationError("La materia ya fue aprovada o ya está registrada")

        if not is_required_subjects_approved(
            subject_uuid=subject_uuid, student=student
        ):
            raise ValidationError(
                "Te faltan materias por aprobar para poder registrar esta materia"
            )

        first_status = SubjectStatus.objects.get(code_name="in_progress")
        serializer.save(student=student, status=first_status)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action in ["create"]:
            return serializers.SubjectRegistrationSerializer
        return serializers.SubjectRegistrationDetailSerializer

    def get_queryset(self):
        return SubjectRegistration.objects.filter(student=self.request.user.student)

    @action(detail=False, methods=["GET"], url_path="average")
    def get_average_subjects_approved(self, request):
        status_approved = SubjectStatus.objects.get(code_name="approved")
        queryset = self.get_queryset().filter(status=status_approved)
        general_average = queryset.aggregate(total=Avg("note"))

        serializer = self.get_serializer(queryset, many=True)

        return Response(
            data={
                "general_average": general_average.get("total", 0.0),
                "subjects": serializer.data,
            }
        )


class ProfessorSubjectRegistrationViewSet(viewsets.GenericViewSet, ListModelMixin):
    queryset = SubjectRegistration.objects.all()
    serializer_class = serializers.SubjectSerializer

    def get_serializer_class(self):
        if self.action in ["finalize_subject"]:
            return serializers.FinishSubjectSerializer
        return serializers.SubjectSerializer

    def get_queryset(self):
        professor = self.request.user.professor
        return Subject.objects.filter(
            uuid__in=SubjectRegistration.objects.filter(
                professor=professor
            ).values_list("subject__uuid")
        ).distinct()

    @action(detail=False, methods=["GET"], url_path="students")
    def get_students_by_subject(self, request):
        subjects = self.get_queryset()
        subjects_students = []

        for subject in subjects:
            subject_registrations = SubjectRegistration.objects.filter(subject=subject)
            students = []
            for sub_registration in subject_registrations:
                student_data = StudentSerializer(sub_registration.student).data
                student_data["note"] = sub_registration.note
                students.append(student_data)
            subjects_students.append(
                {
                    "subject": serializers.SubjectSerializer(subject).data,
                    "students": students,
                }
            )

        return Response(data=subjects_students)

    @action(detail=False, methods=["POST"], url_path="finalize")
    def finalize_subject(self, request):
        subject_uuid = request.data.get("subject")
        students = request.data.get("students")

        for student in students:
            subject_registration = SubjectRegistration.objects.get(
                subject__uuid=subject_uuid, student__uuid=student.get("id")
            )
            subject_registration.note = student.get("note", 0.0)

            if subject_registration.note >= 3.0:
                subject_registration.status = SubjectStatus.objects.get(
                    code_name="approved"
                )
            else:
                subject_registration.status = SubjectStatus.objects.get(
                    code_name="failed"
                )

            subject_registration.save()

        return self.get_students_by_subject(request)
