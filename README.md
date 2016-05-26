# React like templating for Python

This library provides React like templating for Python.

HTML elements are defined as classes (div, a, span) etc.
and you can create custom components by extending CustomComponent
class and defining its render method.


```py


render(div({"class": "foo"}, ["Hello", "World"]))

```

will output

```
<div>Hello World</div>
```

```py

class HelloWorld(CustomComponent):
      def render(self):
          return div({}, ["hello", "world"])


```
# TODO
