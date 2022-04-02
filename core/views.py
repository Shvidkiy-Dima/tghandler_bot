import json
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponseNotAllowed
from core.models import User
from bot.run_polling import TelegramBot
from bot import reply_text


@csrf_exempt
def handle_error(request: HttpRequest):

    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    data = json.loads(request.body.decode())
    code = data.get('code', None)
    error = data.get('error', None)

    if not code or not error:
        return HttpResponseBadRequest('error and code required fields in request body')

    user = get_object_or_404(User, code=code)

    text = reply_text.error(error)
    TelegramBot.bot.send_message(text=text, chat_id=user.user_id, parse_mode='MarkdownV2')
    return HttpResponse(status=200)
