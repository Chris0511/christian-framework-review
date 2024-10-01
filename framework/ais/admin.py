from django.contrib import admin
<<<<<<< HEAD

# Register your models here.
=======
from django.contrib.auth.hashers import make_password  # For hashing passwords
# Import your models
from .models.teachers import Teachers
from .models.students import Students
from .models.users import Users


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('nip', 'name', 'email', 'phone_number')

    def save_model(self, request, obj, form, change):
        # Save Teacher first
        super().save_model(request, obj, form, change)

        # Check if the user with the teacher's email already exists
        user, created = Users.objects.get_or_create(
            username=obj.nip,  # Assuming `nip` is a unique identifier
            defaults={
                'password': make_password('default_password'),  # Hashing the default password
                'role': Users.TEACHER,  # Assuming role field exists
            }
        )
        if not created:
            # If user exists, update the role (for safety)
            user.role = Users.TEACHER
            user.save()


# Register the models at the module level
admin.site.register(Teachers, TeacherAdmin)
admin.site.register(Students)
admin.site.register(Users)
>>>>>>> 2c709c3 (Review 4)
