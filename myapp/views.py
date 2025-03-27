from django.shortcuts import render,redirect,HttpResponse
import smtplib
from .models import DiagCenter, Hospital, PatientDetails,Pres,pdfs,Patient,ppdfs
from django.contrib import messages
from django.template import loader
from geopy.geocoders import Nominatim
import folium
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import logout
import math, random
from twilio.rest import Client
from datetime import date
import math, random
import pandas as pd
from collections import Counter
import json
import requests
from requests.structures import CaseInsensitiveDict
import urllib.parse
# function to generate OTP
def generateOTP() :
    digits = "0123456789"
    OTP = ""
    for i in range(4) :
        OTP += digits[math.floor(random.random() * 10)]
    return OTP



account_sid = 'AC104950427701f529ac826544713d6843'
auth_token = '35651393a6b7a4007a87b3a8db808cec'
def fetchPatient(request):
    if request.method == 'POST':
        adno = request.POST['aadhaar']
        hname = request.POST['hname']
        hid = request.POST['hid']
        try:
            pobj = Patient.objects.get(adhno = adno)
            print(pobj)
        except:
            return redirect(hospitalLogin)
        pmobno = str(pobj.phno)
        pmail = str(pobj.emial)
        client = Client(account_sid, auth_token)
        otp = generateOTP()
        pobj.otp = otp
        pobj.save()
        pname = pobj.pname
        try:
            message = client.messages.create(
            from_='+12622268250',
            to='+91'+pmobno,body="Hello dear "+pobj.pname+", Your OTP for HealthWallet is"+otp
            )
        except:
            pass
        
        msg = "Subject: Your OTP for HealthWallet\n\nHello dear " + pname + ", Your OTP for HealthWallet is: " + str(otp)
        try:
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login("sushmadilakshmikurella@gmail.com", "hsbulcezfkfrhcdz")
            s.sendmail("sushmadilakshmikurella@gmail.com", pmail, msg)
            s.quit()
            print(pmail, msg)
            messages.info(request, "Email successfully sent")
        except Exception as e:
            print("An error occurred:", e)
            messages.error(request, "Failed to send email")
        return render(request, "otpauth.html",{'adno':adno, 'hname':hname, 'hid':hid})

def fetchPatientD(request):
    if request.method == 'POST':
        adno = request.POST['aadhaar']
        dname = request.POST['dname']
        did = request.POST['did']
        print(dname,'1111')
        try:
            pobj = Patient.objects.get(adhno = adno)
            print(pobj)
        except:
            return redirect(diaglogin)
        pmobno = str(pobj.phno)
        pmail = pobj.emial
        client = Client(account_sid, auth_token)
        otp = generateOTP()
        pobj.otp = otp
        pobj.save()
        pname = pobj.pname
        try:
            message = client.messages.create(
            from_='+12622268250',
            to='+91'+pmobno,body="Hello dear "+pobj.pname+", Your OTP for HealthWallet is"+otp
            )
        except:
            pass
        msg = "Subject: Your OTP for HealthWallet\n\nHello dear " + pname + ", Your OTP for HealthWallet is: " + str(otp)
        try:
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login("sushmadilakshmikurella@gmail.com", "hsbulcezfkfrhcdz")
            s.sendmail("sushmadilakshmikurella@gmail.com", pmail, msg)
            s.quit()
            print(pmail, msg)
            messages.info(request, "Email successfully sent")
        except Exception as e:
            print("An error occurred:", e)
            messages.error(request, "Failed to send email")
        return render(request, "otpauthD.html",{'adno':adno,'dname':dname, 'did':did})

def otpauth(request):
    if request.method == 'POST':
        adno = request.POST['adno']
        otp = request.POST['otp']
        hname = request.POST['hname']
        hid = request.POST['hid']

        try:
            pobj = Patient.objects.get(adhno = adno)
            print(pobj)
        except:
            return redirect(hospitalLogin)
        correct_otp = str(pobj.otp)
        pname = pobj.pname 
        print(correct_otp, otp)
        if(otp == correct_otp):
            pobj.otp = ''
            pobj.save()
            return render(request, "vieworadd.html", {'pname':pname, 'hname':hname, 'hid':hid, 'adno':adno})
        else:
            return redirect(hospitalLogin)


def otpauthD(request):
    if request.method == 'POST':
        adno = request.POST['adno']
        otp = request.POST['otp']
        dname = request.POST['dname']
        did = request.POST['did']
        print(dname,'3333')
        try:
            pobj = Patient.objects.get(adhno = adno)
            print(pobj)
        except:
            return redirect(diaglogin)
        correct_otp = str(pobj.otp) 
        pname = pobj.pname
        print(correct_otp, otp)
        if(otp == correct_otp):
            pobj.otp = ''
            pobj.save()
            return render(request, "uploadDetailsDiag.html", {'pname':pname, 'dname':dname, 'did':did,'adhno':adno})
        else:
            return redirect(diaglogin)


# Create your views here.
hid=""
pid=""
def hospitalLogin(request):
    if request.method == 'POST':
        hid = request.POST['hid']
        hpswd = request.POST['hpswd']
        hobj = Hospital.objects.get(hid = hid)
        if(hobj.pswd == hpswd):
            return render(request, 'hospitalhome.html',{'hname': hobj.hname, 'hid': hid})
    return render(request,'hospitalLogin.html')
def diaglogin(request):
    if request.method=='POST':
        did = request.POST['did']
        dpswd = request.POST['dpswd']
        dobj = DiagCenter.objects.get(dcid=did)
        if(dobj.pswd==dpswd):
            return render(request,'diaghome.html',{'dname':dobj.dcname, 'did':did})
    return render(request,'diaglogin.html')
def home(request):
    return render(request,"home.html")
def savepswd(request):
    if request.method == 'POST':
        pswd = request.POST["pswd"]
        cpswd = request.POST["cpswd"]
        hid1 = request.POST["hid"]

        if pswd == cpswd:
            try:
                obj = Hospital.objects.get(hid=hid1)
                obj.pswd = pswd
                obj.save()
                return redirect('home')
            except Hospital.DoesNotExist:
                return render(request, 'setHpswd.html', {"hid": hid1, "error": "User not found"})
        else:
            return render(request, 'setHpswd.html', {"hid": hid1, "error": "Passwords do not match"})

    return render(request, 'setHpswd.html')

def savePswdDiag(request):
    if request.method == 'POST':
        pswd = request.POST["pswd"]
        cpswd = request.POST["cpswd"]
        hid1 = request.POST["did"]

        if pswd == cpswd:
            try:
                obj = DiagCenter.objects.get(hid=hid1)
                obj.pswd = pswd
                obj.save()
                return redirect('home')
            except DiagCenter.DoesNotExist:
                return render(request, 'setDpswd.html', {"did": hid1, "error": "User not found"})
        else:
            return render(request, 'setDpswd.html', {"did": hid1, "error": "Passwords do not match"})

    return render(request, 'setDpswd.html')

def setHpswd(request):
    print("out")
    if request.method=='POST':
        pswd=request.POST["pswd"]
        cpswd=request.POST["cpswd"]
        hid1=request.POST["hid"]
        print("hiii")
        if(pswd==cpswd):
            obj=Hospital.objects.get(hid=hid1)
            obj.pswd=pswd
            obj.save()
            return redirect('home')
    hid1=hid
    return render(request,'setHpswd.html',{"hid":hid1})
       
def setDpswd(request):
    if request.method=='POST':
        pswd=request.POST["pswd"]
        cpswd=request.POST["cpswd"]
        did1=request.POST["did"]
        print("hiii")
        if(pswd==cpswd):
            obj=DiagCenter.objects.get(dcid=did1)
            obj.pswd=pswd
            obj.save()
            return redirect('home')
        return render(request,'setDpswd.html',{"did":did1})
    return render(request,'setDpswd.html')
import re
def addHospital(request):
    if request.method=="POST":
       hid=request.POST["hid"]
       hnumber=request.POST['hnumber']
       mail=request.POST["hmail"]
       pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@gmail\.com$')
       hname=request.POST["hname"]
       pincode=request.POST["pincode"]
       state=request.POST["state"]
       dist=request.POST["dist"]
       Address=request.POST["Address"]
       speciality=request.POST["speciality"]
       #return pattern.match(email) is not None
    #    if(pattern.match(mail) is None):
    #        messages.error(request,"not a valid mail")
    #        return redirect(addHospital)
       if(Hospital.objects.filter(hid=hid).exists()):
           messages.error(request,"hospital id already exists")
           return redirect(addHospital)
       if(Hospital.objects.filter(hnumber=hnumber).exists()):
           messages.error(request,"phone number already exists")
           return redirect(addHospital)
       if(Hospital.objects.filter(hmail=mail).exists()):
           messages.error(request,"email already exists")
           return redirect(addHospital)

       obj=Hospital.objects.create(hid=hid,hmail=mail,hname=hname,pincode=pincode,state=state,dist=dist,Address=Address,speciality=speciality,hnumber=hnumber)
       obj.save()
       name="Krishna"
       '''subject="it's me, Krishna"
        msg="hello, HOw are you? I hope you all fine."
        rl=['suahmakurella@gmail.com']
        send_mail(subject,msg,EMAIL_HOST_USER,rl,fail_silently=False)'''
       s = smtplib.SMTP('smtp.gmail.com', 587)
       s.starttls()

# Authentication
       #s.login("suahmakurella@gmail.com", "zbxnecargpjugmpn")
       #s.login("suahmakurella@gmail.com", "gxgiipbvtpzveujj")
       s.login("sushmadilakshmikurella@gmail.com","hsbulcezfkfrhcdz")
    #    s.login

# message to be sent
       m="http://192.168.24.248:8000/setHpswd/"+hid
       msg="""
       hello,
       password reset link is provided below it will expired with in 10minitues
       """
       """msg = MIMEText(u'<a href="www.google.com">abc</a>')
       msg['Subject'] = 'subject'
       msg['From'] = 'xxx'
       msg['To'] = 'xxx'"""

       """s = smtplib.SMTP(xxx, 25)
       s.setpassword(xxx, xxx, msg.as_string())
       message = "hello this is Krishna. and this is an automated gmail message."
       """
        # sending the mail
       s.sendmail("sushmadilakshmikurella@gmail.com",mail, msg+m)
        # terminating the session
       s.quit()
       messages.info(request,"email succesfully sent")
       return redirect("adminhome")
    #return render(request,'sendmail.html')
    return render(request,"addHospital.html")

def addDiag(request):
    if request.method=="POST":
       did=request.POST["did"]
       dnumber=request.POST['dnumber']
       mail=request.POST["dmail"]
       dname=request.POST["dname"]
       pincode=request.POST["pincode"]
       state=request.POST["state"]
       dist=request.POST["dist"]
       Address=request.POST["Address"]
       pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@gmail\.com$')
    #    if(pattern.match(mail) is None):
    #        messages.error(request,"not a valid mail")
    #        return redirect(addDiag)
       if(DiagCenter.objects.filter(dcid=did).exists()):
           messages.error(request,"center id already exists")
           return redirect(addDiag)
       if(DiagCenter.objects.filter(dnumber=dnumber).exists()):
           messages.error(request,"phone number already exists")
           return redirect(addDiag)
       if(DiagCenter.objects.filter(dmail=mail).exists()):
           messages.error(request,"email already exists")
           return redirect(addDiag)
       obj=DiagCenter.objects.create(dcid=did,dnumber=dnumber,dcname = dname, pincode = pincode, state = state, dist = dist, Address = Address, dmail = mail)
       obj.save()
       name="Krishna"
       '''subject="it's me, Krishna"
        msg="hello, HOw are you? I hope you all fine."
        rl=['suahmakurella@gmail.com']
        send_mail(subject,msg,EMAIL_HOST_USER,rl,fail_silently=False)'''
       s = smtplib.SMTP('smtp.gmail.com', 587)
       s.starttls()

# Authentication
       #s.login("suahmakurella@gmail.com", "zbxnecargpjugmpn")
       #s.login("suahmakurella@gmail.com", "gxgiipbvtpzveujj")
       s.login("sushmadilakshmikurella@gmail.com","hsbulcezfkfrhcdz")
    #    s.login

# message to be sent
       m="http://192.168.24.248:8000/setDpswd/"+did
       msg="""
       hello,
       password reset link is provided below it will expired with in 10minitues
       """
       """msg = MIMEText(u'<a href="www.google.com">abc</a>')
       msg['Subject'] = 'subject'
       msg['From'] = 'xxx'
       msg['To'] = 'xxx'"""

       """s = smtplib.SMTP(xxx, 25)
       s.setpassword(xxx, xxx, msg.as_string())
       message = "hello this is sushma. and this is an automated gmail message."
       """
        # sending the mail
       s.sendmail("sushmadilakshmikurella@gmail.com",mail, msg+m)
        # terminating the session
       s.quit()
       messages.info(request,"email succesfully sent")
       return render(request,"home.html")
    #return render(request,'sendmail.html')       
    return render(request, "addDiag.html")

       
def coord(address):
    url = "https://api.geoapify.com/v1/geocode/search?text="+str(address)+"&apiKey=a1b07ce765f14402b307e1edb02f6920"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        if 'features' in data and data['features']:
            result = data['features'][0]
            latitude = result['properties']['lat']
            longitude = result['properties']['lon']
            return latitude,longitude
    return None
def map(request):
    if request.method == 'POST':
        geolocator = Nominatim(user_agent="my_user_agent")
        # Enter the pin code
        pincode = request.POST['pin']  # Example pin code for Buckingham Palace
        alob = Hospital.objects.filter(pincode=pincode).values()
        dlob = DiagCenter.objects.filter(pincode=pincode).values()
        # loc = geolocator.geocode(pincode)
        mymap=folium.Map(location=[20.5937, 78.9629], zoom_start=7)
        try:
            district = alob[0]['dist']
            disobj = Hospital.objects.filter(dist=district).values()
            # print("d1",disobj)
            for i in disobj:
                try:
                    latt,logg = coord(urllib.parse.quote(i['Address']))
                    if(latt is None or logg is None):
                        continue
                except:
                    continue
                folium.Marker([latt,logg],popup="myloc",tooltip=i['hname']).add_to(mymap)
        except Exception:
            pass
        try:
            district1 = dlob[0]['dist']        
            disobj1 = DiagCenter.objects.filter(dist=district1).values()
            # print(disobj1)
            for i in disobj1:
                try:
                    latt,logg = coord(urllib.parse.quote(i['Address']))
                    if(latt is None or logg is None):
                        continue
                except:
                    continue
                folium.Marker([latt,logg],popup="myloc",tooltip=i['dcname']).add_to(mymap)
        except:
            pass
        folium_map_html = mymap._repr_html_()  
        return render(request,"map.html",{"folium_map_html": folium_map_html})
    return render(request, "enterpin.html")


def patientRegister(request):
    if request.method == 'POST':
        adhno = request.POST['adhno']
        pswd = request.POST['pswd']
        cpswd=request.POST['cpswd']
        pname = request.POST['pname']
        pincode = request.POST['pincode']
        state = request.POST['state']
        dist = request.POST['dist'].lower()
        Address = request.POST['Address']
        gender = request.POST['gender']
        dob = request.POST['dob']
        diab = request.POST['diab']
        bp = request.POST['bp']
        weight = request.POST['weight']
        height = request.POST['height']
        phno = request.POST['phno']
        email = request.POST['email']
        pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@gmail\.com$')
        # if(pattern.match(email) is None):
        #    messages.error(request,"not a valid mail")
        #    return redirect(patientRegister)
        if(pswd!=cpswd):
           render(request,"patientRegister.html",{"msg":"password mismatch"})
        else:
            if(Patient.objects.filter(adhno=adhno).exists()):
                messages.error(request,"Aadhar already exists")
                return redirect(patientRegister)
            if(Patient.objects.filter(phno=phno).exists()):
                messages.error(request,"phone number already exists")
                return redirect(patientRegister)
            if(Patient.objects.filter(emial=email).exists()):
                messages.error(request,"email already exists")
                return redirect(patientRegister)
            obj = Patient.objects.create(
            adhno=adhno,
            pswd=pswd,
            pname=pname,
            pincode=pincode,
            state=state,
            dist=dist,
            Address=Address,
            gender=gender,
            dob=dob,
            diab=diab,
            bp=bp,
            weight=weight,
            height=height,
            phno=phno,
            emial=email
        )
        obj.save();
        name="Krishna"
       
        s = smtplib.SMTP('smtp.gmail.com', 587)

# start TLS for security
        s.starttls()
        s.login("sushmadilakshmikurella@gmail.com","hsbulcezfkfrhcdz")

# message to be sent
        m="http://192.168.24.248:8000/setHpswd/"+hid
        msg="""Congratulations"""
        msg2="""you have registered succeesfully in Health Wallet website
            now your data is safe and secure.
        """

# sending the mail
        s.sendmail("sushmadilakshmikurella@gmail.com",email, msg+pname+msg2)

# terminating the session
        s.quit()
        return redirect('home')
    return render(request,"patientRegister.html")
def uploadDetails(request):
    return render(request,"uploadDetails.html")
from datetime import date
def storeDetails(request):
    if request.method=="POST":
        current_date = date.today()
        print(current_date)

        formatted_date = current_date.strftime("%d-%m-%Y")
        print(formatted_date,'hereeeeeeee')
        date1 = formatted_date
        disease = request.POST["disease"]
        diagnosis = request.POST["diagnosis"]
        #prescription = request.POST["prescription"]
        remarks = request.POST["remarks"]
        adhno = request.POST["adhno"]
        hid = request.POST["hid"]
        hname = request.POST["hname"]
        dname = request.POST["doname"]
        dm1=int(request.POST["dm1"])
        dm2=int(request.POST["dm2"])
        obj=PatientDetails.objects.create(
            date=date1,
            disease=disease,
            diagnosis=diagnosis,
            #prescription=prescription,
            remarks=remarks,
            adhno=adhno,
            hid=hid,
            hname=hname,
            dname=dname
        )
        obj.save();
        for i in range(1,dm1+1):
            m=request.POST["m"+str(i)]
            t=request.POST["t"+str(i)]
            e=request.POST["e"+str(i)]
            obj1=Pres.objects.create(
                date=formatted_date,
                hid=hid,
                hname=hname,
                medicine=m,
                time=t,
                adhno=adhno,
                lunch=e,
                mid=obj.id
                )
            obj1.save();
        for i in range(1,dm2+1):
            pdf=request.FILES["pdf"+str(i)]
            pdfname=request.POST["pdfname"+str(i)]
            obj2=pdfs.objects.create(
                date=formatted_date,
                hid=hid,
                hname=hname,
                pdf=pdf,
                pdfname=pdfname,
                adhno=adhno,
                mid=obj.id
                )
            obj2.save();
    return redirect("home")
import numpy as np 
import pandas as pd
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import hstack
from sklearn.feature_extraction.text import TfidfVectorizer
def recommend_medicines_by_usage(medicine_name, tfidf_matrix_uses, clean_df):
    # Get the index of the medicine
    medicine_index = clean_df[clean_df['Medicine Name'] == medicine_name].index[0]
    
    # Calculate cosine similarity between the given medicine and others based on usage
    sim_scores = cosine_similarity(tfidf_matrix_uses, tfidf_matrix_uses[medicine_index])
    
    # Get indices of top similar medicines (excluding the queried one)
    sim_scores = sim_scores.flatten()
    similar_indices = sim_scores.argsort()[::-1][1:6]  # Top 5 similar medicines
    
    # Get recommended medicine names
    recommended_medicines = clean_df.iloc[similar_indices]['Medicine Name'].tolist()
    
    return recommended_medicines
def recommend_medicines_by_symptoms(symptoms, tfidf_vectorizer, tfidf_matrix_uses, clean_df):
    # Create a string from the given symptoms
    symptom_str = ' '.join(symptoms)
    
    # Transform the symptom string using the TF-IDF vectorizer
    symptom_vector = tfidf_vectorizer.transform([symptom_str])
    
    # Calculate cosine similarity between the symptom vector and all medicine vectors
    sim_scores = cosine_similarity(tfidf_matrix_uses, symptom_vector)
    
    # Get indices of top similar medicines
    sim_scores = sim_scores.flatten()
    similar_indices = sim_scores.argsort()[::-1][:5]  # Top 5 similar medicines
    
    # Get recommended medicine names
    recommended_medicines = clean_df.iloc[similar_indices]['Medicine Name'].tolist()
    
    return recommended_medicines
def recommendMedicine(request):
    if request.method=='POST':
        # for dirname, _, filenames in os.walk(r"/Users/jvmohanakrishnainty/Desktop/Med_Recommend/Medical2/Medicine_Details.csv"):
        #     for filename in filenames:
        #         print(os.path.join(dirname, filename))
        df = pd.read_csv(r'C:/Users/Dell/OneDrive/Desktop/djpro/medicalProject/Medicine_Details.csv')
        #df.head()
        clean_df = df.drop_duplicates()
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix_uses = tfidf_vectorizer.fit_transform(clean_df['Uses'].astype(str))
        tfidf_matrix_composition = tfidf_vectorizer.fit_transform(clean_df['Composition'].astype(str))
        tfidf_matrix_side_effects = tfidf_vectorizer.fit_transform(clean_df['Side_effects'].astype(str))
        min_rows = min(tfidf_matrix_uses.shape[0], tfidf_matrix_composition.shape[0], tfidf_matrix_side_effects.shape[0])

    # Trim matrices to have the same number of rows
        tfidf_matrix_uses = tfidf_matrix_uses[:min_rows]
        tfidf_matrix_composition = tfidf_matrix_composition[:min_rows]
        tfidf_matrix_side_effects = tfidf_matrix_side_effects[:min_rows]

        tfidf_matrix_combined = hstack((tfidf_matrix_uses, tfidf_matrix_composition, tfidf_matrix_side_effects))

        cosine_sim_combined = cosine_similarity(tfidf_matrix_combined, tfidf_matrix_combined)

        # query = "Lobet 20mg Injection"
        # recommended_medicines = recommend_medicines_by_usage(query, tfidf_matrix_uses, clean_df)
        # print(recommended_medicines)

    

        # Create a TF-IDF vectorizer for symptoms
        tfidf = TfidfVectorizer(stop_words='english')

        # Fit and transform the 'Uses' column to create the TF-IDF matrix for symptoms
        tfidf_matrix_uses = tfidf.fit_transform(clean_df['Uses'])

    # Now, you can call the recommend_medicines_by_symptoms function
        query = request.POST["ds"] # Convert the single symptom to a list
        print(query)
        recommended_medicines = recommend_medicines_by_symptoms(query, tfidf, tfidf_matrix_uses, clean_df)
        print(recommended_medicines)
        #****************************************model one completed**********************************
        return render(request,"displayMedicine.html",{"data":recommended_medicines})
    return render(request,"recommendMedicine.html")

def adminhome(request):
    return render(request,"adminhome.html")
def adminlogin(request):
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['pswd']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page or any other page
            return redirect('adminhome')
        else:
            # Authentication failed, display an error message
            error_message = "Invalid username or password. Please try again."
            return render(request, 'adminlogin.html', {'error_message': error_message})
    else:
        return render(request, 'adminlogin.html')

def patientLogin(request):
    if request.method == 'POST':
        pid = request.POST['pid']
        ppswd = request.POST['ppswd']
        pobj = Patient.objects.get(adhno = pid)
        if(pobj.pswd == ppswd):
            obj=PatientDetails.objects.filter(adhno=pid)
            lst=[]
            l=[i for i in range(0,len(obj))]
            for i in obj:
                l1=[]
                l1.append(i)
                pres=Pres.objects.filter(adhno=pid,date=i.date,hid=i.hid)
                pd=pdfs.objects.filter(adhno=pid,date=i.date,hid=i.hid)
                l1.append(pres)
                l1.append(pd)
                lst.append(l1)
                print(pres)
            print(lst)
            return render(request,"patientHome1.html",{"lst":lst,"adno":pid})
    return render(request,'patientlogin.html')
from django.http import HttpResponseRedirect
def adminlogout(request):
    # logout(request)
    if request.method=='POST':
        return redirect('home')
    return redirect('adminhome')


def patientloginregister(request):
    return render(request, "patientlr.html")

def viewpast(request):
    adno = request.POST['adno']
    obj=PatientDetails.objects.filter(adhno=adno)
    lst=[]
    l=[i for i in range(0,len(obj))]
    for i in obj:
        l1=[]
        l1.append(i)
        pres=Pres.objects.filter(adhno=adno,date=i.date,mid=i.id)
        pd=pdfs.objects.filter(adhno=adno,date=i.date,mid=i.id)
        l1.append(pres)
        l1.append(pd)
        lst.append(l1)
        print(pres)

    return render(request,"displayDetails.html",{"lst":lst,"adno":adno})

def uploadnew(request):
    if request.method == 'POST':
        hid = request.POST['hid']
        hname = request.POST['hname']
        pname = request.POST['pname']
        adno=request.POST['adno']
        return render(request, "uploadDetailsHosp.html", {'pname':pname, 'hname':hname, 'hid':hid,'adno':adno})
def uploadnewD(request):
    if request.method == 'POST':
        did = request.POST['did']
        dname = request.POST['dname']
        pname = request.POST['pname']
        adno=request.POST['adno']
        return render(request, "uploadDetailsDiag.html", {'pname':pname, 'dname':dname, 'did':did,'adno':adno})
def showStats(request):
    allob = PatientDetails.objects.all().values()
    allpat = Patient.objects.all().values()
    df = pd.DataFrame(allob)
    df1 = pd.DataFrame(allpat)
    diseases = df['disease'].unique() #unique diseases
    # print(diseases)
    state = "Andhra Pradesh"
    if(request.method=="POST"):
        state = request.POST['state']
        print(state,"sss")
    # state = request['state']
    dfs = df1[df1['state']==state]
    districts = list(dfs['dist'].unique()) # unique districts
    print(districts)
    lisdis = []
    lisdis1 = []
    col = ["AliceBlue","AntiqueWhite","Aqua","Aquamarine","Azure","Beige","Bisque","Black","BlanchedAlmond","Blue","BlueViolet","Brown","BurlyWood","CadetBlue","Chartreuse","Chocolate","Coral","CornflowerBlue","Cornsilk","Crimson","Cyan","DarkBlue","DarkCyan","DarkGoldenRod","DarkGray","DarkGrey","DarkGreen","DarkKhaki","DarkMagenta","DarkOliveGreen","DarkOrange","DarkOrchid","DarkRed","DarkSalmon","DarkSeaGreen","DarkSlateBlue","DarkSlateGray","DarkSlateGrey","DarkTurquoise","DarkViolet","DeepPink","DeepSkyBlue","DimGray","DimGrey","DodgerBlue","FireBrick","FloralWhite","ForestGreen","Fuchsia","Gainsboro","GhostWhite","Gold","GoldenRod","Gray","Grey","Green","GreenYellow","HoneyDew","HotPink","IndianRed","Indigo","Ivory","Khaki","Lavender","LavenderBlush","LawnGreen","LemonChiffon","LightBlue","LightCoral","LightCyan","LightGoldenRodYellow","LightGray","LightGrey","LightGreen","LightPink","LightSalmon","LightSeaGreen","LightSkyBlue","LightSlateGray","LightSlateGrey","LightSteelBlue","LightYellow","Lime","LimeGreen","Linen","Magenta","Maroon","MediumAquaMarine","MediumBlue","MediumOrchid","MediumPurple","MediumSeaGreen","MediumSlateBlue","MediumSpringGreen","MediumTurquoise","MediumVioletRed","MidnightBlue","MintCream","MistyRose","Moccasin","NavajoWhite","Navy","OldLace","Olive","OliveDrab","Orange","OrangeRed","Orchid","PaleGoldenRod","PaleGreen","PaleTurquoise","PaleVioletRed","PapayaWhip","PeachPuff","Peru","Pink","Plum","PowderBlue","Purple","RebeccaPurple","Red","RosyBrown","RoyalBlue","SaddleBrown","Salmon","SandyBrown","SeaGreen","SeaShell","Sienna","Silver","SkyBlue","SlateBlue","SlateGray","SlateGrey","Snow","SpringGreen","SteelBlue","Tan","Teal","Thistle","Tomato","Turquoise","Violet","Wheat","White","WhiteSmoke","Yellow","YellowGreen"]
    for i in districts:
        # print(i)
        adnos = df1[(df1['state']==state) & (df1['dist']==i)]
        adnos = list(adnos['adhno'])
        # print(adnos)
        filtered_df = df[df['adhno'].isin(adnos)]
        disease_counts = Counter(filtered_df['disease'])
        if not disease_counts:
            continue
        max_count_item = max(disease_counts.items(), key=lambda x: x[1])
        n = [i,max_count_item[1],random.choice(col),max_count_item[0]]
        n1 = [max_count_item[0],max_count_item[1]]
        lisdis1.append(n1)
        lisdis.append(n)
    # print(lisdis)
    json_nested_list = json.dumps(lisdis)
    json_nested_list1 = json.dumps(lisdis1)
    # print(type(districts),districts)
    return render(request,'viewStats.html',{'state':state,'json_nested_list': json_nested_list,'json_nested_list1': json_nested_list1})

def displaypdf(request):
    if request.method=='POST':
        pid=request.POST['pid']
        obj=pdfs.objects.get(id=pid)
        return render(request,"displaypdf.html",{'obj':obj})
    return render(request,"displaypdf.html")
def addpdf(request):
    if(request.method=='POST'):
        adno=request.POST['adno']
        return render(request,"addpdf.html",)
def storepdf(request):
    if request.method=='POST':
        adno=request.POST['adno']
        pdfname=request.POST['pdfname']
        pdf=request.FILES["pdf"]
        obj=ppdfs.objects.create(adhno=adno,pdfname=pdfname,pdf=pdf)
        obj.save();
        return render(request,"patientlogin.html")


