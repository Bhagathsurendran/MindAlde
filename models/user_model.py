# This file manages schema descriptions conceptually.
# Since PyMongo is schema-less, these classes aren't strictly enforced
# but they provide structure definition.

class User:
    def __init__(self, name, email, password, role="Patient", **kwargs):
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.__dict__.update(kwargs)

class Therapist(User):
    def __init__(self, name, email, password, specialization, qualification, experience, contact, **kwargs):
        super().__init__(name, email, password, "Therapist", **kwargs)
        self.specialization = specialization
        self.qualification = qualification
        self.experience = experience
        self.contact = contact
        self.verified = False
