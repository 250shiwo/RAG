from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ChatHistory
from knowledge.models import KnowledgeBase


class ChatHistoryView(APIView):
    """对话历史记录接口"""
    permission_classes = [IsAuthenticated]

    def _get_kb_name_map(self, user, kb_ids):
        """批量查询知识库名称，避免历史记录里始终显示默认文案。"""
        if not kb_ids:
            return {}
        return {
            item["id"]: item["name"]
            for item in KnowledgeBase.objects.filter(user=user, id__in=kb_ids).values("id", "name")
        }
    
    def get(self, request, history_id=None):
        """获取用户的对话历史记录或单条详情"""
        if history_id is not None:
            try:
                history = ChatHistory.objects.get(id=history_id, user=request.user)
                kb_name = self._get_kb_name_map(request.user, [history.kb_id]).get(history.kb_id)
                return Response({
                    'id': history.id,
                    'kb_id': history.kb_id,
                    'question': history.question,
                    'answer': history.answer,
                    'created_at': history.created_at,
                    'token_usage': history.token_usage,
                    'elapsed_ms': history.elapsed_ms,
                    'knowledge_base_name': kb_name,
                })
            except ChatHistory.DoesNotExist:
                return Response({'detail': '记录不存在'}, status=status.HTTP_404_NOT_FOUND)

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
        kb_name_map = self._get_kb_name_map(request.user, [history.kb_id for history in history_list])
        
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
                'elapsed_ms': history.elapsed_ms,
                'knowledge_base_name': kb_name_map.get(history.kb_id),
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
