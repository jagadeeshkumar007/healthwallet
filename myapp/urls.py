from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns=[
    path('',views.home,name='home'),
    path('addHospital',views.addHospital,name='addHospital'),
    path('addDiag',views.addDiag, name = 'addDiag'),
    path('setHpswd',views.setHpswd,name='setHpswd'),
    path('setHpswd/setHpswd/<str:hid>',views.setHpswd,name='setHpswd'),
    path('setDpswd',views.setDpswd,name='setDpswd'),
    path('setDpswd/setDpswd/<str:did>',views.setDpswd,name='setDpswd'),
    path('patientlogin', views.patientLogin, name = 'patientlogin'),
    path('patientloginregister', views.patientloginregister, name = 'patientloginregister'),
    path('savepswd',views.savepswd,name='savepswd'),
    path('savePswdDiag',views.savePswdDiag,name='savePswdDiag'),
    path('hospitallogin',views.hospitalLogin,name='hospitallogin'),
    path('diaglogin', views.diaglogin, name='diaglogin'),
    path('patientRegister',views.patientRegister,name='patientRegister'),
    path('uploadDetails',views.uploadDetails,name='uploadDetails'),    
    path('storeDetails',views.storeDetails,name='storeDetails'),    
    path('recommendMedicine',views.recommendMedicine,name='recommendMedicine'),    
    path('adminlogin',views.adminlogin,name='adminlogin'),    
    path('adminhome',views.adminhome,name='adminhome'),    
    path('adminlogout',views.adminlogout,name='adminlogout'),    
    path('adminhome',views.adminhome,name='adminhome'),
    path('fetchPatient', views.fetchPatient, name = 'fetchPatient'),
    path('fetchPatientD', views.fetchPatientD, name = 'fetchPatientD'),
    path('otpauth', views.otpauth, name = 'otpauth'),
    path('otpauthD', views.otpauthD, name = 'otpauthD'),
    # path('enteraadhaar', views.enteraadhaar, name = 'enteraadhaar'),
    path('viewpast', views.viewpast, name='viewpast'),
    path('uploadnew', views.uploadnew, name='uploadnew'),
    path('uploadnewD', views.uploadnewD, name='uploadnewD'),
    path('viewStats', views.showStats, name='viewStats'),
    path('displaypdf', views.displaypdf, name='displaypdf'),
    path('addpdf', views.addpdf, name='addpdf'),
    path('storepdf', views.storepdf, name='storepdf'),
    path('patientHome', views.storepdf, name='storepdf'),
    path('map', views.map, name='map'),
    path('nearby', views.map, name='nearby'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)