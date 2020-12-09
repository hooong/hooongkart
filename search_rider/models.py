from django.db import models


class SearchLog(models.Model):
    # 최근 검색 저장을 위한 모델
    nickname = models.CharField(max_length=255)
    access_id = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nickname
