def countries_context(request):
    from home.models import Country
    countries = Country.objects.all()
    return {'countries': countries}