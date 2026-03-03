from django.db import models
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
import uuid,socket

User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def generate_verification_token(self):
        self.email_verification_token = str(uuid.uuid4())
        self.save()
        return self.email_verification_token

 

    # inside UserProfile model...
    def send_verification_email(self):
        verification_link = f"{settings.BASE_URL}/accounts/verify/{self.email_verification_token}/"
        subject = "Verify Your TaskSphere Email"
        message = f"Hello {self.user.username},\n\nVerify here: {verification_link}"
        
        original_timeout = socket.getdefaulttimeout()
        socket.setdefaulttimeout(5.0) 
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [self.user.email],
                fail_silently=False,
            )
        finally:
            socket.setdefaulttimeout(original_timeout)