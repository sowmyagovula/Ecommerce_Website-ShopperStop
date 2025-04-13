from .models import Profile

def user_profile_context(request):
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
            return {'user_type': profile.user_type}
        except Profile.DoesNotExist:
            return {'user_type': None}
    return {'user_type': None}
