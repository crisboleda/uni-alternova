from subjects.models import SubjectStatus, SubjectRegistration, Subject


def is_required_subjects_approved(subject_uuid, student):
    """
    Validate if all the required subjects was approved
    """
    subject = Subject.objects.filter(uuid=subject_uuid).first()
    status_approved = SubjectStatus.objects.get(code_name="approved")
    subjects_registration_approved = SubjectRegistration.objects.filter(
        student=student, status=status_approved
    )
    subjects_approved = [
        sub_approved.subject for sub_approved in subjects_registration_approved
    ]
    return all(
        sub_required in subjects_approved
        for sub_required in subject.required_subjects.all()
    )


def is_subject_registered(subject_uuid, student):
    """
    Validate if the subject is registered or in progress
    """
    filter_status = SubjectStatus.objects.filter(
        code_name__in=["approved", "in_progress"]
    )
    return SubjectRegistration.objects.filter(
        subject__uuid=subject_uuid, student=student, status__in=filter_status
    ).exists()
