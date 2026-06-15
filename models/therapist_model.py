from models.user_model import User

class Therapist(User):
    def __init__(self, name, email, password, specialization, qualification, experience, contact, **kwargs):
        super().__init__(name, email, password, "Therapist", **kwargs)
        self.specialization = specialization
        self.qualification = qualification
        self.experience = experience
        self.contact = contact
        self.verified = False
