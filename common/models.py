from django.db import models
import uuid
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    #abstract base classes are useful when you wnat to put some common information into a number of other models ypu write yur basr class
    # and put abstract=true in teh meta class this model will then not be used to create any database table instead when it is used as a base class for other models its fied will bw added to those of the base class
    
    class Meta:
        abstract = True