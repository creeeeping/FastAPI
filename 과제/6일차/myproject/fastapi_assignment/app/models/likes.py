from tortoise import Model, fields

class ReviewLike(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="review_likes")
    review = fields.ForeignKeyField("models.Review", related_name="likes")
    is_liked = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table='review_likes'
        unique_together=(('user','review'),)
