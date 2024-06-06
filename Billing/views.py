from django.shortcuts import render, redirect, get_object_or_404

from Billing.forms import PromotionForm
from Billing.models import Promotion


# Create your views here.
def list_offers(request):
    if request.user.has_perm('accountant'):
        promotions = Promotion.objects.all()
        return render(request, 'billing/list_offers.html', {'ofertas': promotions})
    return redirect('home')

def create_offer(request):
    if request.user.has_perm('accountant'):
        if request.method == 'POST':
            form = PromotionForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('list_offers')
        else:
            form = PromotionForm()
        return render(request, 'billing/create_offer.html', {'form': form})
    return redirect('home')
  
def edit_offer(request):
    if request.user.has_perm('accountant'):
        offer = Promotion.objects.get(pk=request.POST['id'])
        if 'image' in request.FILES:
            offer.image = request.FILES['image']
        offer.title = request.POST['title']
        offer.description = request.POST['description']
        offer.save()
        return redirect('list_offers')
    return redirect('home')

def delete_offer(request, offer_id):
    if request.method == 'POST' and request.user.has_perm('accountant'):
        promotion = get_object_or_404(Promotion, id=offer_id)
        coupon = promotion.discount_code
        coupon.active = False
        coupon.save()
        promotion.delete()
        return redirect('list_offers')
    return redirect('home')

