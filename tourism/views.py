from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from .models import TouristSpot, Reservation
from .forms import LimitedSpotReservationForm, UnlimitedSpotReservationForm, ReservationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import timedelta

# --- General Views ---

def home(request):
    spots = TouristSpot.objects.all()
    return render(request, 'tourism/home.html', {'spots': spots})

def about(request):
    about_info = "Cagdianao is rich in history and natural wonders..."
    return render(request, 'tourism/about.html', {'about_info': about_info})

def sign_up(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        age = request.POST.get('age')
        sex = request.POST.get('sex')
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            user.profile.age = age
            user.profile.sex = sex
            user.profile.save()
            login(request, user)
            return redirect('home')
    return render(request, 'tourism/sign_up.html')

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('officials_dashboard' if user.is_superuser else 'home')
        return render(request, 'tourism/login.html', {'error': 'Invalid username or password'})
    return render(request, 'tourism/login.html', {'form': AuthenticationForm()})

def user_logout(request):
    logout(request)
    return redirect('login')

def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)

@login_required
def officials_dashboard(request):
    if not request.user.is_superuser:
        return render(request, 'tourism/access_denied.html', {
            'message': 'Only Tourism Management Officials can access this section.'
        })
    spots = TouristSpot.objects.all()
    return render(request, 'tourism/officials_dashboard.html', {'spots': spots})

def tourist_spots(request):
    spots = TouristSpot.objects.all()
    reservations = Reservation.objects.all()
    return render(request, 'tourism/tourist_spots.html', {
        'spots': spots,
        'reservations': reservations,
    })

def map_view(request):
    return render(request, 'tourism/map.html')

# --- Booking with Date Range, Cottage Handling ---

@login_required
def book_reservation(request, spot_id):
    spot = get_object_or_404(TouristSpot, id=spot_id)

    if request.method == 'POST':
        form = ReservationForm(request.POST, tourist_spot=spot)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.spot = spot
            reservation.user = request.user
            reservation.save()
            messages.success(request, "Reservation successful!")
            return redirect('reservation_success', pk=reservation.pk)

    else:
        form = ReservationForm(tourist_spot=spot)

    return render(request, 'tourism/book_reservation.html', {'form': form, 'spot': spot})

@login_required
def reservation_success(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    return render(request, 'tourism/reservation_success.html', {'reservation': reservation})

@login_required
def edit_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    spot = reservation.spot
    form_class = LimitedSpotReservationForm if spot.is_limited else UnlimitedSpotReservationForm

    if request.method == 'POST':
        form = form_class(request.POST, instance=reservation, spot=spot)
        if form.is_valid():
            updated = form.save(commit=False)
            updated.spot = spot
            updated.user = request.user
            updated.start_date = form.cleaned_data['start_date']
            updated.end_date = form.cleaned_data['end_date']
            updated.time = form.cleaned_data['time']

            if spot.is_limited:
                for single_date in (updated.start_date + timedelta(n) for n in range((updated.end_date - updated.start_date).days + 1)):
                    day_count = Reservation.objects.filter(
                        spot=spot,
                        start_date__lte=single_date,
                        end_date__gte=single_date
                    ).exclude(pk=reservation.pk).count()
                    if day_count >= 5:
                        messages.error(request, f"Spot full on {single_date.strftime('%Y-%m-%d')}. Choose different dates.")
                        return render(request, "tourism/edit_reservation.html", {'form': form})

                for i in range(1, 6):
                    conflict = Reservation.objects.filter(
                        spot=spot,
                        start_date__lte=updated.end_date,
                        end_date__gte=updated.start_date,
                        cottage_number=i
                    ).exclude(pk=reservation.pk)
                    if not conflict.exists():
                        updated.cottage_number = i
                        break

            updated.save()
            messages.success(request, "Reservation updated successfully!")
            return redirect('reservation_success', pk=updated.pk)
    else:
        initial = {
            'start_date': reservation.start_date,
            'end_date': reservation.end_date,
            'time': reservation.time.strftime('%H:%M') if reservation.time else '',
        }
        form = form_class(instance=reservation, initial=initial, spot=spot)

    return render(request, 'tourism/edit_reservation.html', {'form': form})

# --- Other Views ---

@login_required
def cancel_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    reservation.delete()
    messages.success(request, "Reservation cancelled successfully.")
    return redirect('my_reservations')

@login_required
def my_reservations(request):
    reservations = Reservation.objects.filter(user=request.user).order_by('-start_date')
    return render(request, 'tourism/my_reservations.html', {'reservations': reservations})

def delete_reservation_official(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == 'POST':
        reservation.delete()
        messages.success(request, "Reservation deleted successfully.")
    return redirect('officials_dashboard')

def reservation_list(request):
    reservations = Reservation.objects.all().order_by('-start_date', 'time')
    return render(request, 'tourism/reservation_list.html', {'reservations': reservations})
