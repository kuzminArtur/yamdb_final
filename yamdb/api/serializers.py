from rest_framework import serializers
from ..models import Review, Comment, Category, Genre, Title


class ReviewSerializer(serializers.ModelSerializer):
    """ModelSerializer for Review."""
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Review
        exclude = ['title']

    def validate(self, attrs):
        if self.context.get('request').method == 'POST':
            user = self.context.get('request').user
            title_id = self.context.get('view').kwargs.get('title_id')
            if Review.objects.filter(
                    author=user,
                    title=title_id
            ).exists():
                raise serializers.ValidationError(
                    'Пользователь может оставить только один отзыв на объект')
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    """ModelSerializer for Comment."""
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class CategorySerializer(serializers.ModelSerializer):
    """Serializing categories."""

    class Meta:
        exclude = ('id',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Serializing categories."""

    class Meta:
        exclude = ('id',)
        model = Genre


class TitleCreateSerializer(serializers.ModelSerializer):
    """Serializing title for reading."""
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',

    )

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = ('genre', 'category')


class TitleDefaultSerializer(serializers.ModelSerializer):
    """Serializing title for update."""
    genre = GenreSerializer(many=True)
    category = CategorySerializer(required=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'
        depth = 1
