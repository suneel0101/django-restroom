from django.db import models
from restroom import expose, API


class MyModel(models.Model):
    name = models.CharField(max_length=150)

exposed_model_to_serialize_api = API()


@expose(api=exposed_model_to_serialize_api,
        fields=['short_title', 'author', 'id'])
class ExposedModelToSerialize(models.Model):
    short_title = models.CharField(max_length=150)
    expired = models.BooleanField(default=False)
    author = models.CharField(max_length=120)
    status = models.IntegerField(default=1)

another_test_api = API()

@expose(api=another_test_api,
        fields=['text', 'slug', 'id', 'active'])
class AnotherModel(models.Model):
    text = models.CharField(null=False, blank=False, max_length=50)
    slug = models.SlugField(unique=True)
    active = models.BooleanField(blank=False)
