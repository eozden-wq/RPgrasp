from rest_framework.views import APIView
from rest_framework import permissions
from user_profiles.models import UserPorfile
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect 
from django.utils.decorators import method_decorator

@method_decorator(csrf_protect, name='dispatch')
class SignupView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        data = self.request.data
        username = data['username']
        password = data['password']
        re_password = data['re_password']

        if password == re_password:
            if User.objects.filter(username=username).exists():
                return Response({'error': 'Username already exists'})
            elif len(password) <  8:
                return Response({'error': 'password must at least be 8 characters'})
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                
                user = User.objects.get(username=username)

                user_profile = UserProfile(user, first_name='', last_name='')
                user_profile.save()

                return Response({'success': 'user created successfully'})
        
        else:
            return Response({'error': 'Passwords don\'t match'})


@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        return Response({'success': 'CSRF cookie set'})