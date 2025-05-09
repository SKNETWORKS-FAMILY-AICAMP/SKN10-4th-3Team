from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from .token import decode_access_token, decode_refresh_token, create_access_token, create_refresh_token

# jwt access 토큰 검증 함수
def validate_access_token(token):
  try:
    if decode_access_token(token):
      return True
  except AuthenticationFailed:
    return False
  
# jwt refresh 토큰 검증 함수
def validate_refresh_token(token):
  try:
    if decode_refresh_token(token):
      return True
  except AuthenticationFailed:
    return False

# access token 만료 시
def expired_token(request):
  # access token 만료 확인
  access_token = request.COOKIES.get('access_token')
  if validate_access_token(access_token):
    # True일 경우 refresh token 제거
    response = Response()
    response.set_cookie(key='access_token', value='',httponly=True)
    response.set_cookie(key='refresh_token', value='', httponly=True)
    return response
  else:
    return None

# refresh token이 유효할 경우우 새로운 access token 발급 함수
def refresh_access_token(request):
  if request.method == 'POST':
    # refresh token 유효 확인
    refresh_token = request.COOKIES.get('refresh_token')
    if validate_refresh_token(refresh_token):
    # True일 경우 새로운 access token 발급
      access_token = create_access_token(request.user.id)
      response = Response()
      response.set_cookie(key='access_token', value=access_token, httponly=True)
      return response
    else:
      return None

# jwt refresh token이 유효할 때 refresh token 재발급 함수
def make_refresh_token(request):
  # refresh token 유효 확인
  refresh_token = request.COOKIES.get('refresh_token')
  if validate_refresh_token(refresh_token):
    # True일 경우 새로운 refresh token 발급
    refresh_token = create_refresh_token(request.user.id)
    response = Response()
    response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)
    return response
  else:
    return None