from django.conf import settings
from django.db import models


class Store(models.Model):
    store_name = models.CharField(max_length=30)

    def __str__(self):
        return self.store_name


class StoreLocation(models.Model):
    store = models.ForeignKey(
        Store, on_delete=models.PROTECT, related_name="locations"
    )

    address = models.TextField()

    def __str__(self):
        return f"{self.store.store_name} - {self.address}"


class Receipt(models.Model):
    location = models.ForeignKey(
        StoreLocation, on_delete=models.PROTECT, related_name="receipts"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receipts"
    )
    date = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax_rate = models.DecimalField(
        max_digits=5, decimal_places=4, null=True, blank=True
    )
    tax_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    def __str__(self):
        return f"Receipt {self.pk} ({self.date}, {self.total})"


class Tag(models.Model):
    tag_name = models.CharField(max_length=30)
    is_standard = models.BooleanField(default=False)

    def __str__(self):
        return self.tag_name


def get_default_tag_id():
    """Look up the 'Miscellaneous' standard tag by name (see section 6)."""
    return Tag.objects.get(tag_name="Miscellaneous", is_standard=True).pk


class Item(models.Model):
    upc = models.CharField(max_length=12, null=True, blank=True)
    product_name = models.TextField()
    tag = models.ForeignKey(
        Tag,
        on_delete=models.PROTECT,
        related_name="items",
        default=get_default_tag_id()
    )

    def __str__(self):
        return self.product_name


class ItemStoreName(models.Model):

    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="store_names"
    )
    store = models.ForeignKey(
        Store, on_delete=models.PROTECT, related_name="item_names"
    )
    product_name_abbreviated = models.CharField(max_length=30)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["item", "store"], name="unique_item_store_name"
            ),
        ]
    def __str__(self):
        return self.product_name_abbreviated


class ReceiptItem(models.Model):
    receipt = models.ForeignKey(
        Receipt, on_delete=models.CASCADE, related_name="line_items"
    )
    item = models.ForeignKey(
        Item, on_delete=models.PROTECT, related_name="receipt_items"
    )
    quantity = models.DecimalField(max_digits=10, decimal_places=3)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.item}"


class UserTagAlias(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tag_aliases"
    )
    tag = models.ForeignKey(
        Tag, on_delete=models.PROTECT, related_name="user_aliases"
    )
    custom_tag_name = models.CharField(max_length=30)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "tag"], name="unique_user_tag_alias"
            ),
        ]

    def __str__(self):
        return self.custom_tag_name


class UserItemTag(models.Model):
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="item_tags"
    )
    item = models.ForeignKey(
        Item, on_delete=models.PROTECT, related_name="user_tags"
    )
    tag = models.ForeignKey(
        Tag, on_delete=models.PROTECT, related_name="user_item_tags"
    )
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "item"], name="unique_user_item_tag"
            ),
        ]    
    def __str__(self):
        return f"{self.user} tagged {self.item} as {self.tag}"


class UserStoreTag(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="store_tags"
    )
    store = models.ForeignKey(
        Store, on_delete=models.PROTECT, related_name="user_tags"
    )
    tag = models.ForeignKey(
        Tag, on_delete=models.PROTECT, related_name="user_store_tags"
    )
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "store"], name="unique_user_store_tag"
            ),
        ]
    def __str__(self):
        return f"{self.user} tagged {self.store} as {self.tag}"