from django.utils import timezone

def set_cookie(response, key, value, expire_minutes = 20):
	expires = timezone.now() + timezone.timedelta(minutes=expire_minutes)
	response.set_cookie(key, value, expires=expires)

def gen_password(passfraze):
	return passfraze[:8].encode('ascii'), passfraze[:8].encode('ascii')

def validate_permissions(user, username):
	return True if (user.is_authenticated() and user.username == username) else False