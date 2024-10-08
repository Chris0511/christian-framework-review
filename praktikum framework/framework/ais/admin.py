from django.contrib import admin

# Register your models here.
from django.contrib.auth.hashers import make_password  # For hashing passwords
# Import your models
from .models.teachers import Teachers
from .models.students import Students
from .models.users import Users


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('nip', 'name', 'email', 'phone_number')

    def save_model(self, request, obj, form, change):
        # Simpan Teacher terlebih dahulu
        super().save_model(request, obj, form, change)

        # Cek apakah user dengan email guru sudah ada
        user, created = Users.objects.get_or_create(
            username=obj.nip,
            defaults={
                'password': make_password('default_password'),  # Menggunakan hashing password
                'role': Users.TEACHER,  # Pastikan Anda memiliki field role di model Users
            }
        )
        if not created:
            # Jika user sudah ada, perbarui role (untuk berjaga-jaga)
            user.role = Users.TEACHER
            user.save()


# Daftarkan Teachers dengan custom TeacherAdmin
admin.site.register(Teachers, TeacherAdmin)
admin.site.register(Students)
admin.site.register(Users)
