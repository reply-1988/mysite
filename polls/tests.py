from django.test import TestCase
from django.utils import timezone
from .models import Question
import datetime
# Create your tests here.


class QuestionMethodTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """was_published_recently应该对pub_date是未来的那些问题返回false"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertEqual(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """was_published_recently应该对pub_date是过去一天之外的那些问题返回false"""
        time = timezone.now() - datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertEqual(future_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """was_published_recently应该对pub_date是过去一天之内的那些问题返回false"""
        time = timezone.now() - datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertEqual(future_question.was_published_recently(), False)