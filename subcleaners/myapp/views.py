from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import JsonResponse
from django.utils.html import escape
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
from django.urls import reverse
from django.contrib import messages


from django.shortcuts import redirect, render

def home(request):
    if request.method == 'POST':
        #Form data
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        service = request.POST.get('service')
        frequency = request.POST.get('frequency')
        
        #Email message
        subject = 'New Cleaning Service Request'
        message = f"""
        You have received a new cleaning service request.

        Name: {first_name} {last_name}
        Email: {email}
        Phone: {phone}
        Service: {service}
        Frequency: {frequency}
        """

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_RECEIVER],
            fail_silently=False,
        )

        return redirect('booknow', first_name=first_name, last_name=last_name, email=email, phone=phone)

    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        try:
            inquiry_type = request.POST.get('inquiry_type')
            message = request.POST.get('message')
            email = request.POST.get('email')

            # Send confirmation email to customer
            send_mail(
                subject="Contact Form Submission Confirmation",
                message=f"Thank you for reaching out! We received your message regarding: {inquiry_type}. We will get back to you soon.",
                from_email="markmnashed@gmail.com",  # Marks subcleaners Email
                recipient_list=[email],
                fail_silently=False,
            )

            # Marks subcleaners Email
            owner_email = "markmnashed@gmail.com"  # Marks subcleaners Email
            owner_message = (
                f"New contact form submission:\n\n"
                f"Inquiry Type: {inquiry_type}\n"
                f"Message: {message}\n"
                f"Customer Email: {email}\n"
            )

            send_mail(
                subject="New Contact Form Submission",
                message=owner_message,
                from_email="markmnashed@gmail.com",  # Marks subcleaners Email
                recipient_list=[owner_email],
                fail_silently=False,
            )

            return redirect("home")

        except Exception as e:
            print("Error:", e)
            return JsonResponse({"error": "There was an issue with the submission. Please try again."}, status=500)

    return render(request, 'contact.html')

def help(request):
    return render(request, 'help.html')

def quotes(request):
    if request.method == 'POST':
        try:
            # Get form data
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            street = request.POST.get('street')
            apt = request.POST.get('apt')
            city = request.POST.get('city')
            state = request.POST.get('state')
            zipcode = request.POST.get('zipcode')
            notes = request.POST.get('notes')

            # Send confirmation email to the customer
            send_mail(
                subject="Quote Request Confirmation",
                message=f"Thank you for requesting a quote, {firstname}. We have received your request and will get back to you soon with the details.",
                from_email="cleans@subcleaners.com",  # Your email address
                recipient_list=[email],
                fail_silently=False,
            )

            # Send email to the business owner with the quote request details
            owner_email = "cleans@subcleaners.com"  # Replace with your email address
            owner_message = (
                f"New quote request:\n\n"
                f"Customer Name: {firstname} {lastname}\n"
                f"Email: {email}\n"
                f"Phone: {phone}\n"
                f"Address: {street}, {apt}, {city}, {state}, {zipcode}\n"
                f"Notes: {notes}\n"
            )

            send_mail(
                subject="New Quote Request",
                message=owner_message,
                from_email="cleans@subcleaners.com",  # Replace with your email address
                recipient_list=[owner_email],
                fail_silently=False,
            )

            return redirect("home")
        
        except Exception as e:
            print("Error:", e)
            return JsonResponse({"error": "An error occurred. Please try again."}, status=500)

    return render(request, 'quotes.html')  # Render quotes page if the method is GET

def booknow(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        return render(request, 'booknow.html', {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': phone,
        })

    return render(request, 'booknow.html')

@csrf_exempt  # Temporarily disable CSRF for testing purposes (remove in production)
def submit_booking(request):
    if request.method == "POST":
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)

            # Extract necessary form data
            total_price = data.get("totalPrice")
            
            customer_email = data.get("email")
            customer_firstName = data.get("firstName")
            customer_lastName = data.get("lastName")
            customer_phone = data.get("phone")
            customer_street = data.get("street")
            customer_apt = data.get("apt")
            customer_city = data.get("city")
            customer_state = data.get("state")
            customer_zip = data.get("zipcode")
            
            customer_bedrooms = data.get("bedrooms")
            customer_bathrooms = data.get("bathrooms")
            
            selected_extras = data.get("extras")
            
            cleaning_date = data.get("date")
            cleaning_time = data.get("time")
            
            customer_notes = data.get("notes")
            
            # Confirmation to customer email
            send_mail(
                subject="Booking Confirmation",
                message=f"Thank you for your booking with SubCleaners! Total price: ${total_price}",
                from_email="cleans@subcleaners.com",  
                recipient_list=[customer_email],  
                fail_silently=False,  
            )
            selected_extras = data.get("selectedExtras", [])
            formatted_extras = ", ".join(selected_extras)  

            # Prep email content
            owner_email = "cleans@subcleaners.com"  
            company_message = (
                f"New booking submitted:\n\n"
                f"Customer Name: {customer_firstName} {customer_lastName}\n"
                f"Customer Email: {customer_email}\n"
                f"Customer Phone: {customer_phone}\n"
                f"Customer Street: {customer_street}\n"
                f"customer_apt: {customer_apt}\n"
                f"customer_city: {customer_city}\n"
                f"customer_state: {customer_state}\n"
                f"customer_zip: {customer_zip}\n"
                f"customer_bedrooms: {customer_bedrooms}\n"
                f"customer_bathrooms: {customer_bathrooms}\n"
                f"selected_extras: {formatted_extras}\n"
                f"cleaning_date: {cleaning_date}\n"
                f"cleaning_time: {cleaning_time}\n"
                f"customer_notes: {customer_notes}\n"
                f"Total Price: ${total_price}\n"
            )

            # Send email to Marks subcleaners email
            send_mail(
                subject=f"New Booking Notification{customer_firstName}{customer_lastName}",
                message=company_message,
                from_email="cleans@subcleaners.com",  
                recipient_list=[owner_email],
                fail_silently=False,
            )

            return redirect("home")

        except Exception as e:
            print("Error:", e)
            return JsonResponse({"error": "An error occurred"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)