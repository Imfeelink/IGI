import logging

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ReviewForm
from .models import Review

logger = logging.getLogger('apps.reviews')


def review_list_view(request):
    q = request.GET.get('q', '').strip()
    sort = request.GET.get('sort', '-created_at')
    allowed = {'rating', '-rating', 'created_at', '-created_at'}
    if sort not in allowed:
        sort = '-created_at'
    reviews = Review.objects.select_related('user', 'property_obj')
    if q:
        reviews = reviews.filter(
            Q(text__icontains=q) | Q(property_obj__title__icontains=q) | Q(user__username__icontains=q)
        )
    reviews = reviews.order_by(sort)
    return render(request, 'reviews/review_list.html', {'reviews': reviews, 'q': q, 'sort': sort})


def review_detail_view(request, pk):
    review = get_object_or_404(Review, pk=pk)
    return render(request, 'reviews/review_detail.html', {'review': review})


@login_required
def review_create_view(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            logger.info('Review created by %s for %s', request.user.username, review.property_obj.title)
            return redirect('reviews:review_list')
    else:
        form = ReviewForm()
    return render(request, 'reviews/review_form.html', {'form': form, 'title': 'Оставить отзыв'})


@login_required
def review_update_view(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if review.user != request.user and not request.user.is_staff:
        return redirect('reviews:review_list')
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('reviews:review_list')
    else:
        form = ReviewForm(instance=review)
    return render(request, 'reviews/review_form.html', {'form': form, 'title': 'Редактировать отзыв'})


@login_required
def review_delete_view(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if review.user != request.user and not request.user.is_staff:
        return redirect('reviews:review_list')
    if request.method == 'POST':
        review.delete()
        logger.info('Review deleted: %s', pk)
        return redirect('reviews:review_list')
    return render(request, 'reviews/review_confirm_delete.html', {'review': review})
