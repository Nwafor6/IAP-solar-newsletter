from django.shortcuts import render
from .models import Newsletter
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from .serializers import NewsletterSerializer

# Send mail
from django.core.mail import send_mail, BadHeaderError
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework import status
# end

# Create your views here.
@api_view(['POST'])
@csrf_exempt
def Subscribe(request):

    email=request.data["email"]
    print(email, "test")
    Newsletter.objects.all().delete()
    try:
        Newsletter.objects.create(email=email)
    except:
        return Response({"detail":"Already a subscriber !!"}, status=status.HTTP_403_FORBIDDEN)
    subject="Welcome to SEGNAU newsletter"
    # Render the HTML template using the user's email and name
    html_content = render_to_string('newletter_subscibe.html', {'email': email})

    # Create the EmailMultiAlternatives object
    email_message = EmailMultiAlternatives(subject=subject,
        from_email="nwaforglory6@gmail.com",
        to=[email],
    )
    # Attach the HTML content to the email message
    email_message.attach_alternative(html_content, "text/html")
    # Send the email
    email_message.send()
    return Response({"detail":"Thank you for subscribing."}, status=status.HTTP_200_OK)

class SubscribersList(generics.ListAPIView):
    queryset=Newsletter.objects.all()
    serializer_class=NewsletterSerializer

    def get(self, request, *args, **kwargs):
        serializer=self.serializer_class(self.get_queryset(), many=True)
        return Response({"details":serializer.data},status=status.HTTP_200_OK)


    


