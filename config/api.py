from rest_framework import routers

from subjects.viewsets import (
    SubjectViewSet,
    SubjectRegistrationViewSet,
    ProfessorSubjectRegistrationViewSet,
)


api = routers.DefaultRouter()
api.trailing_slash = "/?"

# Subjects
api.register(r"subjects", SubjectViewSet, basename="subjects")
api.register(
    r"students/subjects",
    SubjectRegistrationViewSet,
    basename="student-subject-registration",
)
api.register(
    r"professors/subjects",
    ProfessorSubjectRegistrationViewSet,
    basename="professor-subject-registration",
)
