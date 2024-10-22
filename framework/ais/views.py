from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import StudentsForm
from .models import Students
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from .decorators import group_required
from rest_framework import viewsets
from .serializers import StudentsSerializer
import requests
from django.http import JsonResponse, HttpResponseForbidden

# API
class StudentsViewSet(viewsets.ModelViewSet):
    queryset = Students.objects.all() # Mengambil semua data mahasiswa dari database
    serializer_class = StudentsSerializer # Menggunakan serializer yang sudah kita buat

# Create your views here.
def homepage(request):
    return render(request, 'homepage/index.html')

def about(request):
    return render(request, 'homepage/about.html')


# READ Mahasiswa
def student_index(request):
    query = request.GET.get('q')
    
    # Mengirim GET request ke API
    if query:
        response = requests.get(f'http://127.0.0.1:8000/api/students/?search={query}')
    else:
        response = requests.get('http://127.0.0.1:8000/api/students/')
    
    if response.status_code == 200:
        students = response.json()  # Ambil data mahasiswa dalam format JSON
    else:
        students = []  # Jika gagal, siapkan list kosong
    
    # Render halaman index mahasiswa
    return render(request, 'student/index.html', {
        'students': students,  # Data dari API
        'query': query  # Kirimkan query ke template jika ada
    })

# CREATE Mahasiswa
def student_create(request):
    if request.method == 'POST':
        form_data = {
            'name': request.POST.get('name'),
            'nim': request.POST.get('nim'),
            'email': request.POST.get('email'),
            'phone_number': request.POST.get('phone_number'),
            'year': request.POST.get('year'),  # Pastikan tahun juga diambil dari form
            'teacher': request.POST.get('teacher'),  # ID dosen dari dropdown
        }

        # Mengirim POST request ke API
        response = requests.post('http://127.0.0.1:8000/api/students/', data=form_data)

        if response.status_code == 201:  # Created
            messages.success(request, 'Mahasiswa berhasil dibuat!')  # Pesan sukses
            return redirect('student_index')  # Redirect ke halaman index mahasiswa
        else:
            messages.error(request, f'Gagal membuat mahasiswa: {response.text}')  # Pesan error jika gagal

    else:
        form_data = {}
    
    # Render halaman jika bukan POST, atau jika ada error
    return render(request, 'student/create.html', {'form': StudentsForm()})  # Kirimkan form ke template

# UPDATE Mahasiswa
def student_update(request, student_id):
    if request.method == 'POST':
        form_data = {
            'name': request.POST.get('name'),
            'nim': request.POST.get('nim'),
            'email': request.POST.get('email'),
            'phone_number': request.POST.get('phone_number'),
            'year': request.POST.get('year'),  # Ambil tahun dari form
            'teacher': request.POST.get('teacher'),  # ID dosen dari dropdown
        }

        # Mengirim PUT request ke API
        response = requests.put(f'http://127.0.0.1:8000/api/students/{student_id}/', data=form_data)

        if response.status_code == 200:  # OK
            messages.success(request, 'Data mahasiswa berhasil diubah!')
            return redirect('student_index')  # Redirect ke halaman index mahasiswa
        else:
            messages.error(request, f'Gagal mengubah mahasiswa: {response.text}')

    else:
        # Mengambil data mahasiswa dari API untuk mengisi form
        response = requests.get(f'http://127.0.0.1:8000/api/students/{student_id}/')

        if response.status_code == 200:
            student = response.json()  # Ambil data mahasiswa dalam format JSON
            form = StudentsForm(initial=student)  # Isi form dengan data mahasiswa
        else:
            return HttpResponseForbidden("Data mahasiswa tidak ditemukan.")

    return render(request, 'student/update.html', {'form': form, 'student': student})

# DELETE Mahasiswa
def student_delete(request, student_id):
    if request.method == 'POST':  # Hanya menerima POST untuk menghapus
        # Mengirim DELETE request ke API
        response = requests.delete(f'http://127.0.0.1:8000/api/students/{student_id}/')

        if response.status_code == 204:  # No Content, berarti berhasil dihapus
            messages.success(request, 'Data mahasiswa berhasil dihapus')
            return JsonResponse({'success': True})  # Mengembalikan respons JSON success
        else:
            messages.error(request, f'Gagal menghapus mahasiswa: {response.text}')
            return JsonResponse({'success': False, 'error': response.text})  # Mengembalikan error ke JSON
    else:
        return HttpResponseForbidden("Metode tidak diizinkan.")

# * DASHBOARD
@login_required
def dashboard(request):
    user = request.user
    if user.groups.filter(name='Admin').exists():
        return redirect('dashboard_admin')
    elif user.groups.filter(name='Student').exists():
        return redirect('dashboard_student')
    elif user.groups.filter(name='Teacher').exists():
        return redirect('dashboard_teacher')
    return HttpResponseForbidden("You do not have permission to access this page.")

@login_required
def dashboard_admin(request):
    return render(request, 'dashboard/admin.html')

@login_required
def dashboard_student(request):
    return render(request, 'dashboard/student.html')

@login_required
def dashboard_teacher(request):
    return render(request, 'dashboard/teacher.html')

@group_required('Admin')
def dashboard_admin(request):
    return render(request, 'dashboard/admin.html')

@group_required('Student')
def dashboard_student(request):
    return render(request, 'dashboard/student.html')

@group_required('Teacher')
def dashboard_teacher(request):
    return render(request, 'dashboard/teacher.html')