from django.contrib import admin
from .models import Patient,Hospital,DiagCenter,PatientDetails,pdfs,image,Pres,ppdfs
# Register your models here.
admin.site.register(Patient)
admin.site.register(Hospital)
admin.site.register(DiagCenter)
admin.site.register(PatientDetails)
admin.site.register(pdfs)
admin.site.register(image)
admin.site.register(Pres)
admin.site.register(ppdfs)
