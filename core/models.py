from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_categories')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Suggestion(models.Model):
    STATUS_CHOICES = [
        ('under_review', 'Under Review'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='suggestions')
    is_anonymous = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='suggestions')
    title = models.CharField(max_length=200)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='under_review')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Add NLP fields
    sentiment = models.FloatField(null=True, blank=True, help_text="Sentiment polarity: -1 (negative) to 1 (positive)")
    is_spam = models.BooleanField(default=False, help_text="Flag if suggestion is likely spam")
    auto_category = models.CharField(max_length=100, null=True, blank=True, help_text="Auto-detected category")

    def __str__(self):
        return self.title

class Reply(models.Model):
    suggestion = models.ForeignKey(Suggestion, on_delete=models.CASCADE, related_name='replies')
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='admin_replies')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        admin_name = self.admin.username if isinstance(self.admin, User) else 'Admin'
        suggestion_title = self.suggestion.title if isinstance(self.suggestion, Suggestion) else 'Suggestion'
        return f"Reply to {suggestion_title} by {admin_name}"

class CategoryAdmin(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='category_admin')
    categories = models.ManyToManyField(Category, related_name='admins')

    def save(self, *args, **kwargs):
        self.user.is_staff = True
        self.user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} (Category Admin)"
