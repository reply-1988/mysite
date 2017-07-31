from django.test import TestCase
from django.utils import timezone
from .models import Question
from django.core.urlresolvers import reverse
import datetime
# Create your tests here.


def create_question(question_txt, days):
    """创建一个以question_txt为标题，pub_date为days天之后的问题。days为正表示将来，为负表示过去"""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_txt=question_txt, pub_date=time)


class QuestionViewTest(TestCase):
    def test_index_view_with_no_questions(self):
        """如果数据库中没有投票，应该显示一个合适的信息"""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_a_past_question(self):
        """pub_date是过去的问题应该被显示在主页上"""
        create_question(question_txt='Past question', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question>']
        )

    def test_index_view_with_a_future_question(self):
        """pub_date是未来的问题应该不显示"""
        create_question(question_txt='future question', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No polls are available.', status_code=200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_future_question_and_past_question(self):
        """其中pub_date为未来的不应该显示"""
        create_question(question_txt='future question', days=30)
        create_question(question_txt='past question', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'], ['<Question: past question>']
        )

    def test_index_view_with_two_past_question(self):
        """目录页应该能够显示多个问题"""
        create_question(question_txt='Past question 1', days=-3)
        create_question(question_txt='Past question 2', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'], ['<Question: Past question 1>',
                                                       '<Question: Past question 2>'])


class QuestionMethodTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """was_published_recently应该对pub_date是未来的那些问题返回false"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertEqual(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """was_published_recently应该对pub_date是过去一天之外的那些问题返回false"""
        time = timezone.now() - datetime.timedelta(days=30)
        past_question = Question(pub_date=time)
        self.assertEqual(past_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """was_published_recently应该对pub_date是过去一天之内的那些问题返回false"""
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(pub_date=time)
        self.assertEqual(recent_question.was_published_recently(), True)


class QuestionIndexDetailTests(TestCase):
    def test_detail_view_with_a_future_question(self):
        """访问将来的投票将会发布一个404错误"""
        future_question = create_question(question_txt='future question', days=10)
        response = self.client.get(reverse('polls:detail', args=(future_question.id, )))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_question(self):
        """访问过去的投票页面，页面上应该显示投票信息"""
        past_question = create_question(question_txt='past question', days=-10)
        response = self.client.get(reverse('polls:detail', args=(past_question.id, )))
        self.assertContains(response, past_question.question_txt, status_code=200)