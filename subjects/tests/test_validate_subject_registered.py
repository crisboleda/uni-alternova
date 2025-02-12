from django.test import TestCase
import uuid
from subjects.models import SubjectRegistration, SubjectStatus
from core.factories.students import StudentFactory
from core.factories.users import UserFactory
from core.factories.subjects import SubjectFactory
from core.factories.professors import ProfessorFactory

from subjects.validations import is_subject_registered


class SubjectRegistrationValidationTestCase(TestCase):

    def setUp(self):
        self.user_student = UserFactory.create()
        self.user_professor = UserFactory.create()
        self.student = StudentFactory.create(user=self.user_student)
        self.professor = ProfessorFactory.create(user=self.user_professor)
        self.subject = SubjectFactory.create(name="Física I", uuid=uuid.uuid4())
        self.status_registration_in_progress = SubjectStatus.objects.create(
            name="En progreso", code_name="in_progress"
        )
        self.status_registration_approved = SubjectStatus.objects.create(
            name="Aprobado", code_name="approved"
        )

    def test_subject_in_progress_already_registered(self):
        """
        Validate if the subject is already registered with status In progress
        """
        self.subject_registration = SubjectRegistration.objects.create(
            student=self.student,
            subject=self.subject,
            status=self.status_registration_in_progress,
            professor=self.professor,
        )

        is_subject_already_registered = is_subject_registered(
            subject_uuid=self.subject.uuid,
            student=self.student,
        )
        self.assertTrue(is_subject_already_registered)

    def test_subject_approved_already_registered(self):
        """
        Validate if the subject is already registered with status Approved
        """
        self.subject_registration = SubjectRegistration.objects.create(
            student=self.student,
            subject=self.subject,
            status=self.status_registration_approved,
            professor=self.professor,
        )

        is_subject_already_registered = is_subject_registered(
            subject_uuid=self.subject.uuid,
            student=self.student,
        )
        self.assertTrue(is_subject_already_registered)

    def test_subject_not_registered(self):
        """
        Validate if the subject is not registered yet
        """
        is_subject_already_registered = is_subject_registered(
            subject_uuid=self.subject.uuid,
            student=self.student,
        )
        self.assertFalse(is_subject_already_registered)
