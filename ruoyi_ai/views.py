from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils.translation import activate, get_language
from django.views.decorators.csrf import csrf_exempt
from .langchain_config import create_chat_chain
from .crewai_config import create_crew


def home(request):
    """
    首页视图
    """
    try:
        return render(request, 'chat/index.html')
    except Exception as e:
        return HttpResponse(f'Error: {str(e)}')


def set_language(request):
    """
    设置语言
    """
    if request.method == 'POST':
        language = request.POST.get('language')
        if language:
            # 激活语言
            activate(language)
            # 保存到 cookie
            response = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            response.set_cookie('django_language', language, max_age=365 * 24 * 60 * 60)  # 1年
            return response
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@csrf_exempt
def langchain_chat(request):
    """
    LangChain聊天接口
    """
    if request.method == 'POST':
        try:
            # 获取请求数据
            data = request.POST
            question = data.get('question', '')
            
            if not question:
                return JsonResponse({'error': 'Question is required'}, status=400)
            
            # 创建聊天链
            chain = create_chat_chain()
            
            # 执行聊天
            result = chain.invoke({"question": question})
            
            return JsonResponse({'response': result})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'POST method required'}, status=405)

@csrf_exempt
def crewai_task(request):
    """
    CrewAI任务接口
    """
    if request.method == 'POST':
        try:
            # 获取请求数据
            data = request.POST
            topic = data.get('topic', '')
            
            if not topic:
                return JsonResponse({'error': 'Topic is required'}, status=400)
            
            # 创建团队
            crew = create_crew(topic)
            
            # 执行任务
            result = crew.kickoff()
            
            return JsonResponse({'response': str(result)})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'POST method required'}, status=405)
