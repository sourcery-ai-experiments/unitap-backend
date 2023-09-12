from django.db import models
from authentication.models import UserProfile
from core.models import UserConstraint
from django.utils import timezone


class Constraint(UserConstraint):
    pass


class Tag(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# the Mission class which is the main model of the app
class Mission(models.Model):
    title = models.CharField(max_length=200)
    creator_name = models.CharField(max_length=200, null=True, blank=True)
    creator_url = models.URLField(max_length=200, null=True, blank=True)
    discord_url = models.URLField(max_length=200, null=True, blank=True)
    twitter_url = models.URLField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    imageUrl = models.CharField(max_length=200, null=True, blank=True)
    is_promoted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, blank=True)
    constraints = models.ManyToManyField(
        Constraint, blank=True, related_name="missions"
    )
    constraint_params = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=True)

    def __str__(self):
        return self.title

    @property
    def total_XP(self):
        pass


class Referral(models.Model):
    mission = models.ForeignKey(
        Mission, on_delete=models.CASCADE, related_name="referrals"
    )
    profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="referrals_recieved"
    )
    referred_by = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, null=True, related_name="referals_made"
    )

    created_at = models.DateTimeField(auto_now_add=True, editable=True)

    def __str__(self):
        return f"{self.profile} referred by {self.referred_by} for {self.mission}"
