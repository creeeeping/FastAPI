from tortoise import Model, fields

class Review(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="reviews")
    movie = fields.ForeignKeyField("models.Movie", related_name="reviews")
    title = fields.CharField(max_length=50)
    content = fields.CharField(max_length=255)
    review_image_url = fields.CharField(max_length=255, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table='reviews'
        unique_together=(('user','movie'),)
