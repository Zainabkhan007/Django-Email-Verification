from django.shortcuts import render,HttpResponse,redirect
from blog.models import Post,BlogComment
from django.contrib import messages
from django.contrib.auth.models import User 

# Create your views here.
def Blog(request):
    allpost=Post.objects.all()
    context={"allpost":allpost}
    return render(request,"blog/blog.html",context)

def BlogPost(request,slug):
    post=Post.objects.filter(slug=slug).first()
    post.views=post.views + 1
    post.save()

    comments=BlogComment.objects.filter(post=post,parent=None)
    replies=BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
     if reply.parent.sno not in replyDict.keys():
        replyDict[reply.parent.sno]=[reply]
     else:
        replyDict[reply.parent.sno].append(reply)
    
    context={"post":post, "comments":comments,"user":request.user,"replyDict":replyDict}
    return render(request,"blog/blogpost.html",context)

def postComment(request):
    if request.method=="POST":
        comment=request.POST.get("comment")
        user=request.user
        postSno=request.POST.get("postSno")
        post=Post.objects.get(sno=postSno)
        parentSno=request.POST.get("parentSno")
        if parentSno == "":
          new_comment=BlogComment(comment=comment,user=user,post=post)
          new_comment.save()
          messages.success(request,"Your comment has been successfully post")

        else:
            parent = BlogComment.objects.get(sno=parentSno)
            new_comment = BlogComment(comment=comment,user=user,post=post,parent=parent)
           
            new_comment.save()
            messages.success(request,"Your reply has been successfully post")
    return redirect(f"/blog/{post.slug}")
