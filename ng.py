import random

alpha_beta = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890'


class NameGenerator:
    def __init__(self):
        self.name = None
        self.mail = None

    def get_user_name(self, new=False):
        if new or self.name is None:
            name = alpha_beta[random.randint(0, len(alpha_beta) - 11)]
            for i in range(15):
                name += alpha_beta[random.randint(0, len(alpha_beta) - 1)]
            self.name = name
            return self.name
        else:
            return self.name

    def get_email(self, new=False):
        if new or self.mail is None:
            mail = alpha_beta[random.randint(0, len(alpha_beta) - 11)]
            for i in range(10):
                mail += alpha_beta[random.randint(0, len(alpha_beta) - 1)]
            mail += '@'
            for i in range(5):
                mail += alpha_beta[random.randint(0, len(alpha_beta) - 1)]
            mail += '.com'
            self.mail = mail
            return self.mail
        else:
            return self.mail


ng = NameGenerator()
