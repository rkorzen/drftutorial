from django.contrib.auth.models import User

from rest_framework import serializers

from snippets.models import Snippet



class SnippetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    file = serializers.FileField(required=False, write_only=True)
    code = serializers.CharField(required=False)

    class Meta:
        model = Snippet
        fields = ["id", "title", "code", "linenos", "language", "style", "owner", "file"]


    def validate(self, data):
        if not data.get('code') and not data.get('file'):
            raise serializers.ValidationError(
                "Musisz podać albo kod, albo plik."
            )
        if 'file' in data and 'code' in data:
            raise serializers.ValidationError(
                "Nie można jednocześnie podać pliku i kodu. Wybierz jeden sposób."
            )
        if 'file' in data:
            try:
                content = data['file'].read().decode('utf-8')
                data['code'] = content
                del data['file']
            except UnicodeDecodeError:
                raise serializers.ValidationError(
                    "Plik musi być w formacie tekstowym (UTF-8)"
                )
        return data


class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())


    class Meta:
        model = User
        fields = ["id", "username", "snippets"]