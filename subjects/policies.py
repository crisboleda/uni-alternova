from rest_access_policy.access_policy import AccessPolicy


class StudentAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["*"],
            "principal": ["group:student"],
            "effect": "allow",
        },
    ]
