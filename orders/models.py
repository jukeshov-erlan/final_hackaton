from django.db import models
from django.contrib.auth import get_user_model
from movies.models import Movie
from django.utils.crypto import get_random_string


User = get_user_model() #

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    movies = models.ManyToManyField(Movie, through='CartMovie') #CartProduct посмотреть
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_price(self):
        return sum(movie.total_price() for movie in self.cart_movies.all())
    
    def clear_cart(self):
        self.movies.clear()

    def __str__(self):
        return f"Cart #{self.id} - User: {self.user.name}" # id and name??

class CartMovie(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_movies')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='cart_movies')
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.movie.price * self.quantity

    def __str__(self):
        return f"{self.quantity} - {self.movie.title}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, related_name='orders', null=True, blank=True, unique=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('completed', 'Completed'), ('canceled', 'Canceled'), ('pending', 'Pending')], default='pending')
    verification_code = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=False)
    payment_link = models.CharField(blank=True)

    def __str__(self):
        return f"Order #{self.id} with the total price {self.total_price} - User: {self.user.name}."
    
    def create_verification_code(self):
        code = get_random_string(10)
        self.verification_code = code 
        self.save()

# class OrderHistory(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, related_name='order_history')

#     def __str__(self):
#         return str(self.order)

    
