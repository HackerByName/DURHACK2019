from flask_site import *

class Verifications:
    @staticmethod
    def is_logged_in():
        return "email" in session

    def logout():
        if Verifications.is_logged_in():
            session.pop("email", None)
