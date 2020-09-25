from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from . import forms


def registration_view(request):
    if request.method == "POST":
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created!')
            return HttpResponseRedirect(reverse('accounts:login'))
    else:
        form = forms.RegistrationForm()
    return render(request, 'accounts/registration.html', {'form': form})


class ProfileView(DetailView):
    model = get_user_model()
    template_name = 'accounts/profile.html'


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    form_class = forms.ChangePasswordForm
    template_name = 'accounts/pwchange.html'

    def get_success_url(self):
        return reverse_lazy(
            'accounts:profile',
            kwargs={'pk': self.request.user.id}
            )


@login_required
def profile_update(request):
    if request.method == 'POST':
        p_form = forms.ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
            )
        u_form = forms.UpdateUserForm(request.POST, instance=request.user)

        if u_form.is_valid() and p_form.is_valid():
            p_form.save()
            u_form.save()
            messages.success(request, 'Your account has been updated!')
            # return redirect('accounts:profile', pk=request.user.pk)
            return HttpResponseRedirect(reverse(
                'accounts:profile',
                kwargs={'pk': request.user.pk}
                ))
    else:
        p_form = forms.ProfileUpdateForm(instance=request.user.profile)
        u_form = forms.UpdateUserForm(instance=request.user)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'accounts/update_profile.html', context)
