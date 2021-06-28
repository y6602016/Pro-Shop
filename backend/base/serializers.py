from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, User, Order, OrderItem, ShippingAddress


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ["_id", "username", "email", "name", "isAdmin"]

    def get__id(self, instance):
        return instance.id

    def get_isAdmin(self, instance):
        return instance.is_staff

    def get_name(self, instance):
        name = instance.first_name + " " + instance.last_name
        if not name:
            name = instance.email
        return name


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ["_id", "username", "email", "name", "isAdmin", "token"]

    def get_token(self, instance):
        token = RefreshToken.for_user(instance)
        return str(token.access_token)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    orderItems = serializers.SerializerMethodField(read_only=True)
    shippingAddress = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = "__all__"

    def get_orderItems(self, instance):
        items = instance.orderitem_set.all()
        serializer = OrderItemSerializer(items, many=True)
        return serializer.data

    def get_shippingAddress(self, instance):
        try:
            address = ShippingAddressSerializer(instance.shippingAddress)
        except:
            address = False
        return address

    def get_user(self, instance):
        user = instance.user
        serializer = UserSerializer(user, many=False)
        return serializer.data
