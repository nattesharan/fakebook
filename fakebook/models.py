from werkzeug.security import generate_password_hash,check_password_hash
from mongoengine import Document,StringField,DoesNotExist
from flask_login import UserMixin
class FakeBookUser(Document,UserMixin):
    email = StringField(max_length=128,required=True)
    password = StringField(max_length=128,required=True)
    first_name = StringField(max_length=20,required=True)
    last_name = StringField(max_length=20,required=True)

    def set_password(self,password):
        self.password = generate_password_hash(password,method='sha256')
    
    def verify_password(self,password):
        return check_password_hash(self.password,password)
    @classmethod
    def find_user(cls,email):
        try:
            return bool(cls.objects.get(email=email))
        except DoesNotExist:
            return False