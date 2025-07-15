from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Category, Suggestion, Reply
from .forms import UserRegistrationForm, SuggestionForm, ReplyForm, CategoryForm
from textblob import TextBlob

def home(request):
    """Home page with suggestion submission form"""
    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():
            suggestion = form.save(commit=False)
            if request.user.is_authenticated:
                suggestion.user = request.user
            # NLP: Sentiment analysis
            blob = TextBlob(suggestion.content)
            suggestion.sentiment = blob.sentiment.polarity
            # NLP: Spam detection (simple rule: if too short or contains spammy words)
            spam_keywords = ['buy now', 'free', 'click here', 'subscribe', 'visit', 'winner', 'prize']
            content_lower = suggestion.content.lower()
            suggestion.is_spam = (
                len(suggestion.content) < 10 or
                any(word in content_lower for word in spam_keywords)
            )
            # NLP: Auto-categorization (simple keyword-based)
            category_map = {
                'library': 'Library & Study Spaces',
                'book': 'Library & Study Spaces',
                'parking': 'Transportation & Parking',
                'bus': 'Transportation & Parking',
                'food': 'Cafeteria & Food',
                'canteen': 'Cafeteria & Food',
                'classroom': 'Classroom & Academic',
                'teacher': 'Classroom & Academic',
                'maintenance': 'Facilities & Maintenance',
                'clean': 'Facilities & Maintenance',
            }
            auto_cat = None
            for keyword, cat in category_map.items():
                if keyword in content_lower:
                    auto_cat = cat
                    break
            suggestion.auto_category = auto_cat
            suggestion.save()
            messages.success(request, 'Suggestion submitted successfully!')
            return redirect('dashboard')
    else:
        form = SuggestionForm()
    
    categories = Category.objects.all()
    return render(request, 'core/home.html', {
        'form': form,
        'categories': categories
    })

def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'core/register.html', {'form': form})

def user_login(request):
    """User login view"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'core/login.html')

def user_logout(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'Logout successful!')
    return redirect('home')

@login_required
def dashboard(request):
    """Dashboard view showing user's suggestions"""
    if request.user.is_superuser:
        # Superuser sees all suggestions
        suggestions = Suggestion.objects.all().order_by('-created_at')
    elif hasattr(request.user, 'category_admin'):
        # Category admin sees only their categories
        suggestions = Suggestion.objects.filter(category__in=request.user.category_admin.categories.all()).order_by('-created_at')
    else:
        # Regular users see only their own suggestions
        suggestions = Suggestion.objects.filter(user=request.user).order_by('-created_at')

    # Accurate status counts
    total_count = suggestions.count()
    under_review_count = suggestions.filter(status='under_review').count()
    accepted_count = suggestions.filter(status='accepted').count()
    rejected_count = suggestions.filter(status='rejected').count()

    categories = Category.objects.all()
    return render(request, 'core/dashboard.html', {
        'suggestions': suggestions,
        'categories': categories,
        'total_count': total_count,
        'under_review_count': under_review_count,
        'accepted_count': accepted_count,
        'rejected_count': rejected_count,
    })

@login_required
def suggestion_detail(request, suggestion_id):
    """Detailed view of a suggestion with replies"""
    suggestion = get_object_or_404(Suggestion, id=suggestion_id)
    # Permission: can this user manage this suggestion?
    can_manage = False
    can_view = False
    if request.user.is_superuser:
        can_manage = True
        can_view = True
    elif hasattr(request.user, 'category_admin'):
        if suggestion.category in request.user.category_admin.categories.all():
            can_manage = True
            can_view = True
    if suggestion.user == request.user:
        can_view = True
    # Block if not allowed to view
    if not can_view:
        messages.error(request, 'You do not have permission to view this suggestion.')
        return redirect('dashboard')
    if request.method == 'POST' and can_manage:
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.suggestion = suggestion
            reply.admin = request.user
            reply.save()
            messages.success(request, 'Reply added successfully!')
            return redirect('suggestion_detail', suggestion_id=suggestion.id)
    else:
        reply_form = ReplyForm()
    return render(request, 'core/suggestion_detail.html', {
        'suggestion': suggestion,
        'reply_form': reply_form,
        'can_manage': can_manage,
    })

@login_required
def admin_panel(request):
    """Admin panel for managing categories and suggestions"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')

    categories = Category.objects.all().order_by('-created_at')
    # Superuser: see all pending suggestions
    if request.user.is_superuser:
        pending_suggestions = Suggestion.objects.filter(status='under_review').order_by('-created_at')
    else:
        # Category admin: see only suggestions in their categories
        try:
            cat_admin = request.user.category_admin
            pending_suggestions = Suggestion.objects.filter(
                status='under_review',
                category__in=cat_admin.categories.all()
            ).order_by('-created_at')
        except Exception:
            pending_suggestions = Suggestion.objects.none()

    return render(request, 'core/admin_panel.html', {
        'categories': categories,
        'pending_suggestions': pending_suggestions
    })

@login_required
def add_category(request):
    """Add new category (admin only)"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.created_by = request.user
            category.save()
            messages.success(request, 'Category added successfully!')
            return redirect('admin_panel')
    else:
        form = CategoryForm()
    
    return render(request, 'core/add_category.html', {'form': form})

@login_required
@require_POST
def update_suggestion_status(request, suggestion_id):
    """Update suggestion status (admin only)"""
    suggestion = get_object_or_404(Suggestion, id=suggestion_id)
    # Permission: can this user manage this suggestion?
    can_manage = False
    if request.user.is_superuser:
        can_manage = True
    elif hasattr(request.user, 'category_admin'):
        if suggestion.category in request.user.category_admin.categories.all():
            can_manage = True
    if not can_manage:
        print(f"[DEBUG] User {request.user} tried to update status without permission.")
        return JsonResponse({'error': 'Access denied'}, status=403)
    status = request.POST.get('status')
    print(f"[DEBUG] Received status update for suggestion {suggestion_id}: {status}")
    if status in ['under_review', 'accepted', 'rejected']:
        suggestion.status = status
        suggestion.save()
        print(f"[DEBUG] Status for suggestion {suggestion_id} updated to {status}.")
        return JsonResponse({'success': True, 'status': status})
    print(f"[DEBUG] Invalid status value received: {status}")
    return JsonResponse({'error': 'Invalid status'}, status=400)
