from django.db                  import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
class UserProfile(models.Model):
    user = models.ForeignKey(User)
    phone_number = models.CharField(max_length = 15, blank = True, null = True)
    userid = models.AutoField(primary_key = True)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)
    		
    post_save.connect(create_user_profile, sender=User)
    def is_event_core(self):
        try:
            self.user.groups.get(name = "EventCore")
            return True
        except Group.DoesNotExist:
            return False
    def is_event_coord(self):
        try:
            self.user.groups.get(name = "EventCoord")
            return True
        except Group.DoesNotExist:
            return False
    def is_finance_core(self):
       try:
           self.user.groups.get(name = "FinanceCore")
           return True
       except Group.DoesNotExist:
           return False
	
# Create your models here.
