from django.test import TestCase
import uuid
from subjects.models import SubjectRegistration, SubjectStatus
from core.factories.students import StudentFactory
from core.factories.users import UserFactory
from core.factories.subjects import SubjectFactory
from core.factories.professors import ProfessorFactory

from subjects.validations import is_required_subjects_approved


class SubjectRequiredSubjectsTestCase(TestCase):

    def setUp(self):
        self.user_student = UserFactory.create()
        self.user_professor = UserFactory.create()
        self.student = StudentFactory.create(user=self.user_student)
        self.professor = ProfessorFactory.create(user=self.user_professor)
        self.subject_required = SubjectFactory.create(
            name="Física I", uuid=uuid.uuid4()
        )
        self.subject = SubjectFactory.create(
            name="Matematicas II",
            uuid=uuid.uuid4(),
        )
        self.subject.required_subjects.add(self.subject_required)
        self.subject.save()

        self.status_registration_in_progress = SubjectStatus.objects.create(
            name="En progreso", code_name="in_progress"
        )
        self.status_registration_approved = SubjectStatus.objects.create(
            name="Aprobado", code_name="approved"
        )

    def test_all_subjects_required_not_approved(self):
        """
        Validate if the required subjects have not been completed
        """
        is_all_required_subjects_approved = is_required_subjects_approved(
            subject_uuid=self.subject.uuid,
            student=self.student,
        )
        self.assertFalse(is_all_required_subjects_approved)

    def test_all_subjects_required_approved(self):
        """
        Validate if the required subjects are approved
        """
        self.subject_registration = SubjectRegistration.objects.create(
            student=self.student,
            subject=self.subject_required,
            status=self.status_registration_approved,
            professor=self.professor,
        )

        is_all_required_subjects_approved = is_required_subjects_approved(
            subject_uuid=self.subject.uuid,
            student=self.student,
        )
        self.assertTrue(is_all_required_subjects_approved)
