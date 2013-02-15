import ast

from restroom.views import (
    RestroomListView, RestroomSingleItemView)

from mock import Mock
from sure import expect

from django.http import (QueryDict,
                         HttpResponseForbidden)

from restroom import API


def test_restroom_list_view_for_get_when_allowed():
    # Given a restroom API instance
    api = API()

    # And we have a model
    MyModel = Mock()
    MyModel._meta.fields = [Mock(attname='id'), Mock(attname='text')]
    MyModel._meta.db_table = "table_mymodel"

    (MyModel.objects
     .filter
     .return_value
     .values
     .return_value) = [{'id': 1, 'text': 'Shalom'}]

    # And we register this model to the api
    api.register(MyModel)

    # The api view that is generated by api.generate_view
    # should return the expected json data when requested
    # via GET
    request = Mock(method='GET')
    view = RestroomListView.as_view(api=api,
                             allowed_methods=['GET'],
                             table_name='table_mymodel')

    response_from_GET = view(request)
    expected_response_json = [{'id': 1, 'text': 'Shalom'}]
    response_json = ast.literal_eval(response_from_GET.content)
    expect(response_json).to.equal(expected_response_json)


def test_restroom_list_view_for_GET_when_not_allowed_gets_forbidden():
    # Given a restroom API instance
    api = API()

    # And we have a model
    MyModel = Mock()
    MyModel._meta.fields = [Mock(attname='id'), Mock(attname='text')]
    MyModel._meta.db_table = "table_mymodel"

    # And we register this model to the api
    api.register(MyModel, {'allowed_methods': ['POST']})

    # The api view that is generated by api.generate_view
    # should return the expected json data when requested
    # via GET
    request = Mock(method='GET')
    view = RestroomListView.as_view(api=api,
                             allowed_methods=['POST'],
                             table_name='table_mymodel')
    response_from_GET = view(request)

    forbidden_response = HttpResponseForbidden()
    (expect(response_from_GET.status_code)
     .to.equal(forbidden_response.status_code))
    expect(response_from_GET.content).to.equal(forbidden_response.content)
    assert not MyModel.objects.values.called


def test_restroom_list_view_for_post_when_allowed():
    # Given a restroom API instance
    api = API()

    # And we have a model
    MyModel = Mock()
    MyModel._meta.fields = [Mock(attname='id'), Mock(attname='text')]
    MyModel._meta.db_table = "table_mymodel"

    # We mock the return of Django .create
    # to be an object with id 1 and text=Shalom
    # whose __class__._meta.db_table is `table_mymodel`
    returned_obj = Mock()
    returned_obj.id = 1
    returned_obj.text = 'Shalom'
    _meta = Mock(db_table='table_mymodel')
    returned_obj.__class__ = Mock(_meta=_meta)
    MyModel.objects.create.return_value = returned_obj

    # And we register this model to the api
    api.register(MyModel, {'allowed_methods': ['GET', 'POST']})

    # The api view that is generated by api.generate_view
    # should return the expected json data when requested
    # via POST
    request = Mock(method='POST')
    request.POST = QueryDict('text=Shalom')
    view = RestroomListView.as_view(api=api,
                             allowed_methods=['GET', 'POST'],
                             table_name='table_mymodel')
    response_from_POST = view(request)

    expected_response_json = {'id': 1, 'text': 'Shalom'}
    response_json = ast.literal_eval(response_from_POST.content)
    expect(response_json).to.equal(expected_response_json)
    MyModel.objects.create.assert_called_once_with(text='Shalom')


def test_restroom_list_view_for_POST_when_not_allowed_gets_forbidden():
    # Given a restroom API instance
    api = API()

    # And we have a model
    MyModel = Mock()
    MyModel._meta.fields = [Mock(attname='id'), Mock(attname='text')]
    MyModel._meta.db_table = "table_mymodel"

    # We mock the return of Django .create
    # to be an object with id 1 and text=Shalom
    # whose __class__._meta.db_table is `table_mymodel`
    returned_obj = Mock()
    returned_obj.id = 1
    returned_obj.text = 'Shalom'
    _meta = Mock(db_table='table_mymodel')
    returned_obj.__class__ = Mock(_meta=_meta)

    # And we register this model to the api
    api.register(MyModel, {'allowed_methods': ['GET']})

    # The api view that is generated by api.generate_view
    # should return the expected json data when requested
    # via POST
    request = Mock(method='POST')
    request.POST = QueryDict('text=Shalom')
    view = RestroomListView.as_view(api=api,
                             allowed_methods=['GET'],
                             table_name='table_mymodel')
    response_from_POST = view(request)
    forbidden_response = HttpResponseForbidden()
    (expect(response_from_POST.status_code)
     .to.equal(forbidden_response.status_code))
    expect(response_from_POST.content).to.equal(forbidden_response.content)
    assert not MyModel.objects.create.called


def test_restroom_list_view_for_DELETE_gets_forbidden_if_not_allowed():
    # Given a restroom API instance
    api = API()

    # And we have a model
    MyModel = Mock()
    fields = [Mock(attname='id'), Mock(attname='text')]
    db_table = "table_mymodel"
    _meta = Mock(fields=fields, db_table=db_table)
    MyModel._meta = _meta

    _id = 1

    returned_object = Mock()
    returned_object.id = _id
    returned_object.text = 'Shalom'
    returned_object.__class__ = MyModel

    # And we register this model to the api
    api.register(MyModel, {'allowed_methods': ['GET', 'POST']})

    request = Mock(method='DELETE')
    view = RestroomListView.as_view(api=api,
                             allowed_methods=['GET', 'POST'],
                             table_name='table_mymodel')

    response_from_DELETE = view(request)

    forbidden_response = HttpResponseForbidden()
    (expect(response_from_DELETE.status_code)
     .to.equal(forbidden_response.status_code))
    expect(response_from_DELETE.content).to.equal(forbidden_response.content)


def test_restroom_list_view_for_DELETE_gets_forbidden_even_if_allowed():
    # Given a restroom API instance
    api = API()

    # And we have a model
    MyModel = Mock()
    fields = [Mock(attname='id'), Mock(attname='text')]
    db_table = "table_mymodel"
    _meta = Mock(fields=fields, db_table=db_table)
    MyModel._meta = _meta

    _id = 1

    returned_object = Mock()
    returned_object.id = _id
    returned_object.text = 'Shalom'
    returned_object.__class__ = MyModel

    # And we register this model to the api
    api.register(MyModel, {'allowed_methods': ['GET', 'POST', 'DELETE']})

    request = Mock(method='DELETE')

    view = RestroomListView.as_view(api=api,
                             allowed_methods=['GET', 'POST'],
                             table_name='table_mymodel')

    response_from_DELETE = view(request)

    forbidden_response = HttpResponseForbidden()
    (expect(response_from_DELETE.status_code)
     .to.equal(forbidden_response.status_code))
    expect(response_from_DELETE.content).to.equal(forbidden_response.content)


def test_restroom_single_item_view_for_GET():
    # Given a restroom API instance
    api = API()

    # And we have a model
    MyModel = Mock()
    fields = [Mock(attname='id'), Mock(attname='text')]
    db_table = "table_mymodel"
    _meta = Mock(fields=fields, db_table=db_table)
    MyModel._meta = _meta

    _id = 1

    returned_object = Mock()
    returned_object.id = _id
    returned_object.text = 'Shalom'
    returned_object.__class__ = MyModel
    MyModel.objects.get.return_value = returned_object

    MyModel.objects.values.return_value = [{'id': _id, 'text': 'Shalom'}]
    # And we register this model to the api
    api.register(MyModel)

    # The api view that is generated by api.generate_view
    # should return the expected json data when requested
    # via GET
    request = Mock(method='GET')
    view = RestroomSingleItemView.as_view(api=api,
                             allowed_methods=['GET'],
                             table_name='table_mymodel')
    response_from_GET = view(request, _id)

    expected_response_json = {'id': _id, 'text': 'Shalom'}
    response_json = ast.literal_eval(response_from_GET.content)
    expect(response_json).to.equal(expected_response_json)


def test_restroom_single_item_view_for_GET_when_not_allowed_gets_forbidden():
    # Given a restroom API instance
    api = API()

    # And we have a model
    MyModel = Mock()
    fields = [Mock(attname='id'), Mock(attname='text')]
    db_table = "table_mymodel"
    _meta = Mock(fields=fields, db_table=db_table)
    MyModel._meta = _meta

    _id = 1

    returned_object = Mock()
    returned_object.id = _id
    returned_object.text = 'Shalom'
    returned_object.__class__ = MyModel

    # And we register this model to the api
    api.register(MyModel, {'allowed_methods': ['POST', 'PUT', 'DELETE']})

    # The api view that is generated by api.generate_view
    # should return the expected json data when requested
    # via GET
    request = Mock(method='GET')

    view = RestroomSingleItemView.as_view(api=api,
                             allowed_methods=['POST', 'PUT', 'DELETE'],
                             table_name='table_mymodel')
    response_from_GET = view(request, _id)

    forbidden_response = HttpResponseForbidden()
    (expect(response_from_GET.status_code)
     .to.equal(forbidden_response.status_code))
    expect(response_from_GET.content).to.equal(forbidden_response.content)
    assert not MyModel.objects.values.called


def test_restroom_single_item_view_for_DELETE():
    # Given a restroom API instance
    api = API()

    # And we have a model
    MyModel = Mock()
    fields = [Mock(attname='id'), Mock(attname='text')]
    db_table = "table_mymodel"
    _meta = Mock(fields=fields, db_table=db_table)
    MyModel._meta = _meta

    _id = 1

    returned_object = Mock()
    returned_object.id = _id
    returned_object.text = 'Shalom'
    returned_object.__class__ = MyModel
    MyModel.objects.get.return_value = returned_object

    MyModel.objects.values.return_value = [{'id': _id, 'text': 'Shalom'}]
    # And we register this model to the api
    api.register(MyModel, {'allowed_methods': ['GET', 'POST', 'DELETE']})

    request = Mock(method='DELETE')
    view = RestroomSingleItemView.as_view(api=api,
                             allowed_methods=['GET', 'POST', 'DELETE'],
                             table_name='table_mymodel')
    response_from_DELETE = view(request, _id)
    expected_response_json = {'status': 'deletion successful'}
    response_json = ast.literal_eval(response_from_DELETE.content)
    expect(response_json).to.equal(expected_response_json)
    returned_object.delete.assert_called_once()


def test_restroom_single_item_view_for_DELETE_not_allowed_gets_forbidden():
    # Given a restroom API instance
    api = API()

    # And we have a model
    MyModel = Mock()
    fields = [Mock(attname='id'), Mock(attname='text')]
    db_table = "table_mymodel"
    _meta = Mock(fields=fields, db_table=db_table)
    MyModel._meta = _meta

    _id = 1

    returned_object = Mock()
    returned_object.id = _id
    returned_object.text = 'Shalom'
    returned_object.__class__ = MyModel

    MyModel.objects.values.return_value = [{'id': _id, 'text': 'Shalom'}]
    # And we register this model to the api
    api.register(MyModel, {'allowed_methods': ['GET', 'POST']})

    request = Mock(method='DELETE')
    view = RestroomSingleItemView.as_view(api=api,
                             allowed_methods=['GET', 'POST'],
                             table_name='table_mymodel')
    response_from_DELETE = view(request, _id)

    forbidden_response = HttpResponseForbidden()

    (expect(response_from_DELETE.status_code)
     .to.equal(forbidden_response.status_code))
    expect(response_from_DELETE.content).to.equal(forbidden_response.content)
    assert not MyModel.objects.get.called
    assert not returned_object.delete.called


def test_restroom_single_item_view_for_POST_gets_forbidden_if_not_allowed():
    # Given a restroom API instance
    api = API()

    # And we have a model
    MyModel = Mock()
    MyModel._meta.fields = [Mock(attname='id'), Mock(attname='text')]
    MyModel._meta.db_table = "table_mymodel"

    # We mock the return of Django .create
    # to be an object with id 1 and text=Shalom
    # whose __class__._meta.db_table is `table_mymodel`
    returned_obj = Mock()
    returned_obj.id = 1
    returned_obj.text = 'Shalom'
    _meta = Mock(db_table='table_mymodel')
    returned_obj.__class__ = Mock(_meta=_meta)

    # And we register this model to the api
    api.register(MyModel, {'allowed_methods': ['GET']})

    # The api view that is generated by api.generate_view
    # should return the expected json data when requested
    # via POST
    request = Mock(method='POST')
    request.POST = QueryDict('text=Shalom')
    view = RestroomSingleItemView.as_view(api=api,
                             allowed_methods=['GET'],
                             table_name='table_mymodel')

    response_from_POST = view(request)

    forbidden_response = HttpResponseForbidden()
    (expect(response_from_POST.status_code)
     .to.equal(forbidden_response.status_code))
    expect(response_from_POST.content).to.equal(forbidden_response.content)


def test_restroom_single_item_view_for_POST_gets_forbidden_even_if_allowed():
    # Given a restroom API instance
    api = API()

    # And we have a model
    MyModel = Mock()
    MyModel._meta.fields = [Mock(attname='id'), Mock(attname='text')]
    MyModel._meta.db_table = "table_mymodel"

    # We mock the return of Django .create
    # to be an object with id 1 and text=Shalom
    # whose __class__._meta.db_table is `table_mymodel`
    returned_obj = Mock()
    returned_obj.id = 1
    returned_obj.text = 'Shalom'
    _meta = Mock(db_table='table_mymodel')
    returned_obj.__class__ = Mock(_meta=_meta)

    # And we register this model to the api
    api.register(MyModel, {'allowed_methods': ['GET', 'POST']})

    # The api view that is generated by api.generate_view
    # should return the expected json data when requested
    # via POST
    request = Mock(method='POST')
    request.POST = QueryDict('text=Shalom')

    view = RestroomSingleItemView.as_view(api=api,
                             allowed_methods=['GET', 'POST'],
                             table_name='table_mymodel')

    response_from_POST = view(request)

    forbidden_response = HttpResponseForbidden()
    (expect(response_from_POST.status_code)
     .to.equal(forbidden_response.status_code))
    expect(response_from_POST.content).to.equal(forbidden_response.content)


def test_restroom_single_item_view_for_PUT():
    # Given a restroom API instance
    api = API()

    # And we have a model
    MyModel = Mock()
    MyModel._meta.fields = [Mock(attname='id'), Mock(attname='text')]
    MyModel._meta.db_table = "table_mymodel"

    # We mock the return of Django .create
    # to be an object with id 1 and text=Shalom
    # whose __class__._meta.db_table is `table_mymodel`
    returned_obj = Mock()
    returned_obj.id = 1
    returned_obj.text = 'Shalom'
    _meta = Mock(db_table='table_mymodel')
    returned_obj.__class__ = Mock(_meta=_meta)
    MyModel.objects.get.return_value = returned_obj

    # And we register this model to the api
    api.register(MyModel, {'allowed_methods': ['GET', 'POST', 'PUT']})

    # The api view that is generated by api.generate_view
    # should return the expected json data when requested
    # via POST
    request = Mock(method='PUT')
    request.PUT = QueryDict('text=Hello')
    view = RestroomSingleItemView.as_view(api=api,
                             allowed_methods=['GET', 'POST', 'PUT'],
                             table_name='table_mymodel')

    response_from_PUT = view(request, returned_obj.id)
    expected_response_json = {'id': 1, 'text': 'Hello'}
    response_json = ast.literal_eval(response_from_PUT.content)
    expect(response_json).to.equal(expected_response_json)


def test_restroom_single_item_view_for_PUT_not_allowed_gets_forbidden():
    # Given a restroom API instance
    api = API()

    # And we have a model
    MyModel = Mock()
    MyModel._meta.fields = [Mock(attname='id'), Mock(attname='text')]
    MyModel._meta.db_table = "table_mymodel"

    # We mock the return of Django .create
    # to be an object with id 1 and text=Shalom
    # whose __class__._meta.db_table is `table_mymodel`
    returned_obj = Mock()
    returned_obj.id = 1
    returned_obj.text = 'Shalom'
    _meta = Mock(db_table='table_mymodel')
    returned_obj.__class__ = Mock(_meta=_meta)
    MyModel.objects.get.return_value = returned_obj

    # And we register this model to the api
    api.register(MyModel, {'allowed_methods': ['GET', 'POST']})

    # The api view that is generated by api.generate_view
    # should return the expected json data when requested
    # via POST
    request = Mock(method='PUT')
    request.PUT = QueryDict('text=Hello')
    view = RestroomSingleItemView.as_view(api=api,
                             allowed_methods=['GET', 'POST'],
                             table_name='table_mymodel')

    response_from_PUT = view(request, returned_obj.id)
    forbidden_response = HttpResponseForbidden()
    (expect(response_from_PUT.status_code)
     .to.equal(forbidden_response.status_code))
    (expect(response_from_PUT.content)
     .to.equal(forbidden_response.content))