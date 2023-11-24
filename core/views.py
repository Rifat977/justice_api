from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

# OPENAI_API_KEY = Config('OPENAI_API_KEY')

llm = OpenAI(api_key='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')
chat_model = ChatOpenAI(api_key='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')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def index(request):
    prompt = request.data.get('prompt', '')

    if not prompt:
        return JsonResponse({'error': 'Please provide a prompt in the request data.'}, status=400)

    try:
        llm_result = llm.generate([prompt])
        chat_result = chat_model.get_response(prompt)
    except Exception as e:
        return JsonResponse({'error': f'Error processing the request: {str(e)}'}, status=500)

    return JsonResponse({'llm_result': llm_result, 'chat_result': chat_result})
