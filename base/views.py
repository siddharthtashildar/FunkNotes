from django.shortcuts import render, redirect 
from .models import NoteDatabase, User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm,CreateNoteForm
from django.db.models import Q
from django.contrib.auth.hashers import check_password


# Create your views here.

def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')
        
    else:
        if request.method == 'POST':
            username = request.POST['email']
            password = request.POST['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')

            else:
                messages.info(request, 'Email or password is incorrect')

    return render(request, 'login_register.html', {'page': page})


def logoutUser(request):
    logout(request)
    return redirect('login')


def registerUser(request):
    page = 'Register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            if user is not None:
                login(request, user)
                return redirect('home')


    context = {'form': form, 'page': page}
    return render(request, 'login_register.html', context)


def home(request):
    page="Home"
    if request.user.is_authenticated:
        user_req=request.user.user_uuid
        Note=NoteDatabase.objects.filter(Note_user=user_req).order_by('-updated')[:6]
        context={"note":Note,'page': page}
    else:
        context={'page': page}
    return render(request, 'home.html',context)

#-------------------------------------------------------LOGIN REQUIRED-----------------------------------------------#



@login_required(login_url='login')
def noteslist(request):
    page='Notes'
    user_req=request.user.user_uuid

    Note=NoteDatabase.objects.filter(Note_user=user_req).order_by('-updated')
    
    if request.method=='GET':
        q=request.GET.get('q','')
        if q:
            Note=NoteDatabase.objects.filter(
                Q(Note_user=user_req) & Q(name__icontains=q) | Q(content__icontains=q)
            )
        else:
            Note=NoteDatabase.objects.filter(Note_user=user_req).order_by('-updated')
    else:
        Note=NoteDatabase.objects.filter(Note_user=user_req).order_by('-updated')

    context={"note":Note, 'page': page}

    return render(request, 'note_list.html',context)


@login_required(login_url='login')
def Note(request,pk):
    note=NoteDatabase.objects.get(noteID=pk)
    page='View | '+note.name
    context={"note":note, 'page': page }
    return render(request,'view_note.html',context)


@login_required(login_url='login')
def Create_note(request):
    user_req=request.user.user_uuid
    page="Create"
    form=CreateNoteForm()
    msg=''
    if request.method== 'POST':
        Note_name=request.POST.get('name')
        Note_content=request.POST.get('content')
        if Note_name == '' or Note_content =='':
            msg="Can't save note with empty fields!"
        else:
            NoteDatabase.objects.create(
                Note_user=request.user,
                name=Note_name,
                content=Note_content,)
    no_of_data=int(NoteDatabase.objects.filter(Note_user=user_req).count()) + 1
    def_title='Note-'+ str(no_of_data)
    context={'form':form, 'def_title':def_title,'msg':msg, 'page': page}
    return render(request,'create_note.html',context)


@login_required(login_url='login')
def Edit_note(request,pk):
    form=CreateNoteForm()
    note=NoteDatabase.objects.get(noteID=pk)
    page="Edit | "+ note.name
    context={"note":note,'form':form,'msg':'', 'page': page}
    if request.method== 'POST':
        Note_name=request.POST.get('name')
        Note_content=request.POST.get('content')
        if Note_name == '' or Note_content =='':
            msg="Can't save note with empty fields!"
            context={"note":note,'form':form,'msg':msg}
        else:
            note.name=Note_name
            note.content=Note_content
            note.save()
            return render(request,'view_note.html',context)
   
    return render(request,'edit_note.html',context)


@login_required(login_url='login')
def Delete_note(request,pk):
    form=CreateNoteForm()
    note=NoteDatabase.objects.get(noteID=pk)
    page='Delete | '+note.name
    if request.method == 'POST':
        note.delete()
        return redirect('home')
    context={"note":note,'form':form }
    return render(request,'delete_note.html',context)


@login_required(login_url='login')
def Settings(request):
    message=''
    page='Settings'
    if request.method=='POST':
        new_username=request.POST.get('Inputusername')
        check=User.objects.filter(username=new_username).exists()
        if check:
            message="Username already taken!"  
        else:
            request.session['new_username']=new_username
            return redirect('veri_pass')

    context={'message':message, 'page': page}
    return render(request,'settings.html',context)


@login_required(login_url='login')
def verify_pass(request):
    user_req=request.user.user_uuid
    user=User.objects.get(user_uuid=user_req)
    msg=''
    new_username=request.session.get('new_username')
    if request.method=='POST':
        user_entered_password=str(request.POST.get('inputpassword'))
        pass_check=check_password(user_entered_password, user.password)
        if not pass_check:
            msg='Invalid password!'
        else:
            user.username=new_username
            user.save()
            return redirect('settings')
    context={'msg':msg}
    return render(request,'user_password_verify.html',context)


@login_required(login_url='login')
def Edit_password(request):
    user_req=request.user.user_uuid
    user=User.objects.get(user_uuid=user_req)
    msg=''
    if request.method=='POST':
        Old_password=request.POST.get('inputoldpassword')
        New_password=request.POST.get('inputnewpassword')
        Confirm_new_password=request.POST.get('inputconfirmnewpassword')
        pass_check=check_password(Old_password,user.password)
        if not pass_check:
            msg='Old Password is Invalid!'
        else:
            if New_password != Confirm_new_password:
                msg='New password and Confirm new password doesnt match!'
            else:
                if Old_password == New_password:
                    msg='You entered the same password!'
                else:
                    if len(Confirm_new_password) < 8:
                        msg='Password must be atleast 8 digits long!'
                    else:
                        user.set_password(Confirm_new_password)
                        user.save()#PC*4p#rd2jx7C^$W
    context={'msg':msg}
    return render(request,'change_password.html',context)


@login_required(login_url='login')
def delete_account(request):
    user_req=request.user.user_uuid
    user=User.objects.get(user_uuid=user_req)
    msg=''
    if request.method=='POST':
        password=request.POST.get('inputpassword')
        confirm_txt=request.POST.get('inputconfirmtext')
        #dl_check=request.POST.get('downloadcheckbox')
        pass_check=check_password(password, user.password)
        if not pass_check:
            msg='Invalid password!'
        else:
            if confirm_txt !='Yes! delete my account':
                msg='Invalid confirmation text!'

            else:
                user.delete()
                return redirect('register')

    context={'msg':msg}
    return render(request,'delete_account.html',context)