from django.db import models


class Person(models.Model):
    iin = models.CharField(max_length=128)
    age = models.IntegerField()

    def to_json(self):
        return {
            'iin': self.iin,
            'age': self.age
        }
