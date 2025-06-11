from django.core.management.base import BaseCommand
from django.db.models import F
from accounts.models import User


class Command(BaseCommand):
    help = "모든 유저의 토큰을 50씩 증가시킵니다"

    def handle(self, *args, **options):
        User.objects.update(token=F('token') + 50)
        self.stdout.write(self.style.SUCCESS("토큰 업데이트 완료"))