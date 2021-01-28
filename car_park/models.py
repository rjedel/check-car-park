from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.db import IntegrityError


class CarPark(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    location = models.PointField()
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    free_of_charge = models.BooleanField(default=False)
    tariff = models.ForeignKey('Tariff', on_delete=models.CASCADE, null=True)
    categories = models.ManyToManyField('Category', related_name='car_parks')

    @property
    def longitude_x(self):
        return str(self.location.x).replace(',', '.')

    @property
    def latitude_y(self):
        return str(self.location.y).replace(',', '.')

    def __str__(self):
        return self.name


class Tariff(models.Model):
    tariffs_name = models.CharField(max_length=100, blank=True)
    first_hour_fee = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    maximum_additional_fee = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    additional_fee_description = models.TextField(blank=True)


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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_opinions')
    car_park = models.ForeignKey('CarPark', on_delete=models.CASCADE, related_name='car_park_opinions')
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    votes = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user_id', 'car_park_id',)

    def up_vote(self, user):
        try:
            self.opinion_votes.create(user=user, opinion=self, vote_type=True)
            self.votes += 1
            self.save()
        except IntegrityError:
            return 'already voted for'
        else:
            return 'ok'

    def down_vote(self, user):
        try:
            self.opinion_votes.create(user=user, opinion=self, vote_type=False)
            self.votes -= 1
            self.save()
        except IntegrityError:
            return 'already voted against'
        else:
            return 'ok'


class UserVotes(models.Model):
    user = models.ForeignKey(User, related_name='user_votes', on_delete=models.CASCADE)
    opinion = models.ForeignKey(Opinion, related_name='opinion_votes', on_delete=models.CASCADE)
    vote_type = models.BooleanField()

    class Meta:
        unique_together = ('user', 'opinion', 'vote_type',)


class SavedUserCarPark(models.Model):
    notes = models.TextField(blank=True, verbose_name='Notatki')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_saved_car_parks')
    car_park = models.ForeignKey('CarPark', on_delete=models.CASCADE, related_name='car_park_saved_car_parks')

    class Meta:
        unique_together = ('user_id', 'car_park_id',)


class Category(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
