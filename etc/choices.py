USER_TYPE_CHOICES = [
    ('admin', 'Admin'),
    ('client', 'Client'),
    ('seller', 'Seller'),
    ('developer', 'Developer'),
]


GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'),
)


PRODUCT_SIZE = (
    ('XS', 'Extra Small'),
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
    ('XL', 'Extra Large'),
    ('XXL', 'Double Extra Large'),
    ('XXXL', 'Triple Extra Large'),
    ('OVER', 'Oversize'),
    ('ONE_SIZE', 'One Size Fits All'),
    ('GEN', 'General Size'),
)


COLOR_CHOICES = [
    ('#FF0000', 'Red'),
    ('#00FF00', 'Green'),
    ('#0000FF', 'Blue'),
    ('#FFFF00', 'Yellow'),
    ('#FFA500', 'Orange'),
    ('#800080', 'Purple'),
    ('#FFC0CB', 'Pink'),
    ('#A52A2A', 'Brown'),
    ('#808080', 'Gray'),
    ('#000000', 'Black'),
    ('#FFFFFF', 'White'),
    ('#00FFFF', 'Cyan'),
    ('#008080', 'Teal'),
    ('#FFD700', 'Gold'),
    ('#4B0082', 'Indigo'),
    ('#F5F5DC', 'Beige'),
    ('#D2691E', 'Chocolate'),
]


MEDIA_TYPE_CHOICES = [
    ('image', 'Image'),
    ('video', 'Video'),
    ('audio', 'Audio'),
    ('document', 'Document'),
    ('other', 'Other'),
]

INVOICE_STATUS = (
    ("pending", "Pending"),
    ("paid", "Paid"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
    ("cancelled", "Cancelled"),
    ("refunded", "Refunded"),
)


PAYMENT_LOG_STATUS = [
    ('PENDING', 'Pending'),                        # Payment is not yet processed
    ('PROCESSING', 'Processing'),                  # Payment is being processed
    ('SUCCESS', 'Success'),                        # Payment succeeded
    ('FAILED', 'Failed'),                          # Payment failed
    ('CANCELLED', 'Cancelled by user or system'),  # User canceled or system auto-cancelled
    ('EXPIRED', 'Expired'),                        # Payment link or session expired
    ('REFUNDED', 'Refunded'),                      # Full refund issued
    ('PARTIALLY_REFUNDED', 'Partially Refunded'),  # Partial refund issued
    ('CHARGEBACK', 'Chargeback Requested'),        # Dispute/chargeback from user
    ('AUTHORIZED', 'Authorized'),                  # Authorized but not captured yet
    ('CAPTURED', 'Captured'),                      # Authorized and then captured
    ('DECLINED', 'Declined by provider'),          # Bank or provider declined it
    ('WAITING_3DS', 'Waiting 3DS Authentication'), # Waiting for 3D Secure check
]


PAYMENT_METHOD_CHOICES = [
    ('CASH', 'Cash on Delivery'),
    ('CARD', 'Credit/Debit Card'),
    ('PAYPAL', 'PayPal'),
    ('STRIPE', 'Stripe'),
    ('BANK', 'Bank Transfer'),
    ('VISA', 'Visa'),
    ('MASTERCARD', 'MasterCard'),
    ('APPLE', 'Apple Pay'),
    ('GOOGLE', 'Google Pay'),
    ('VODAFONE', 'Vodafone Cash'),
    ('FAWRY', 'Fawry'),
    ('AMAN', 'Aman'),
    ('MEEZA', 'Meeza Card'),
    ('CRYPTO', 'Cryptocurrency'),
    ('OTHER', 'Other'),
]
