



from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def resume_analysis(request):
    if request.method=='POST':
        resume=request.POST.get('resume')
        resume=resume.lower()

        matched=0
        keywords=['python','html','css','sql','django','pandas','c','c++','assembly8086','oops']
        missing_keywords=[]
        total_keywords=10
        for keyword in keywords:
            print(keyword)
            if keyword in resume:
                matched+=1
            else:
                missing_keywords.append(keyword)
        result=round(matched/total_keywords*100)
        print(result)
        context={
            'result':result,
            'missing_keywords':missing_keywords,
        }
        return render(request,'resume_form.html',context)
    else:
        return render(request,'resume_form.html')
# so we use cotext to show the data that user wants to see