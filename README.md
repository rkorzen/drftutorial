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
```