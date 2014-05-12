from pyramid.view import view_config


@view_config(route_name='render', renderer='json')
def render(request):
    renders = request.POST.__dict__
    print 'got to renders'
    print renders
    return {}

