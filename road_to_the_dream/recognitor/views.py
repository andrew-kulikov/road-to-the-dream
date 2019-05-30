from django.shortcuts import render, redirect
from .forms import PostForm
from .ai import Recognitor
from .models import Post
from django.conf import settings
import os
import cv2


def main_view(request, image_id):
    post = Post.objects.get(id=image_id)
    return render(
        request,
        'image_uploaded.html',
        {
            'url': settings.MEDIA_URL + 'images/' + str(image_id) + '-recognized.jpg',
            'old': post.image.url
        }
    )


def upload_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_image = form.save()
            result_photo, plate_number = Recognitor.recognize(new_image.image.path)

            if plate_number and len(plate_number) != 0:
                cv2.imwrite(os.path.join(settings.MEDIA_ROOT, 'images', str(new_image.id) + '-recognized.jpg'),
                            result_photo)

            return redirect('/recognitor/' + str(new_image.id))
    form = PostForm()
    return render(request, 'image_upload.html', {'form': form})
