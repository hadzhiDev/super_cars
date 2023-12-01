from rest_framework import serializers

from core.models import Category, Car, Brand, CarImage, CarAttribute


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class CarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = '__all__'


class ImageForCarCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarImage
        fields = ('id', 'image',)


class AttributeForCarCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarAttribute
        fields = ('id', 'name', 'value',)


class CreateCarSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = Car
        fields = '__all__'

    def create(self, validated_data):
        image = validated_data.pop('image', None)
        car = Car.objects.create(**validated_data)
        image_serializer = ImageForCarCreationSerializer(data=image)
        image_serializer.is_valid(raise_exception=True)
        image_serializer.save(car=car)
        return car


class ReadCarSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    owner = serializers.CharField(source='owner.username')
    owner_id = serializers.IntegerField(source='owner.id')
    image = serializers.SerializerMethodField()
    images = ImageForCarCreationSerializer(many=True)
    attributes = AttributeForCarCreationSerializer(many=True)

    class Meta:
        model = Car
        fields = '__all__'

    def get_image(self, item):
        req = self.context['request']
        if item.image:
            return req.build_absolute_uri(item.image.url)
        return None


class CarAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarAttribute
        fields = '__all__'


class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = '__all__'

