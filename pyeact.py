
class Props(object):

    def __init__(self, attrs):
        self.attrs = attrs

    def __getattr__(self, key):
        return self.attrs[key]

    def __getitem__(self, key):
        return self.attrs[key]

try:
    from html import escape  # python 3
except:
    from cgi import escape


class Component(object):

    def __init__(self, attrs=None, children=None, *args):

        # support single argument case
        # TODO: maybe support differently for custom vs HTMLComponent's
        if attrs is not None and children is None:
            children = attrs
            attrs = None

        # support zero-argument case
        if attrs is None and children is None:
            attrs = {}
            children = []

        if attrs is None:
            attrs = {}
        self.attrs = attrs

        # support the case where children is improperly passed or passed not in a list, but as args
        if len(args) > 0:  # probably they passed args react-style, not in a list
            children = [children]
            children.extend(args)

        if not isinstance(children, list):
            children = [children]
        self.children = children

        self.props = Props(self.attrs)

    def render_inner_content(self):

        def render_child(child):
            if isinstance(child, Component):
                return child._render()
            elif isinstance(child, str):
                return escape(child)
            elif isinstance(child, (int, long, float, complex)):
                return escape(str(child))
            else:
                # TODO: warn maybe
                # raise RuntimeError("Unknown type of child %s" % child)
                return escape(str(child))

        def join_children(children_str):
            """Text nodes are prefixed with a space, tags with a new line"""
            output = ""
            for child_str in children_str:
                print child_str
                if len(child_str) > 0 and child_str[0] == "<":
                    output = output + "\n" + child_str
                else:
                    output = output + " " + child_str
            return output.strip()

        return join_children(map(render_child, self.children))

    def render_attributes(self):
        valid_list = ["style", "className"]
        conversions = {"className": "class"}

        attr_list = []
        for attr_name, attr_value in self.attrs.iteritems():
            if attr_name in valid_list or True:
                final_attr_name = conversions.get(attr_name, attr_name)
                final_attr_value = attr_value  # TODO: convert dict to string?
                attr_list.append(u'% s="%s"' % (final_attr_name, final_attr_value))
        if len(attr_list) > 0:
            return " " + u" ".join(attr_list)
        else:
            return ""

    def _render(self):
        raise "not implemented"


class HTMLComponent(Component):

    def _render(self):
        tag_name = self.__class__.__name__
        return u"<%(tag_name)s%(attributes)s>%(inner_content)s</%(tag_name)s>" % {"tag_name": tag_name,
                                                                                  "attributes": self.render_attributes(),
                                                                                  "inner_content": self.render_inner_content()}

    def render(self):
        return self._render()


class CustomComponent(Component):

    def _render(self):
        return self.render()._render()

HTML_TAGS = ["div", "span", "a"]  # TODO: auto-generate below from this list


class div(HTMLComponent):
    pass


class span(HTMLComponent):
    pass


def render(component):
    return component._render()


def remove_new_lines(x):
    return x.replace("\n", "")


def render_no_new_lines(component):
    return remove_new_lines(render(component))
