from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
import json
from django.forms.models import modelform_factory
from django.views.generic import View
from user.models import User, Author, Image
from audio.models import Audio
from .models import Post, Comment
import sys
from .forms import PostImageForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User as djUser
from audio.views import handle_uploaded_file
from audio.forms import UploadFileForm
from django.shortcuts import redirect
class Wall(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request, path):
        try:
            xhr = request.GET['xhr']
        except:
            xhr = False
        if xhr == 'true':
            print(request.META["QUERY_STRING"])
            return redirect('/search' + '?' + request.META["QUERY_STRING"])
        try:
            prev = True
            next = True
            print(request.GET)
            if 'page' in request.GET:
                if request.GET['page']:
                    page = int(request.GET['page'])
                    if request.method == 'GET' and 'path' in request.GET:
                        if request.GET['path'] == 'next':
                            page += 1
                            print('next')
                        elif request.GET['path'] == 'prev':
                            page -= 1
                            print('prev')
                else:
                    page = 1
                    prev = False
            else:
                page = 1
                prev = False

            if User.objects.get(id=int(path)).wall.count() > page * 5 and page > 0:
                posts = User.objects.get(id=int(path)).wall.all().reverse()[(page - 1) * 5 : page* 5]
                if page == 1:
                    prev = False
            elif User.objects.get(id=int(path)).wall.count() > (page - 1) * 5 and page > 0:
                posts = User.objects.get(id=int(path)).wall.all().reverse()[(page - 1) * 5:]
                next = False
            elif page <= 0:
                page = 1
                posts = User.objects.get(id=int(path)).wall.all().reverse()[:5]
                prev = False
            else:
                print(page)
                page = User.objects.get(id=int(path)).wall.count() // 5
                print(page)
                posts = User.objects.get(id=int(path)).wall.all().reverse()[(page) * 5:]
                next = False
            user = User.objects.get(id=int(path))
        except User.DoesNotExist:
            return HttpResponse(json.dumps({'error masage' : 'does not exist'}), content_type="application/json")
        except:
            return HttpResponse(json.dumps({'error masage' : 'server error'}), content_type="application/json")
        max_page = User.objects.get(id=int(path)).wall.count() // 5 + 1
        return render(request, "wall.html", {'posts': posts, 'user': user, 'you': request.user.customUser, 'page': page, 'next': next, 'prev': prev, 'max' : max_page})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request, path):
        print(request.POST)
        print(request.FILES)
        if 'comment_text' in request.POST:
            try:
                Comment.objects.create(text = request.POST['comment_text'], post = Post.objects.get(id=request.POST['id']), owner = request.user.customUser)
            except:
                print("Unexpected error:", sys.exc_info())
        elif 'delete' in request.POST:
            id = int(request.POST['delete'])
            print(id)
            you = request.user.customUser
            p = Post.objects.get(id=id)
            if p.creator == you or p.owner == you:
                p.delete()
                print('deleted')
            return self.get(request, path)
        elif 'post_text' in request.POST:
            try:
                audios_id = []
                try:
                    if request.POST['audios'] != '':
                        if request.POST['audios'].find('_') != -1:
                            audios_id = request.POST['audios'].split('_')
                        else:
                            audios_id.append(request.POST['audios'])
                        print(request.POST['audios'])

                except:
                    print('error in audio')
                images = []
                try:
                    if 'post_image' in request.FILES:
                        form = PostImageForm(request.POST, request.FILES)
                        if form.is_valid():
                            #handle_uploaded_file(request.FILES['post_image'])
                            img = Image.objects.create(file=request.FILES['post_image'])
                            img.save()
                            images.append(img)
                        else:
                            print('form invalid')
                except:
                    print("Unexpected error:", sys.exc_info())
                p = Post.objects.create(text = request.POST['post_text'], creator = request.user.customUser, owner = User.objects.get(id=int(path)))
                for audio in audios_id:
                    p.audio.add(Audio.objects.get(id=int(audio)))
                for img in images:
                    p.image.add(img)
                p.save()
            except:
                print("Unexpected error:", sys.exc_info())
        elif 'image' in request.FILES:
            try:
                form = UploadFileForm(request.POST, request.FILES)
                if form.is_valid():
                    handle_uploaded_file(request.FILES['image'])
                else:
                    HttpResponse(json.dumps({'error': 'form invalid'}), content_type="application/json")
                i = Image.objects.create(file = request.FILES['image'])
                request.user.customUser.avatar = i
                i.save()
                request.user.customUser.save()
                print(i)

            except:
                print("Unexpected error:", sys.exc_info())
        return self.get(request, path)
@login_required(login_url='/login/')
def del_post(request, path1, path2):
    id = int(path2)
    print(path1, path2)
    you = request.user.customUser
    response_dict = {'status': 'wrong method'}
    if request.method == 'DELETE':
        p = Post.objects.get(id=id)
        if p.creator == you or p.owner == you:
            p.delete()
            response_dict = {'status' : 'ok'}
            print('deleted')
        else:
            response_dict = {'status': 'error'}
    return HttpResponse(json.dumps(response_dict), content_type='application/javascript')