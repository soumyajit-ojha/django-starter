from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError("email must required.")
        if not password:
            raise ValueError("password must required.")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
    
    def create_user(self, email, username, password, **extra_fields):
        extra_fields.setdefault("is_admin", False)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, username, password, **extra_fields)
    
    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, username, password, **extra_fields)
        