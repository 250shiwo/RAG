from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ChatHistory


class ChatHistoryView(APIView):
    """对话历史记录接口"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取用户的对话历史记录"""
        kb_id = request.query_params.get('kb_id')
        
        queryset = ChatHistory.objects.filter(user=request.user)
        if kb_id:
            queryset = queryset.filter(kb_id=kb_id)
        
        # 分页获取，默认每页10条
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        start = (page - 1) * page_size
        end = start + page_size
        
        history_list = queryset[start:end]
        total = queryset.count()
        
        # 构建响应数据
        data = []
        for history in history_list:
            data.append({
                'id': history.id,
                'kb_id': history.kb_id,
                'question': history.question,
                'answer': history.answer,
                'created_at': history.created_at,
                'token_usage': history.token_usage,
                'elapsed_ms': history.elapsed_ms
            })
        
        return Response({
            'items': data,
            'total': total,
            'page': page,
            'page_size': page_size
        })
    
    def delete(self, request, history_id):
        """删除对话历史记录"""
        try:
            history = ChatHistory.objects.get(id=history_id, user=request.user)
            history.delete()
            return Response({'detail': '删除成功'}, status=status.HTTP_200_OK)
        except ChatHistory.DoesNotExist:
            return Response({'detail': '记录不存在'}, status=status.HTTP_404_NOT_FOUND)
