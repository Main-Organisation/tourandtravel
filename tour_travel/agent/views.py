from datetime import datetime
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Agent, Booking
from .helpers import validate_user
from home.models import Country

# Create your views here.


class AgentSignupView(View):
    def get(self, request):
        return render(request, 'agent/agent_signup.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile_number = request.POST.get('mobile')
        company_name = request.POST.get('company')
        country = request.POST.get('country')
        city = request.POST.get('city')
        try:
            country_obj = Country.objects.get(id=country)
        except Country.DoesNotExist:
            messages.error(request, _('Country does not exist.'))
            return redirect('agent-signup')
        data = {
            'username': username,
            'email': email,
        }
        # check if username or email is registered or not
        errors = validate_user(**data)
        if errors or len(errors) > 0:
            for error in errors:
                messages.error(request, error)
            return redirect('agent-signup')
        try:
            _user = User(
                username=username, email=email, password=password,
                first_name=first_name, last_name=last_name)
            validate_password(password, _user)
        except Exception as e:
            messages.error(request, str(e))
            return redirect('agent-signup')
        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=username, email=email, password=password,
                    first_name=first_name, last_name=last_name)
                agent = Agent.objects.create(
                    user=user,
                    email=email,
                    mobile_number=mobile_number,
                    company_name=company_name,
                    country=country_obj,
                    city=city,
                )
            messages.success(request, _(
                f"Registration Success, your AGN_CODE is: {agent.agent_code}, you can login once verified."
            ))
            return redirect('agent-login')
        except Exception as e:
            messages.error(request, str(e))
            return redirect('agent-signup')
    

class AgentLoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('agent-home')
        return render(request, 'home/index.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        agn_code = request.POST.get('agn_code')
        
        user = User.objects.filter(username=username)
        if user.exists():
            user = user.first()
            if user.agent: 
                if user.agent.agent_code != agn_code:
                    messages.error(request, _('Invalid Agent Code'))
                    return redirect('agent-login')
                elif not user.agent.is_verify:
                    messages.error(request, _("Your account is not verified yet"))
                    return redirect('agent-login')
                else:
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                        login(request, user)
                        return redirect('agent-dashboard-first-page')
                    else:
                        messages.error(request, _("Invalid Credentials!"))
                        return redirect('agent-login')
            else:
                messages.error(request, _("No agent account found with given credentials"))
                return redirect('agent-login')
        else:
            messages.error(request, _("Invalid Credentials!"))
            return redirect('agent-login')
        

class AgentDashboardView(LoginRequiredMixin, View):
    login_url = 'agent-login'
    def get(self, request):
        return render(request, 'agent/agent_dashboard.html')
    

class AgentLogoutView(LoginRequiredMixin, View):
    login_url = 'agent-login'
    def get(self, request):
        logout(request)
        messages.success(request, _('Logged out successfully'))
        return redirect('index')
    

class AgentDashboardFirstPage(LoginRequiredMixin, View):
    login_url = 'agent-login'

    def get(self, request):
        if not request.user.agent:
            return redirect('agent-login')
        countries = Country.objects.all()
        context = {'countries': countries}
        return render(request, 'agent/agent_dashboard.html', context)
    

class AgentDashboardSecondPage(LoginRequiredMixin, View):
    login_url = 'agent-login'

    def get(self, request):
        if not request.user.agent:
            return redirect('agent-login')
        country_id = request.GET.get('destination')
        if country_id:
            # Set the selected_country_id in session
            request.session['selected_country_id'] = country_id
        country_id_from_session = request.session.get('selected_country_id')
        if not country_id_from_session:
            # If country ID is not found in session, redirect to first page
            messages.error(request, _('Please select a country first.'))
            return redirect('agent-dashboard-first-page')
        try:
            country = Country.objects.get(id=int(country_id_from_session))
        except Country.DoesNotExist:
            messages.error(request, _('Country does not exist.'))
            return redirect('agent-dashboard-first-page')
        query_number = request.GET.get('query_number')
        query_date_from = request.GET.get('query_date_from')
        query_date_to = request.GET.get('query_date_to')
        countries = Country.objects.all()
        bookings = Booking.objects.filter(agent=request.user.agent, location=country)

        if query_number:
            bookings = bookings.filter(web_id=query_number)
        if query_date_from or query_date_to:
            try:
                # Convert string date inputs to datetime objects
                if query_date_from:
                    date_from = datetime.strptime(query_date_from, '%Y-%m-%d')
                if query_date_to:
                    date_to = datetime.strptime(query_date_to, '%Y-%m-%d')
                
                # Filter bookings based on date range
                if query_date_from and query_date_to:
                    bookings = bookings.filter(created_at__gte=date_from, created_at__lte=date_to)
                elif query_date_from:
                    bookings = bookings.filter(created_at__gte=date_from)
                elif query_date_to:
                    bookings = bookings.filter(created_at__lte=date_to)
            except ValueError:
                messages.error(request, _('Invalid date format.'))
        context = {"bookings": bookings.order_by('-id'), "countries": countries}
        return render(request, 'agent/booking_list.html', context)
    
    def post(self, request):
        if not request.user.agent:
            return redirect('agent-login')
        country_id = request.POST.get('destination')
        return redirect('agent-dashboard-second-page')
    

class AgentBuildPackageView(LoginRequiredMixin, View):
    login_url = 'agent-login'

    def get(self, request):
        if not request.user.agent:
            return redirect('agent-login')
        country_id = request.session.get('selected_country_id')
        if not country_id:
            # If country ID is not found in session, redirect to first page
            messages.error(request, _('Please select a country first.'))
            return redirect('agent-dashboard-first-page')
        try:
            country = Country.objects.get(id=int(country_id))
        except Country.DoesNotExist:
            messages.error(request, _('Country does not exist.'))
            return redirect('agent-dashboard-first-page')
        context = {'country': country, 'agent': request.user.agent, 'countries': Country.objects.all()}
        return render(request, 'agent/build_package.html', context)
    
    def post(self, request):
        # Retrieve form data
        location_id = request.session.get('selected_country_id')
        arrival_date_str = request.POST.get('arrival')
        guest_title = request.POST.get('guest')
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        country_id = request.POST.get('country')
        adults = request.POST.get('adults')
        cwb = request.POST.get('cwb')
        cnb = request.POST.get('cnb')
        infants = request.POST.get('infants')

        # Validate form data and handle errors
        if not location_id:
            messages.error(request, _('Please select a country first.'))
            return redirect('agent-dashboard-first-page')

        try:
            location = Country.objects.get(id=int(location_id))
        except Country.DoesNotExist:
            messages.error(request, _('Selected country does not exist.'))
            return redirect('agent-dashboard-first-page')

        try:
            country = Country.objects.get(id=int(country_id))
        except Country.DoesNotExist:
            messages.error(request, _('Country does not exist.'))
            return redirect('agent-build-package')

        try:
            arrival_date = datetime.strptime(arrival_date_str, '%Y-%m-%d')
        except ValueError:
            messages.error(request, _('Invalid arrival date format.'))
            return redirect('agent-build-package')

        # Construct guest name
        guest_name = f"{guest_title} {first_name} {last_name}"

        # Create booking object
        booking = Booking(
            agent=request.user.agent,
            location=location,
            arrival_date=arrival_date,
            guest_name=guest_name,
            nationality=country.name,
            number_of_adults=adults,
            number_of_cwb=cwb,
            number_of_cnb=cnb,
            number_of_infants=infants
        )

        try:
            booking.full_clean()  # Validate the model fields
            booking.save(country=location.name)
            messages.success(request, _(f'Booking created successfully with web_id: {booking.web_id}.'))
            return redirect('agent-dashboard-second-page')
        except ValidationError as e:
            # Handle validation errors
            for field, errors in e.message_dict.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
            return redirect('agent-build-package')