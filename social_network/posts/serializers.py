from django.conf import settings
from django.contrib.auth.models import User
from geopy.exc import GeocoderTimedOut
from rest_framework import serializers

from geo.GeoResolver import GeoResolver
from geo.LocationIsUndefined import LocationIsUndefined
from posts.models import Post, Comment, Reaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = "__all__"
        read_only_fields = ['author', 'post']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        validated_data['post'] = self.context['post']
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ['author', 'post']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        validated_data['post'] = self.context['post']

        return super().create(validated_data)


class CommentInPostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['author', 'text', 'commented_at']


class PostSerializer(serializers.ModelSerializer):
    comments = CommentInPostSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    image = serializers.ImageField()
    location = serializers.CharField(required=False)

    likes_count = serializers.SerializerMethodField(method_name='get_likes_count')

    class Meta:
        model = Post
        fields = ['id', 'author', 'text', 'image', 'location', 'created_at', 'comments', 'likes_count']

    def create(self, validated_data):
        if validated_data['location']:
            validated_data['geo_data'] = self.__location_to_geo_data(validated_data['location'])
            del validated_data['location']
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if validated_data['location']:
            validated_data['geo_data'] = self.__location_to_geo_data(validated_data['location'])
            del validated_data['location']
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['location'] = None
        if instance.geo_data:
            # Так как при сохранении гео данных мы сохраняем и полученный адрес, то оптимальнее использовать его
            # при отображении, а не делать доп запрос на каждый пост
            # Во-первых, это быстрее и меньше запросов,
            # во-вторых, обратный запрос по координатам отдает не всегда тот же адрес, который запрашивался изначально.
            # data['location'] = instance.geo_data.get('address')

            # Вариант, согласно заданию: При отображении, наоборот, по координатам отобразить название объекта, используя метод reverse()
            data['location'] = self.__coords_to_location(instance.geo_data)
        return data

    def get_likes_count(self, obj):
        return obj.reactions.count()

    def __location_to_geo_data(self, location, attempt=0) -> dict | None:
        attempts_count = 3
        attempt += 1
        try:
            geo_resolver = GeoResolver(settings.GEO_CODER)
            return geo_resolver.load_by_location(location).data()
        except LocationIsUndefined:
            return None
        except GeocoderTimedOut:
            if attempt > attempts_count:
                return None

            return self.__location_to_geo_data(location, attempt)

    def __coords_to_location(self, geo_data) -> dict | None:
        try:
            geo_resolver = GeoResolver(settings.GEO_CODER)
            geo_data = geo_resolver.load_by_coords(geo_data['latitude'], geo_data['longitude'])
            return geo_data.data().get('address')
        except LocationIsUndefined:
            return None
        except GeocoderTimedOut:
            return geo_data.get('address')
