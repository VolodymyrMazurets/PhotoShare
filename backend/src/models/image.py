from tortoise.models import Model
from tortoise import fields

class Image(Model):
    id = fields.IntField(pk=True)
    data = fields.BinaryField()
    description = fields.CharField(max_length=255)

    class Meta:
        table = "images"
