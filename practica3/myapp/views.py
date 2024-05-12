# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from .forms import SignUpForm, LogInForm
from django.http import HttpResponseRedirect

def home(request):
    return render(request, 'home.html')

def signup(request):
    if(request.method == 'POST'):
        form = SignUpForm(request.POST)
        if(form.is_valid()):
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login(request):
    if(request.method == 'POST'):
        form = LogInForm(request.POST)
        if(form.is_valid()):
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(username=username, password=password)
                request.session['user_id'] = user.id
                return redirect('userinfo')
            except User.DoesNotExist:
                messages.error(request, 'Invalid username or password')
    else:
        form = LogInForm()
    return render(request, 'login.html', {'form': form})
    
def userinfo(request):
    user_id = request.session.get('user_id')
    if(user_id):
        user = User.objects.get(id=user_id)
        if(request.method == 'POST' and request.FILES.get('myfile')):
            myfile = request.FILES['myfile']
            if(myfile.name.endswith('.p2')):
                file_content = myfile.read().decode('utf-8')
                processed_content = process_file_content(file_content)
                return render(request, 'userinfo.html', {'user': user, 'file_content': processed_content})
            else:
                messages.error(request, 'Invalid file format. Please upload a .p2 file.')
        return render(request, 'userinfo.html', {'user': user})
    else:
        return redirect('login')

delta = {       1:{'+':11,   'dd':12,   '-':11},
                2:{'/':5},
                3:{'.':24,  'dd':21, 'i':10, '-':6},
                4:{'dd':4,'i':10},
                5:{'dd':7},
                6:{'dd':8},
                7:{'dd':9},
                8:{'dd':27},
                9:{'dd':8},
                10:{},
                11:{'dd':13},
                12:{'.':14, 'E':15, '+':16, '-':16, 'dd':17},
                13:{'.':14, 'E':15, '+':16, '-':16, 'dd':13},
                14:{'dd':18},
                15:{'+':19, '-':19, 'dd':20},
                16:{'dd':21},
                17:{'.':14, '/':22, 'E':15, '+':16, 'dd':13, '-':23},
                18:{'E':15, '+':16, '-':16, 'dd':18},
                19:{'dd':20},
                20:{'dd':20},
                21:{'.':24, 'dd':21, 'i':10},
                22:{'dd':25},
                23:{'dd':26},
                24:{'dd':4},
                25:{'dd':2},
                26:{'.':24, 'dd':3, 'i':10},
                27:{}}

F1 = {9,10,12,13,17,18,20,27}

q_0 = 1

def convertidor(caracter):
    strAux = ""
    if(caracter.isdigit()):
        strAux = 'dd'
    else:
        strAux = caracter
    return strAux

def analizador(cadena):
    q_k = q_0
    lexema=""
    for c in cadena:
        transiciones_posibles = delta[q_k]
        try:
            q_k = transiciones_posibles[convertidor(c)]
            lexema = lexema + c
        except KeyError:
            #reset
            q_k = 1
            lexema = ""
            return -1

    if(q_k in F1):
        if(q_k==12 or q_k==13 or q_k==17):
            #integer
            return 1
        elif(q_k==18):
            #float
            return 2
        elif(q_k==20):
            #Scientific notation
            return 3
        elif(q_k==10):
            #complex number
            return 4
        elif(q_k==9 or q_k==27):
            #date
            return 5
        else:
            return -1

def process_file_content(file_content):
    # Split the file content into words
    words = file_content.split()
    processed_content = []
    F2 = {'teorema','matematico','matematica','hilbert','turing','analisis','euler','fermat','pitagoras','automata','boole','cantor','perelman',
      'experimentacion','fisico','fisica','astronomia','mecanica','newton','einstein','galileo','modelo','tesla','dinamica','particulas'}
    
    # Iterate through each word
    for word in words:
         
        if(word.lower() in F2):
            #high ligh the special words
            word = f'<span class="word_of_interest">{word}</span>'

        elif(analizador(word)==1):
            # Wrap integers in a span with class "integer" and style it with blue color
            word = f'<span class="integer">{word}</span>'
        
        elif(analizador(word)==2):

            word = f'<span class="floa">{word}</span>'

        elif(analizador(word)==3):
            word = f'<span class="scientific_notation">{word}</span>'
        
        elif(analizador(word)==4):
            word = f'<span class="complex_number">{word}</span>'

        elif(analizador(word)==5):
            word = f'<span class="dat">{word}</span>'

        #append the word to the list for reconstruct the text
        processed_content.append(word)
        
    # Join the processed words back into a string
    return ' '.join(processed_content)