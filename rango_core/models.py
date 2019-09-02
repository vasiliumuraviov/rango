from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify


class Category(models.Model):
    max_lengths = {'name': 128}
    max_lengths['slug'] = max_lengths['name']

    # blank = False  - by default for fields
    # null = False - by default for fields
    # but TextField and CharField always stores ONLY ""(empty string), and never 'null'

    name = models.CharField(max_length=max_lengths['name'], unique=True,
                            blank=False, null=False)

    likes = models.IntegerField(default=0,
                                blank=False, null=False)

    views = models.IntegerField(default=0,
                                blank=False, null=False)

    slug = models.SlugField(max_length=max_lengths['name'], unique=True,
                            blank=False, null=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Page(models.Model):
    max_lengths = {'title': 128, 'url': 200}

    # related_name='pages' - param of ForeignKey? What does?
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)

    title = models.CharField(max_length=max_lengths['title'],
                             blank=False, null=False)

    url = models.URLField(max_length=max_lengths['url'],
                          blank=False, null=False)

    views = models.IntegerField(default=0,
                                blank=False, null=False)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    max_lengths = {'website': 200}

    user = models.OneToOneField(to=User, on_delete=models.CASCADE)

    #
    website = models.URLField(max_length=max_lengths['website'],
                              blank=True, null=False)

    picture = models.ImageField(upload_to='profile_images',
                                blank=True, null=False)

    def __str__(self):
        return f'{self.user.username}\'s profile'
