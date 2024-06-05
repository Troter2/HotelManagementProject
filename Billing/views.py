from django.shortcuts import render, redirect

from Billing.forms import PromotionForm
from Billing.models import Promotion


# Create your views here.
def list_offers(request):
    if request.user.has_perm('accountant'):
        promotions = Promotion.objects.all()
        return render(request, 'billing/list_offers.html', {'ofertas': promotions})
    return redirect('home')

def create_offer(request):
    if request.method == 'POST':
        form = PromotionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list_offers')
    else:
        form = PromotionForm()
    return render(request, 'billing/create_offer.html', {'form': form})