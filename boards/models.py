from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

def board_image_path(instance, filename):
    return f'boards/{instance.pk}/images/{filename}'


# Create your models here.
class Board(models.Model):
    title = models.CharField(max_length=10)
    content = models.TextField()
    #나중에 추가한건 실제로는 표에서 맨 뒤에 뜸
    image = ProcessedImageField(
                upload_to=board_image_path,          #저장 위치
                processors=[ResizeToFill(200,300)], #처리할 작업 목록     여러가지 들어갈 수 있음
                format='JPEG',                      #저장 포맷
                options={'quality':90},             #옵션
        )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.id}: {self.title}"
        
class Comment(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)     
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.content

