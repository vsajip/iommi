from django.urls import path
from django.utils.translation import gettext

from examples import (
    example_adding_decorator,
    example_links,
)
from examples.models import (
    Foo,
    TBar,
    TFoo,
)
from examples.views import (
    all_column_sorts,
    ExamplesPage,
)
from iommi import (
    Action,
    Column,
    html,
    Table,
)

examples = []

example = example_adding_decorator(examples)


@example(gettext('Readme example 1'))
def table_readme_example_1(request):
    # Say I have a class...
    class Foo(object):
        def __init__(self, i):
            self.a = i
            self.b = 'foo %s' % (i % 3)
            self.c = (i, 1, 2, 3, 4)

    # and a list of them
    foos = [Foo(i) for i in range(4)]

    # I can declare a table:
    class FooTable(Table):
        a = Column.number()  # This is a shortcut that results in the css class "rj" (for right justified) being added to the header and cell
        b = Column()
        c = Column(cell__format=lambda value, **_: value[-1])  # Display the last value of the tuple
        sum_c = Column(cell__value=lambda row, **_: sum(row.c), sortable=False)  # Calculate a value not present in Foo

    # now to get an HTML table:
    return FooTable(rows=foos)


@example(gettext('Readme example 2'))
def table_readme_example_2(request):
    class BarTable(Table):
        select = Column.select()  # Shortcut for creating checkboxes to select rows
        b__a = Column.number(  # Show "a" from "b". This works for plain old objects too.
            filter__include=True,  # put this field into the query language
        )
        c = Column(
            bulk__include=True,  # Enable bulk editing for this field
            filter__include=True,
        )

    return BarTable(rows=TBar.objects.all(), page_size=20)


@example(gettext('Auto from model example 1'))
def table_auto_example_1(request):
    return Table(
        auto__model=Foo,
    )


@example(gettext('Auto from model example 2'))
def table_auto_example_2(request):
    return Table(
        auto__model=Foo,
        rows=lambda table, **_: Foo.objects.all(),
    )


@example(gettext('Kitchen sink example'))
def table_kitchen_sink(request):
    class BarTable(Table):
        select = Column.select()  # Shortcut for creating checkboxes to select rows
        b__a = Column.number()  # Show "a" from "b". This works for plain old objects too.

        b = Column.from_model(
            model=TBar,
            model_field_name='b',
            bulk__include=True,
            filter__include=True,
        )
        c = Column(bulk__include=True)  # The form is created automatically

        d = Column(
            display_name='Display name',
            attr__class__css_class=True,
            header__url='https://docs.iommi.rocks',
            sortable=False,
            group='Foo',
            auto_rowspan=True,
            filter__include=True,
            cell__value=lambda row, **_: row.b.a // 3,
            cell__format=lambda value, **_: '- %s -' % value,
            cell__attrs__class={'text-center': True},
            cell__attrs__title='cell title',
            cell__url='url',
            cell__url_title='cell url title',
        )
        e = Column(group='Foo', cell__value='explicit value', sortable=False)
        f = Column(include=False, sortable=False)
        g = Column(attr='c', sortable=False)
        django_templates_for_cells = Column(
            sortable=False,
            cell__value=None,
            cell__template='kitchen_sink_cell_template.html',
            group='Bar',
        )

        class Meta:
            title = 'Kitchen sink'
            _name = 'bar'
            page_size = 20

    return BarTable(rows=TBar.objects.all())


example_6_view = Table(
    auto__model=TFoo,
    columns__a__bulk__include=True,
    bulk__actions__delete__include=True,
    extra_evaluated__report_name='example_download',
    columns__a__extra_evaluated__report_name='A'
).as_view()

example_6_view = example('Table expressed directly as a view function')(example_6_view)


class IndexPage(ExamplesPage):
    header = html.h1('Table examples')

    description = html.p('Some examples of iommi tables')

    all_fields = html.p(
        Action(
            display_name='Example with all available types of columns',
            attrs__href='all_columns',
        ),
        html.br(),
        after='example_6',
    )

    class Meta:
        parts = example_links(examples)


urlpatterns = [
    path('', IndexPage().as_view()),
    path('all_columns/', all_column_sorts),

    path('example_1/', table_readme_example_1, name='readme_example_1'),
    path('example_2/', table_readme_example_2, name='readme_example_2'),
    path('example_3/', table_auto_example_1, name='readme_example_1'),
    path('example_4/', table_auto_example_2, name='readme_example_2'),
    path('example_5/', table_kitchen_sink, name='kitchen_sink'),
    path('example_6/', example_6_view),
]
