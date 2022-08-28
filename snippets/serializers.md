## przykłady pracy w shell

>>> from pygments.lexers import get_all_lexers
>>> from pygments.styles import get_all_styles
>>> 
>>> 
>>> LEXER = [item for item in get_all_lexers() if item[1]]
>>> 
>>> LEXER


In [1]: from snippets.models import Snippet

In [2]: from snippets.serializers import SnippetSerializer

In [3]: from rest_framework.renderers import JSONRenderer

In [4]: from rest_framework.parsers import JSONParser


In [5]: snippet = Snippet(code='foo = "bar"\n')

In [6]: snippet.save()

In [7]: snippet = Snippet(code='print("hello world")\n')

In [8]: snippet.save()

In [9]: serializer = SnippetSerializer(snippet)

In [10]: serializer

In [11]: serializer.data
Out[11]: {'id': 2, 'title': '', 'code': 'print("hello world")\n', 'linenos': False, 'language': 'python', 'style': 'friendly'}

In [12]: type(serializer.data)
Out[12]: rest_framework.utils.serializer_helpers.ReturnDict

In [13]: json_content = JSONRenderer().render(serializer.data)

In [14]: json_content
Out[14]: b'{"id":2,"title":"","code":"print(\\"hello world\\")\\n","linenos":false,"language":"python","style":"friendly"}'

In [15]: import io

In [16]: stream = io.BytesIO(json_content)

In [17]: data = JSONParser().parse(stream)

In [18]: data
Out[18]: 
{'id': 2,
 'title': '',
 'code': 'print("hello world")\n',
 'linenos': False,
 'language': 'python',
 'style': 'friendly'}

In [19]: data = JSONParser().parse(json_content)
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
Input In [19], in <cell line: 1>()
----> 1 data = JSONParser().parse(json_content)

File ~/PycharmProjects/szkolenia/k-python-25-06-2022/drf_tutorial/venv/lib/python3.9/site-packages/rest_framework/parsers.py:65, in JSONParser.parse(self, stream, media_type, parser_context)
     63     decoded_stream = codecs.getreader(encoding)(stream)
     64     parse_constant = json.strict_constant if self.strict else None
---> 65     return json.load(decoded_stream, parse_constant=parse_constant)
     66 except ValueError as exc:
     67     raise ParseError('JSON parse error - %s' % str(exc))

File ~/PycharmProjects/szkolenia/k-python-25-06-2022/drf_tutorial/venv/lib/python3.9/site-packages/rest_framework/utils/json.py:31, in load(*args, **kwargs)
     28 @functools.wraps(json.load)
     29 def load(*args, **kwargs):
     30     kwargs.setdefault('parse_constant', strict_constant)
---> 31     return json.load(*args, **kwargs)

File /usr/local/Cellar/python@3.9/3.9.13_1/Frameworks/Python.framework/Versions/3.9/lib/python3.9/json/__init__.py:293, in load(fp, cls, object_hook, parse_float, parse_int, parse_constant, object_pairs_hook, **kw)
    274 def load(fp, *, cls=None, object_hook=None, parse_float=None,
    275         parse_int=None, parse_constant=None, object_pairs_hook=None, **kw):
    276     """Deserialize ``fp`` (a ``.read()``-supporting file-like object containing
    277     a JSON document) to a Python object.
    278 
   (...)
    291     kwarg; otherwise ``JSONDecoder`` is used.
    292     """
--> 293     return loads(fp.read(),
    294         cls=cls, object_hook=object_hook,
    295         parse_float=parse_float, parse_int=parse_int,
    296         parse_constant=parse_constant, object_pairs_hook=object_pairs_hook, **kw)

File /usr/local/Cellar/python@3.9/3.9.13_1/Frameworks/Python.framework/Versions/3.9/lib/python3.9/codecs.py:496, in StreamReader.read(self, size, chars, firstline)
    494 # we need more data
    495 if size < 0:
--> 496     newdata = self.stream.read()
    497 else:
    498     newdata = self.stream.read(size)

AttributeError: 'bytes' object has no attribute 'read'

In [20]: data
Out[20]: 
{'id': 2,
 'title': '',
 'code': 'print("hello world")\n',
 'linenos': False,
 'language': 'python',
 'style': 'friendly'}

In [21]: serializer = SnippetSerializer(data=data)

In [22]: serializer.is_valid()
Out[22]: True

In [23]: serializer.validated_data
Out[23]: 
OrderedDict([('title', ''),
             ('code', 'print("hello world")'),
             ('linenos', False),
             ('language', 'python'),
             ('style', 'friendly')])

In [24]: serializer.save()
Out[24]: <Snippet: Snippet object (3)>

In [25]: serializer = SnippetSerializer(Snippet.objects.all())

In [26]: serializer.data
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
File ~/PycharmProjects/szkolenia/k-python-25-06-2022/drf_tutorial/venv/lib/python3.9/site-packages/rest_framework/fields.py:457, in Field.get_attribute(self, instance)
    456 try:
--> 457     return get_attribute(instance, self.source_attrs)
    458 except BuiltinSignatureError as exc:

File ~/PycharmProjects/szkolenia/k-python-25-06-2022/drf_tutorial/venv/lib/python3.9/site-packages/rest_framework/fields.py:97, in get_attribute(instance, attrs)
     96     else:
---> 97         instance = getattr(instance, attr)
     98 except ObjectDoesNotExist:

AttributeError: 'QuerySet' object has no attribute 'code'

During handling of the above exception, another exception occurred:

AttributeError                            Traceback (most recent call last)
Input In [26], in <cell line: 1>()
----> 1 serializer.data

File ~/PycharmProjects/szkolenia/k-python-25-06-2022/drf_tutorial/venv/lib/python3.9/site-packages/rest_framework/serializers.py:555, in Serializer.data(self)
    553 @property
    554 def data(self):
--> 555     ret = super().data
    556     return ReturnDict(ret, serializer=self)

File ~/PycharmProjects/szkolenia/k-python-25-06-2022/drf_tutorial/venv/lib/python3.9/site-packages/rest_framework/serializers.py:253, in BaseSerializer.data(self)
    251 if not hasattr(self, '_data'):
    252     if self.instance is not None and not getattr(self, '_errors', None):
--> 253         self._data = self.to_representation(self.instance)
    254     elif hasattr(self, '_validated_data') and not getattr(self, '_errors', None):
    255         self._data = self.to_representation(self.validated_data)

File ~/PycharmProjects/szkolenia/k-python-25-06-2022/drf_tutorial/venv/lib/python3.9/site-packages/rest_framework/serializers.py:509, in Serializer.to_representation(self, instance)
    507 for field in fields:
    508     try:
--> 509         attribute = field.get_attribute(instance)
    510     except SkipField:
    511         continue

File ~/PycharmProjects/szkolenia/k-python-25-06-2022/drf_tutorial/venv/lib/python3.9/site-packages/rest_framework/fields.py:490, in Field.get_attribute(self, instance)
    476     raise SkipField()
    477 msg = (
    478     'Got {exc_type} when attempting to get a value for field '
    479     '`{field}` on serializer `{serializer}`.\nThe serializer '
   (...)
    488     )
    489 )
--> 490 raise type(exc)(msg)

AttributeError: Got AttributeError when attempting to get a value for field `code` on serializer `SnippetSerializer`.
The serializer field might be named incorrectly and not match any attribute or key on the `QuerySet` instance.
Original exception text was: 'QuerySet' object has no attribute 'code'.

In [27]: serializer = SnippetSerializer(Snippet.objects.all(), many=True)

In [28]: serializer.data
Out[28]: [OrderedDict([('id', 1), ('title', ''), ('code', 'foo = "bar"\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')]), OrderedDict([('id', 2), ('title', ''), ('code', 'print("hello world")\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')]), OrderedDict([('id', 3), ('title', ''), ('code', 'print("hello world")'), ('linenos', False), ('language', 'python'), ('style', 'friendly')])]

