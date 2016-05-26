from pyeact import div, span, render, CustomComponent, render_no_new_lines, remove_new_lines


def test_single_div_single_child():
    assert render(div({}, ["foo"])) == "<div>foo</div>"


def test_single_div_single_child_no_list_wrapping():
    assert render(div({}, "foo")) == "<div>foo</div>"


def test_single_div_single_child_no_list_wrapping_no_attrs():
    assert render(div("foo")) == "<div>foo</div>"


def test_single_div_single_child_single_attribute():
    assert render(div({"foo": "bar", "className": "foo bar"}, ["foo"])) == """<div class="foo bar" foo="bar">foo</div>"""


def test_single_div_with_children():
    assert \
        render(div({"className": "foo"},
                   [div({},
                        [span({}, ["foo"])])])) == \
        """<div class="foo"><div><span>foo</span></div></div>"""


def test_custom_component_with_single_div():
    class HelloWorld(CustomComponent):

        def render(self):
            return div({}, ["Hello World"])

    assert render(HelloWorld({}, [])) == "<div>Hello World</div>"
    assert render(HelloWorld()) == "<div>Hello World</div>"


def test_custom_component_with_two_children():
    class HelloWorldTwoChildren(CustomComponent):

        def render(self):
            return div({}, [div({}, ["Hello World"]), div({}, ["Hello World"])])

    assert render_no_new_lines(HelloWorldTwoChildren({}, [])) == \
        remove_new_lines("""
<div>
<div>Hello World</div>
<div>Hello World</div>
</div>""")


def test_custom_component_with_render_method():

    class HelloWorldComponent(CustomComponent):

        def render(self):
            return div(["Hello", self.props.name, self.props['surname']])

    assert render_no_new_lines(HelloWorldComponent({"name": "Ustun", "surname": "Ozgur"}, [])) == remove_new_lines("<div>Hello Ustun Ozgur</div>")


def test_custom_component_with_render_method_and_some_computation_in_render():

    class HelloWorldComponent(CustomComponent):

        def render(self):
            return div({"class": "foo"},
                       ["Hello", self.props.name, self.props['surname'], ". My name is", len(self.props.name), "characters long."])

    assert render_no_new_lines(HelloWorldComponent({"name": "Ustun", "surname": "Ozgur"}, [])) == \
        remove_new_lines("""<div class="foo">Hello Ustun Ozgur . My name is 5 characters long.</div>""")


def test_custom_component_in_custom_component():

    class HelloWorldComponent(CustomComponent):

        def render(self):
            return div({"class": "foo"},
                       ["Hello", self.props.name, self.props['surname'], "."])

    class GreetComponent(CustomComponent):

        def render(self):
            # import ipdb
            # ipdb.set_trace()
            return div({},
                       [HelloWorldComponent({"name": "Ustun", "surname": "Ozgur"}, []),
                        HelloWorldComponent({"name": "Reyhan", "surname": "Ustun"}, [])])

    print render(GreetComponent())
    assert render_no_new_lines(GreetComponent()) == remove_new_lines("""<div><div class="foo">Hello Ustun Ozgur .</div><div class="foo">Hello Reyhan Ustun .</div></div>""")


def test_single_div_single_child_escape():
    assert render(div({}, ["<foo>"])) != "<div><foo></div>"
