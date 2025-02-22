# DRF tutorial


## Po utworzeniu modeli i serializera (serializer.Serializer) sprawdzamy to w shell

```
$ python manage.py shell
>>> from snippets.models import Snippet
>>> from snippets.serializers import SnippetSerializer
>>> from rest_framework.renderers import JSONRenderer
>>> from rest_framework.parsers import JSONParser
>>> s1 = Snippet(code="foo = 'bar'\n")
>>> s1.save()
>>> s2 = Snippet(code='print("Hello world")\n')
>>> s2.save()
>>> serializer = SnippetSerializer(s2)

>>> serializer.data
{'id': 2, 'title': '', 'code': 'print("Hello world")\n', 'linenos': False, 'language': 'python', 'style': 'friendly'}

>>> content = JSONRenderer().render(serializer.data)
b'{"id":2,"title":"","code":"print(\\"Hello world\\")\\n","linenos":false,"language":"python","style":"friendly"}'

>>> import io
>>> stream = io.BytesIO(content)

>>> data = JSONParser().parse(stream)
>>> data
{'id': 2,
 'title': '',
 'code': 'print("Hello world")\n',
 'linenos': False,
 'language': 'python',
 'style': 'friendly'}

>>> type(data)
dict

>>> serializer = SnippetSerializer(data=data)
>>> serializer.is_valid()
True

>>> serializer.validated_data
{'title': '',
 'code': 'print("Hello world")',
 'linenos': False,
 'language': 'python',
 'style': 'friendly'}


>>> serializer.save()
>>> <Snippet: Snippet object (3)>
>>> serializer.data
{'id': 3, 'title': '', 'code': 'print("Hello world")', 'linenos': False, 'language': 'python', 'style': 'friendly'}

>>> snippets = SnippetSerializer(Snippet.objects.all(), many=True)
>>> snippets.data
[{'id': 1, 'title': '', 'code': "foo = 'bar'\n", 'linenos': False, 'language': 'python', 'style': 'friendly'}, {'id': 2, 'title': '', 'code': 'print("Hello world")\n', 'linenos': False, 'language': 'python', 'style': 'friendly'}, {'id': 3, 'title': '', 'code': 'print("Hello world")', 'linenos': False, 'language': 'python', 'style': 'friendly'}]


```

## Po zmianie na ModelSerializer w zasadzie pracuję tak samo 

```
>>> snippets = SnippetSerializer(Snippet.objects.all(), many=True)
>>> snippets.data
[{'id': 1, 'title': '', 'code': "foo = 'bar'\n", 'linenos': False, 'language': 'python', 'style': 'friendly'}, {'id': 2, 'title': '', 'code': 'print("Hello world")\n', 'linenos': False, 'language': 'python', 'style': 'friendly'}, {'id': 3, 'title': '', 'code': 'print("Hello world")', 'linenos': False, 'language': 'python', 'style': 'friendly'}]
```

## Komunikacja z API z poziomu klienta:

### z poziomu konsoli

#### CURL

#### httpie

pip install httpie


### z poziomu IDE (np. REST CLIENT)

* tworzymy dokument z rozszerzeniem http
* dajemy tam zapytania oddzielajac je ###

### Narzędzia takie jak POSTMAN, Insomnia



## Zadanie 1


Utwórz projekt movies_library.
Dodaj model Movie (title. genre, time, rate, number_of_rents)
Dodać do aplikacji blog operacje CRUD realizowane poprzez API


GET /api/v1/movies - lista filnow
POST /api/v1/movies - tworz nowy film

GET /api/v1/movies/1 - szczegoly filmu
PUT /api/v1/movies/1 - aktualizacja
DELETE /api/v1/movies/1 - usuniecie filmu