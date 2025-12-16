from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db.models import Q
from .models import CodeSnippet, ExecutionHistory, UserProfile
from .forms import CodeSnippetForm, UserProfileForm

@login_required
def editor(request):
    """Main code editor view - redirects to studio editor."""
    from django.shortcuts import redirect
    return redirect('studio_editor')

@login_required
def snippet_detail(request, pk):
    """View and edit a code snippet."""
    snippet = get_object_or_404(CodeSnippet, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = CodeSnippetForm(request.POST, instance=snippet)
        if form.is_valid():
            form.save()
            return redirect('snippet_detail', pk=snippet.pk)
    else:
        form = CodeSnippetForm(instance=snippet)
    
    context = {
        'snippet': snippet,
        'form': form,
    }
    return render(request, 'editor/snippet_detail.html', context)

@login_required
def create_snippet(request):
    """Create a new code snippet."""
    if request.method == 'POST':
        form = CodeSnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.user = request.user
            snippet.save()
            return redirect('snippet_detail', pk=snippet.pk)
    else:
        form = CodeSnippetForm()
    
    context = {'form': form}
    return render(request, 'editor/create_snippet.html', context)

@login_required
def delete_snippet(request, pk):
    """Delete a code snippet."""
    snippet = get_object_or_404(CodeSnippet, pk=pk, user=request.user)
    if request.method == 'POST':
        snippet.delete()
        return redirect('editor')
    
    context = {'snippet': snippet}
    return render(request, 'editor/delete_snippet.html', context)

@login_required
def execution_history(request):
    """View execution history."""
    executions = ExecutionHistory.objects.filter(user=request.user)
    
    # Filter by language if provided
    language = request.GET.get('language')
    if language:
        executions = executions.filter(language=language)
    
    context = {
        'executions': executions,
        'languages': [
            ('python', 'Python'),
            ('cpp', 'C++'),
            ('c', 'C'),
            ('java', 'Java'),
        ]
    }
    return render(request, 'editor/history.html', context)

@login_required
def profile(request):
    """User profile view."""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    
    stats = {
        'total_snippets': CodeSnippet.objects.filter(user=request.user).count(),
        'total_executions': ExecutionHistory.objects.filter(user=request.user).count(),
        'recent_executions': ExecutionHistory.objects.filter(user=request.user)[:5],
    }
    
    context = {
        'profile': profile,
        'form': form,
        'stats': stats,
    }
    return render(request, 'editor/profile.html', context)
