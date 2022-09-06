from posts.forms import PostForm
from ..models import Post
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )
        cls.form = PostForm()

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        self.somebody = User.objects.create_user(username='SomeBodyToLove')
        # Создаем второй клиент
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(self.somebody)

    def post_create_post(self):
        """Валидная форма создает запись в Post."""
        # Подсчитаем количество записей в Task
        posts_count = Post.objects.count()

        form_data = {
            'author': self.authorized_client,
            'text': 'Тестовый текст',
        }
        # Отправляем POST-запрос
        self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        # Проверяем, увеличилось ли число постов
        self.assertEqual(Post.objects.count(), posts_count + 1)

    def test_edit_post(self):
        form_data = {
            'text': 'Новый текст поста'
        }
        self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': '1'}),
            data=form_data,
            follow=True
        )
        self.assertTrue(
            Post.objects.filter(
                id=1,
                author=self.user,
                text='Новый текст поста',
            ).exists()
        )
