from denied.authorizers import any_authorized
from denied.decorators import authorize
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import reverse  # type: ignore  # Issue 762
from django.views.decorators.http import require_POST

from .forms import ReferralForm


@require_POST
@authorize(any_authorized)
def create_referral(request):
    """Create a referral."""
    email = request.POST.get("email", "missing email")
    data = {"email": email, "referring_user": request.user}
    form = ReferralForm(data=data)
    if form.is_valid():
        form.save()
        messages.success(request, "We will message your friend shortly.")
    else:
        messages.error(request, f"'{email}' is an invalid email address.")
    return HttpResponseRedirect(reverse("settings:dashboard"))
