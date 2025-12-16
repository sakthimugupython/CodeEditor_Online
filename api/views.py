from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from editor.models import CodeSnippet, ExecutionHistory
from .serializers import CodeSnippetSerializer, ExecutionHistorySerializer, ExecutionRequestSerializer
from executor.runner import CodeRunner

class CodeSnippetViewSet(viewsets.ModelViewSet):
    """API for managing code snippets."""
    serializer_class = CodeSnippetSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return CodeSnippet.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ExecutionViewSet(viewsets.ViewSet):
    """API for code execution."""
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def execute(self, request):
        """Execute code and return results."""
        serializer = ExecutionRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        code = serializer.validated_data['code']
        language = serializer.validated_data['language']
        stdin = serializer.validated_data.get('stdin', '')
        snippet_id = serializer.validated_data.get('snippet_id')
        
        # Run the code
        result = CodeRunner.run(code, language, stdin)
        
        # Determine status
        if result['error']:
            exec_status = 'error'
        elif result['timeout']:
            exec_status = 'timeout'
        elif result['memory_exceeded']:
            exec_status = 'memory_exceeded'
        else:
            exec_status = 'success'
        
        # Save to history
        snippet = None
        if snippet_id:
            try:
                snippet = CodeSnippet.objects.get(id=snippet_id, user=request.user)
            except CodeSnippet.DoesNotExist:
                pass
        
        execution = ExecutionHistory.objects.create(
            user=request.user,
            snippet=snippet,
            code=code,
            language=language,
            stdin=stdin,
            stdout=result['stdout'],
            stderr=result['stderr'],
            returncode=result['returncode'],
            status=exec_status,
            execution_time=result.get('execution_time', 0),
        )
        
        return Response({
            'id': execution.id,
            'stdout': result['stdout'],
            'stderr': result['stderr'],
            'returncode': result['returncode'],
            'status': exec_status,
            'timeout': result['timeout'],
            'error': result['error'],
            'execution_time': result.get('execution_time', 0),
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def history(self, request):
        """Get execution history."""
        executions = ExecutionHistory.objects.filter(user=request.user)
        
        language = request.query_params.get('language')
        if language:
            executions = executions.filter(language=language)
        
        serializer = ExecutionHistorySerializer(executions, many=True)
        return Response(serializer.data)
