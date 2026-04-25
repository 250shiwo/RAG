from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import StreamingHttpResponse
from datetime import date

from knowledge.models import KnowledgeBase
from users.models import UserUsage, UserSubscription
from .models import ChatHistory

from .serializers import RagChatRequestSerializer
from .services import RagError, rag_chat, rag_chat_stream


def check_chat_limit(user):
    """检查用户的聊天次数限制"""
    today = date.today()
    usage, created = UserUsage.objects.get_or_create(user=user, date=today)
    
    # 获取用户的每日聊天限制
    try:
        subscription = UserSubscription.objects.get(user=user)
        if subscription.is_active:
            daily_limit = subscription.plan.daily_chat_limit
        else:
            daily_limit = 5  # 免费版默认5次
    except UserSubscription.DoesNotExist:
        daily_limit = 5  # 免费版默认5次
    
    if usage.chat_count >= daily_limit:
        return False, daily_limit
    
    # 增加使用次数
    usage.chat_count += 1
    usage.save()
    
    return True, daily_limit


class RagChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 检查聊天次数限制
        allowed, daily_limit = check_chat_limit(request.user)
        if not allowed:
            return Response(
                {"detail": f"今日聊天次数已达上限（{daily_limit}次），请升级订阅或明日再试"},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        serializer = RagChatRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        kb_id = serializer.validated_data["kb_id"]
        question = serializer.validated_data["question"]
        session_id = serializer.validated_data.get("session_id")

        kb = KnowledgeBase.objects.filter(id=kb_id, user=request.user).first()
        if kb is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            # 获取历史对话记录，用于多轮对话
            history = ChatHistory.objects.filter(
                user=request.user,
                kb_id=kb_id,
                session_id=session_id
            ).order_by('created_at')
            
            # 构建对话历史上下文
            context = ""
            for item in history:
                context += f"用户: {item.question}\n助手: {item.answer}\n"
            
            # 将上下文添加到当前问题中
            if context:
                full_question = f"历史对话:\n{context}\n\n当前问题: {question}"
            else:
                full_question = question
            
            payload = rag_chat(kb, full_question)
            # 保存对话记录
            ChatHistory.objects.create(
                user=request.user,
                kb_id=kb_id,
                session_id=session_id,
                question=question,
                answer=payload.get('answer', ''),
                token_usage=payload.get('token_usage'),
                elapsed_ms=payload.get('elapsed_ms')
            )
            # 在响应中添加session_id
            payload['session_id'] = str(session_id)
        except RagError as e:
            return Response({"detail": e.detail}, status=e.status_code)

        return Response(payload, status=status.HTTP_200_OK)


class RagChatStreamView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 检查聊天次数限制
        allowed, daily_limit = check_chat_limit(request.user)
        if not allowed:
            return Response(
                {"detail": f"今日聊天次数已达上限（{daily_limit}次），请升级订阅或明日再试"},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        serializer = RagChatRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        kb_id = serializer.validated_data["kb_id"]
        question = serializer.validated_data["question"]
        session_id = serializer.validated_data.get("session_id")

        kb = KnowledgeBase.objects.filter(id=kb_id, user=request.user).first()
        if kb is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            # 获取历史对话记录，用于多轮对话
            history = ChatHistory.objects.filter(
                user=request.user,
                kb_id=kb_id,
                session_id=session_id
            ).order_by('created_at')
            
            # 构建对话历史上下文
            context = ""
            for item in history:
                context += f"用户: {item.question}\n助手: {item.answer}\n"
            
            # 将上下文添加到当前问题中
            if context:
                full_question = f"历史对话:\n{context}\n\n当前问题: {question}"
            else:
                full_question = question
            
            stream, stream_state = rag_chat_stream(kb, full_question)
        except RagError as e:
            return Response({"detail": e.detail}, status=e.status_code)

        def gen():
            for delta in stream:
                yield (delta or "").encode("utf-8", errors="ignore")
            
            # 对话结束后保存对话记录
            ChatHistory.objects.create(
                user=request.user,
                kb_id=kb_id,
                session_id=session_id,
                question=question,
                answer=stream_state.get('answer', ''),
                token_usage=stream_state.get('token_usage'),
                elapsed_ms=stream_state.get('elapsed_ms')
            )

        resp = StreamingHttpResponse(gen(), content_type="text/plain; charset=utf-8")
        resp["Cache-Control"] = "no-cache"
        resp["X-Accel-Buffering"] = "no"
        resp["X-Session-ID"] = str(session_id)
        return resp
