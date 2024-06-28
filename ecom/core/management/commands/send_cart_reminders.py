from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from core.models import Cart

class Command(BaseCommand):
    help = 'Sends an email reminder to users with items in their carts.'

    def handle(self, *args, **kwargs):
        carts = Cart.objects.exclude(items__isnull=True)
        for cart in carts:
            message = f"Dear {cart.user.username}, you have items pending in your cart."
            send_mail(
                'Cart Reminder',
                message,
                settings.DEFAULT_FROM_EMAIL,
                [cart.user.email],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully sent reminder to {cart.user.email}.'))