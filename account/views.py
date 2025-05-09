from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        # 로그인 처리 로직
        return render(request, 'chatbot/chatbot.html')
    return render(request, 'account/login.html')    

def register_view(request):
    if request.method == 'POST':
        # 회원가입 처리 로직
        return redirect('account:login')  # 로그인 페이지로 리다이렉트
    return render(request, 'account/register.html')
