from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.db import IntegrityError


class CarPark(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    location = models.PointField()
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    price_list = models.OneToOneField('PriceList', on_delete=models.CASCADE, null=True)


class Opinion(models.Model):
    STARS_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    opinion = models.TextField()
    stars = models.PositiveSmallIntegerField(choices=STARS_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car_park = models.ForeignKey('CarPark', on_delete=models.CASCADE)


class PriceList(models.Model):
    free_of_charge = models.BooleanField(default=False)
    first_hour_fee = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    maximum_additional_fee = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    additional_fee_description = models.TextField(blank=True)
    votes = models.IntegerField(default=0)

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.price_list_votes = None

    def up_vote(self, user):
        try:
            self.price_list_votes.create(user=user, price_list=self, vote_type=True)
            self.votes += 1
            self.save()
        except IntegrityError:
            return 'already voted for'
        return 'ok'

    def down_vote(self, user):
        try:
            self.price_list_votes.create(user=user, price_list=self, vote_type=False)
            self.votes -= 1
            self.save()
        except IntegrityError:
            return 'already voted against'
        return 'ok'


class UserVotes(models.Model):
    user = models.ForeignKey(User, related_name='user_votes', on_delete=models.CASCADE)
    price_list = models.ForeignKey(PriceList, related_name='price_list_votes', on_delete=models.CASCADE)
    vote_type = models.BooleanField()

    class Meta:
        unique_together = ('user', 'price_list', 'vote_type')
