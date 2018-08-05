from werkzeug.security import generate_password_hash,check_password_hash
from mongoengine import Document,StringField,DoesNotExist
from flask_login import UserMixin
class FakeBookUser(Document,UserMixin):
    email = StringField(max_length=128,required=True)
    password = StringField(max_length=128,required=True)
    first_name = StringField(max_length=20,required=True)
    image = StringField(max_length=128,default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS942xv3bE55-_AwDA31FCNGhfWNDaAmmUXy3a3uxRwrV-lcZu6')
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
    
    @property
    def name(self):
        return self.first_name + ' ' + self.last_name