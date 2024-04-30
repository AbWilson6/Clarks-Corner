from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import os
from .managers import CustomUserManager


# need to fix this
def custom_email_validator(value):
    if not value.endswith('@clarku.edu'):
        raise ValidationError(('Invalid email address. Only clarku.edu addresses are allowed.'))


class Shopping_User(AbstractUser):
    clark_email = models.EmailField(max_length=50, unique=True, validators=[custom_email_validator])
    products = models.ManyToManyField("Product", through="has_in_cart")

    objects = CustomUserManager()

    def __str__(self):
        return self.clark_email


RATING_CHOICES = (
    (1, "1"),
    (2, "2"),
    (3, "3"),
    (4, "4"),
    (5, "5"),
)

class Review(models.Model):
    review_id = models.IntegerField(primary_key=True)
    r_description = models.TextField()
    send_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_reviews')
    receive_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_reviews')
    rating_number = models.IntegerField(choices=RATING_CHOICES)

    def __str__(self):
        return "Review ID: " + str(self.review_id)
    

PRODUCT_CHOICES = (
    ("textbooks", "Textbook"),
    ("electronics", "Electronic"),
    ("fashion", "Fashion"),
    ("housing", "Housing & Living"),
    ("stationary", "Stationary Item"),
    ("collectibles", "Collectible"),
)

def product_image_upload(instance, filename):
    # Get the file extension
    ext = filename.split('.')[-1]
    # Generate a new filename based on the product ID
    new_filename = f"{instance.product_id}.{ext}"
    # Return the new path
    # Return the new path
    return os.path.join('uploaded', new_filename)

class Product(models.Model):
    product_id = models.IntegerField(primary_key=True)
    p_image = models.ImageField(upload_to=product_image_upload)
    p_name = models.CharField(max_length=100)
    p_description = models.TextField()
    category = models.CharField(max_length=100, choices=PRODUCT_CHOICES)
    price = models.DecimalField(decimal_places=2, max_digits=7)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.p_name

    def save(self, *args, **kwargs):
        # Call the parent class's save method to ensure all fields are saved
        super(Product, self).save(*args, **kwargs)
        # Check if product_id has been generated (it's an AutoField)
        if not self.product_id:
            # Reload the instance to obtain the auto-generated product_id
            self.refresh_from_db()
        # Rename the image file to match the product ID
        self.p_image.name = product_image_upload(self, self.p_image.name)
        # Call the parent class's save method again to save the renamed image field
        super(Product, self).save(*args, **kwargs)

class has_in_cart(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    p_id = models.ForeignKey('Product', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user_id.username} has {self.p_id.p_name} in cart"

    def clean(self):
        # Check if the user is trying to add their own item to their cart
        if self.user_id == self.p_id.seller:
            raise ValidationError("You cannot add your own item to your cart.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Receipt(models.Model):
    receipt_id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField()
    products_bought = models.TextField()
    total_price = models.IntegerField()

    def __str__(self):
        return "Receipt ID: " + str(self.receipt_id)
