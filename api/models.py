from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import NewUser

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(Genre, related_name="titles", blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 related_name="titles",
                                 blank=True,
                                 null=True)


class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name="reviews",)
    text = models.TextField()
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)],
        default=0,
    )
    author = models.ForeignKey(NewUser, on_delete=models.CASCADE,
                               related_name="reviews")
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-pub_date"]


class Comment(models.Model):
    text = models.TextField()
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="comments")
    pub_date = models.DateTimeField("date published",
                                    auto_now_add=True)

    class Meta:
        ordering = ["-pub_date"]
