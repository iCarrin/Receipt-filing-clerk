from django.contrib import admin

from .models import Store, StoreLocation, Receipt, Tag, Item, ReceiptItem, ItemStoreName, UserTagAlias, UserItemTag, UserStoreTag

for model in (Store, StoreLocation, Receipt, Tag, Item, ReceiptItem, ItemStoreName, UserTagAlias, UserItemTag, UserStoreTag):
    admin.site.register(model)
