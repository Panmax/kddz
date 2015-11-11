# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


class Goods(models.Model):
    goods_name = models.CharField(max_length=15)
    average_price = models.FloatField()
    last_price = models.FloatField()
    add_people = models.ForeignKey(User)
    update_date = models.DateField(auto_now_add=True)
    recent_sell = models.DateField(blank=True, null=True)
    is_delete = models.BooleanField(default=False)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.goods_name


class Shop(models.Model):
    name = models.CharField(max_length=10)
    principal = models.ForeignKey(User)  # 负责人

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name


class GoodsShop(models.Model):
    goods = models.ForeignKey(Goods)
    shop = models.ForeignKey(Shop)
    remain = models.IntegerField()  # 剩余
    last_updater = models.ForeignKey(User)
    last_update_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        return u"%s--%s" % (self.shop, self.goods)


class GoodsRecord(models.Model):
    goods = models.ForeignKey(Goods)
    shop = models.ForeignKey(Shop)
    change_num = models.IntegerField()
    updater = models.ForeignKey(User)
    date = models.DateTimeField(auto_now=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        return u"%s--%s" % (self.shop, self.goods)


class Order(models.Model):
    name = models.CharField(max_length=20)
    is_arrears = models.BooleanField()
    customer = models.CharField(max_length=10, default='无')
    phonenumber = models.CharField(max_length=15, default='无')
    address = models.CharField(max_length=50, default='无')
    remark = models.TextField(blank=True, null=True)
    all_price = models.FloatField(default=0)
    all_profit = models.FloatField(default=0)
    is_delete = models.BooleanField(default=False)
    updater = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name


class GoodsSellRecord(models.Model):
    goods = models.ForeignKey(Goods)
    shop = models.ForeignKey(Shop)
    sell_num = models.IntegerField()
    average_price = models.FloatField()
    sell_price = models.FloatField()
    is_arrears = models.BooleanField()
    customer = models.CharField(max_length=10, default='无')
    phonenumber = models.CharField(max_length=15, default='无')
    address = models.CharField(max_length=50, default='无')
    remark = models.TextField(blank=True, null=True)
    order = models.ForeignKey(Order, blank=True, null=True)
    is_delete = models.BooleanField(default=False)
    updater = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)

    def get_profit(self):
        profit = self.sell_num * (self.sell_price - self.average_price)
        return profit

    def get_receivable(self):
        receivable = self.sell_num * self.sell_price
        return receivable

    def __unicode__(self):  # Python 3: def __str__(self):
        return u"%s--%s" % (self.shop, self.goods)


class GoodsReturnRecord(models.Model):
    goods_sell_record = models.ForeignKey(GoodsSellRecord)
    updater = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)


class InboundChannel(models.Model):
    name = models.CharField(max_length=15)
    phonenumber = models.CharField(max_length=15)


class GoodsAddRecord(models.Model):
    goods = models.ForeignKey(Goods)
    shop = models.ForeignKey(Shop)
    number = models.IntegerField()
    price = models.FloatField()
    inbound_channel = models.ForeignKey(InboundChannel)
    remark = models.TextField(blank=True, null=True)
    updater = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        return u"%s--%s" % (self.shop, self.goods)


#
#
# class TransferGoods(models.Model):
# from_shop = models.ForeignKey(Shop, related_name='from_shop')
#     to_shop = models.ForeignKey(Shop, related_name='to_name')
#     goods = models.ForeignKey(Goods)
#     change_num = models.IntegerField()
#     updater = models.ForeignKey(User)
#     date = models.DateTimeField(auto_now_add=True)
#
#     def __unicode__(self):  # Python 3: def __str__(self):
#         return u"%s--%s--%s--%s" % (self.from_shop, self.to_shop, self.goods, self.change_num)
#
#
# class ChangePrice(models.Model):
#     goods = models.ForeignKey(Goods)
#     old_price = models.FloatField()
#     new_price = models.FloatField()
#     updater = models.ForeignKey(User)
#     date = models.DateTimeField(auto_now=True)
#
#     def __unicode__(self):  # Python 3: def __str__(self):
#         return self.goods.name
#
#
class Backup(models.Model):
    goods_name = models.CharField(max_length=15)
    kadi_count = models.IntegerField()
    is_lastet = models.BooleanField(default=True)
    save_datetime = models.DateTimeField(auto_now_add=True)


class LineItem(models.Model):
    product = models.ForeignKey(GoodsShop)
    unit_price = models.FloatField()
    quantity = models.IntegerField()

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.product.id


class Cart(object):
    def __init__(self):
        self.items = []
        self.total_price = 0

    def add_product(self, product, unit_price, quantity):
        self.total_price += unit_price * quantity
        self.items.append(LineItem(product=product, unit_price=unit_price, quantity=quantity))


class OtherCost(models.Model):
    purpose = models.CharField(max_length=10)
    price = models.FloatField()
    is_delete = models.BooleanField(default=False)
    updater = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)


class TransferShop(models.Model):
    name = models.CharField(max_length=20)
    phonenumber = models.CharField(max_length=15)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name


class TransferRecord(models.Model):
    transfer_shop = models.ForeignKey(TransferShop)
    goods = models.ForeignKey(Goods)
    count = models.IntegerField()
    remark = models.TextField()
    updater = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)


class ChangeCountRecord(models.Model):
    goods = models.ForeignKey(Goods)
    old_count = models.IntegerField()
    real_count = models.IntegerField()
    updater = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)


# 还款记录
class RefundRecord(models.Model):
    sell_record = models.ForeignKey(GoodsSellRecord)
    updater = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)

    def get_receivable(self):
        receivable = self.sell_record.sell_num * self.sell_record.sell_price
        return receivable