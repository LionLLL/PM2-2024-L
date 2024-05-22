from django.shortcuts import render
from re import compile,sub,IGNORECASE
# Create your views here.

def home(request):
    if(request.method == 'POST'):
        input_text = request.POST.get('input_text', '')
        highlighted_text = highlight_text(input_text)
        return render(request, 'home.html', {'highlighted_text': highlighted_text})
    return render(request, 'home.html')

def highlight_text(text):
    #keywords(in lowercase)
    lowercase_keywords = ["if", "else", "while", "for"]

    #regular expression
    int_pattern = compile(r'(\b\d+\b)')
    float_pattern = compile(r'(\b\d+\.\d+\b)')

    #process each line individually
    lines = text.split('\n')
    processed_lines = []

    for line in lines:
        #preserve indentation
        indentation = len(line)-len(line.lstrip())
        indented_text = '&nbsp;'*indentation

        #highlight integers and floating numbers
        line = float_pattern.sub(r'<span style="color:blue;">\1</span>', line)
        line = int_pattern.sub(r'<span style="color:blue;">\1</span>', line)

        #highlight keywords (case-insensitive)
        for keyword in lowercase_keywords:
            line = sub(r'\b{}\b'.format(keyword), r'<span style="color:blue;">{}</span>'.format(keyword), line, flags=IGNORECASE)

        #indentation back to the processed line
        processed_lines.append(indented_text + line)

    # Re build the text
    highlighted_text = '<br>'.join(processed_lines)

    return highlighted_text
