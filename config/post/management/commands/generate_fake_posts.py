from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
from post.models import Post
from django.utils.text import slugify
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Generate 100 fake posts'

    def handle(self, *args, **kwargs):
        fake = Faker()
        users = list(User.objects.all())

        if not users:
            self.stdout.write(self.style.ERROR("هیچ کاربری در دیتابیس وجود ندارد."))
            return

        for _ in range(100):
            user = random.choice(users)
            title = fake.sentence(nb_words=6)
            description = fake.paragraph(nb_sentences=5)
            slug = slugify(title) + '-' + fake.uuid4()[:8]

            post = Post.objects.create(
                user=user,
                title=title,
                slug=slug,
                description=description,
                public=True,
                is_repost=False,
            )

        self.stdout.write(self.style.SUCCESS('✅ 100 پست فیک ساخته شد.'))
