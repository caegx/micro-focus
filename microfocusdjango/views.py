from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser, AccessKey, Payment
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.conf import settings
from .decorators import unauthenticated_user
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.views import View
from .utils import account_activation_token
from django.http import Http404, JsonResponse, HttpResponse



def home(request):
    return render(request, 'home.html')

@unauthenticated_user
def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        repeat_password = request.POST['repeatPassword']
        if password == repeat_password:
            if CustomUser.objects.filter(email=email).exists():
                error_message = 'Email already in use'
                return render(request, 'register.html', {'error_message': error_message})
            
            else:
                user = CustomUser.objects.create_user(email=email)
                user.set_password(password)
                user.is_active = False
                user.save()

                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={'uidb64': uidb64, 'token': account_activation_token.make_token(user)})
                activate_url = f'http://{domain}{link}'
                subject = 'Activate your account'
                message = f'Click the following link to activate your account: {activate_url} '
                sender_email = settings.EMAIL_HOST_USER

                send_mail(subject, message, sender_email, [email])
                return redirect('login')
                
                
        else:
            error_message = 'Passwords do not match'
            return render(request, 'register.html', {'error_message': error_message})
    
    return render(request, 'register.html')


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return render(request, 'activation_success.html')
        else:
            support = settings.EMAIL_HOST_USER
            return render(request, 'activation_failed.html', {'support': support})


@unauthenticated_user
def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            if user.role == 'admin': 
                login(request, user)
                return redirect('admin_dashboard')
        
            elif user.role == 'school':
                login(request, user)
                return redirect('school_dashboard')
        else:
            error_message = "Invalid email or password"
            return render(request, 'login.html', {'error_message': error_message})
        
    return render(request, 'login.html')


class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset_form.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'



@login_required
def school_dashboard(request):
    current_user = request.user
    access_keys = AccessKey.objects.filter(user=current_user)
    return render(request, 'school_dashboard.html', {'access_keys': access_keys})


@login_required
def admin_dashboard(request):
    access_keys = AccessKey.objects.all()
    return render(request, 'admin_dashboard.html', {'access_keys': access_keys})


@login_required
def logout_user(request):
    logout(request)
    return redirect('/')


@login_required
def admin_revoke_key(request, key_id):
    access_key = get_object_or_404(AccessKey, pk=key_id)
    if access_key.status == 'revoked':
        messages.error(request, 'Access key already revoked')

    else:
        access_key.revoke_key()
        messages.success(request, 'Access key revoked successfully')
    
    return redirect('admin_dashboard')


@login_required
def initialize_payment(request):
    active_key = AccessKey.objects.filter(user=request.user, status='active')
    if active_key.exists():
        messages.error(request, "You already have an active access key.")
        return redirect('school_dashboard')
    
    else:
        if request.method == 'POST':
            email = request.POST['email']
            amount_str = 100
            amount = float(amount_str)

            if not email:
                messages.error(request, 'Enter email')
            
            else:
                payment = Payment.objects.create(amount=amount, user=request.user, email=email)
                payment.save()
                paystack_pk = settings.PAYSTACK_PK
                return render(request, 'make_payment.html', {'payment': payment, 'paystack_pk': paystack_pk})
            
    return render(request, 'initialize_payment.html')


@login_required
def make_payment(request):
    return render(request, 'make_payment.html')


@login_required
def verify_payment(request, ref):
    try:
        payment = Payment.objects.get(ref=ref)
    except Payment.DoesNotExist:
        raise Http404("Payment not found")

    if payment.verified:
        messages.warning(request, 'Access key already generated for this payment.')
    else:
        verified = payment.verify_payment()
        if verified:
            access_key = AccessKey.objects.create(user=request.user)
            access_key.generate_key()
            messages.success(request, "Access key generated successfully.")
        else:
            messages.warning(request, 'Sorry payment could not be processed.')

    return redirect('school_dashboard')

@login_required
def get_active_key_details(request):
    if request.user.role == 'admin':
        school_email = request.GET.get('school_email')

        if not school_email and request.method == 'GET':
            school_email = request.GET.get('school_email')  

        if school_email:
            active_key = AccessKey.objects.filter(school_email=school_email, status='active').first()

            if active_key:
                data = {
                    'status': 200,
                    'message': 'Active access key found',
                    'key': active_key.key,
                    'date_of_procurement': active_key.date_of_procurement,
                    'expiry_date': active_key.expiry_date
                }

            else:
                data = {'status': 404, 'message': 'No active key found'}

            return JsonResponse(data)
        
        else:
            return JsonResponse({'status': 400, 'message': 'Invalid request'})
    
    else:
        return HttpResponse('You are not authorized to view this page')
