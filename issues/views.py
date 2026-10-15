from django.shortcuts import render, redirect, get_object_or_404
from .models import Issue
from .forms import IssueForm
from django.core.mail import send_mail
from django.contrib.auth.decorators import user_passes_test,login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .forms import IssueForm,CustomUserCreationForm
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import logout
from .models import EmailLog
from django.core.mail import send_mail
from django.conf import settings

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)   # use custom form
        role = request.POST.get('role')
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully! You can now log in.")
            
            # Assign group based on role
            if role == 'staff':
                staff_group, created = Group.objects.get_or_create(name='MunicipalStaff')
                user.groups.add(staff_group)
            else:
                citizen_group, created = Group.objects.get_or_create(name='Citizens')
                user.groups.add(citizen_group)

            return redirect('login')
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()   # use custom form here too
    return render(request, 'registration/register.html', {'form': form})


@login_required
def redirect_after_login(request):
    if request.user.is_staff or request.user.groups.filter(name='MunicipalStaff').exists():
        return redirect('staff_dashboard')
    return redirect('citizen_dashboard')

def is_staff(user):
    return user.groups.filter(name='MunicipalStaff').exists() or user.is_staff


@login_required
def some_view(request):
    is_staff_user = is_staff(request.user)
    return render(request, 'base.html', {'is_staff_user': is_staff_user})

def issue_list(request):
    issues = Issue.objects.all()
    is_staff_user = request.user.is_staff or request.user.groups.filter(name='MunicipalStaff').exists()

    return render(request, 'issues/issue_list.html', {'issues': issues, 'is_staff_user': is_staff_user})

@login_required
def issue_detail(request, id):
    issue = get_object_or_404(Issue, id=id)
    is_staff_user = request.user.is_staff or request.user.groups.filter(name='MunicipalStaff').exists()
    return render(request, 'issues/issue_detail.html', {
        'issue': issue,
        'is_staff_user': is_staff_user
    })

@login_required
def issue_create(request):
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.created_by = request.user
            issue.status = 'open'
            issue.save()
            return redirect('issue_list')
    else:
        form = IssueForm()
    return render(request, 'issues/issue_form.html', {'form': form})

def map_view(request):
    issues = Issue.objects.all()
    return render(request, 'issues/map_view.html', {'issues': issues})

def is_municipal_staff(user):
    return user.groups.filter(name='MunicipalStaff').exists() or user.is_staff

@login_required
def issue_create(request):
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.created_by = request.user   # link complaint to citizen
            issue.status = 'open'
            issue.save()
            return redirect('issue_list')     # after complaint, show list
    else:
        form = IssueForm()
    return render(request, 'issues/issue_form.html', {'form': form})

@login_required
@user_passes_test(is_staff)
def staff_dashboard(request):
    # Show all complaints (or filter only open ones)
    complaints = Issue.objects.order_by('-created_at')
    is_staff_user = is_staff(request.user)
    return render(request,'issues/staff_dashboard.html', {'complaints': complaints,'is_staff_user': is_staff_user})


@login_required
@user_passes_test(is_staff)
def update_status(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)   
    if request.method == 'POST':
        issue.status = request.POST['status']
        issue.progress_notes = request.POST.get('progress_notes', issue.progress_notes)
        issue.save()

        # ✅ Only email if resolved
        if issue.status == 'resolved':
            print('inside issue status')
            send_mail(
                    subject=f"Issue '{issue.title}' resolved",
                    message=f"""Dear {issue.created_by.username},
                    Your complaint '{issue.title}' has been resolved.
                    Notes: {issue.progress_notes}
                    Thank you for using CivicTrack.
                    CivicTrack Team
                    """,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[issue.created_by.email],
                    fail_silently=False,
                    )
        messages.success(request, f"Issue '{issue.title}' updated successfully!")
        return redirect('staff_dashboard')
    return render(request, 'issues/update_status.html', {'issue': issue})


@login_required
def citizen_dashboard(request):
    complaints = Issue.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'issues/citizen_dashboard.html', {'complaints': complaints})


def custom_logout(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('login')


@login_required
@user_passes_test(is_staff)
def send_issue_email(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)

    if request.method == 'POST':
        message = request.POST.get('message', '').strip()
        if issue.status == 'resolved' and message:
            send_mail(
                subject=f"Follow-up on your complaint '{issue.title}'",
                message=message,
                from_email="noreply@civictrack.com",
                recipient_list=[issue.created_by.email],
            )
            messages.success(request, f"Email sent to {issue.created_by.username} ({issue.created_by.email}).")
        else:
            messages.error(request, "Please enter a message and ensure the complaint is resolved.")

    return redirect('staff_dashboard')

@login_required
@user_passes_test(is_staff)
def send_issue_email(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)

    if request.method == 'POST':
        message = request.POST.get('message', '').strip()
        if issue.status == 'resolved' and message:
            subject = f"Follow-up on your complaint '{issue.title}'"
            send_mail(
                subject=subject,
                message=message,
                from_email="noreply@civictrack.com",
                recipient_list=[issue.created_by.email],
            )

            # log the email
            EmailLog.objects.create(
                issue=issue,
                sent_to=issue.created_by.email,
                subject=subject,
                message=message,
                sent_by=request.user
            )

            messages.success(request, f"Email sent to {issue.created_by.username} ({issue.created_by.email}).")
        else:
            messages.error(request, "Please enter a message and ensure the complaint is resolved.")

    return redirect('staff_dashboard')
