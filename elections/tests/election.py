from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import IntegrityError

from elections.models import Election
from elections.forms import ElectionForm


class ElectionModelTest(TestCase):
    def test_create_election(self):
        user, created = User.objects.get_or_create(username='joe')
        election, created = Election.objects.get_or_create(name='BarBaz',
                                                           owner=user,
                                                           slug='barbaz',
                                                           description='esta es una descripcion')
        self.assertTrue(created)
        self.assertEqual(election.name, 'BarBaz')
        self.assertEqual(election.owner, user)
        self.assertEqual(election.slug, 'barbaz')
        self.assertEqual(election.description, 'esta es una descripcion')

    def test_create_two_election_by_same_user_with_same_slug(self):
        user = User.objects.create_user(username='joe', password='doe', email='joe@doe.cl')
        election = Election.objects.create(name='BarBaz',
                                                    owner=user,
                                                    slug='barbaz',
                                                    description='esta es una descripcion')
        
        self.assertRaises(IntegrityError, Election.objects.create, 
                          name='FooBar', owner=user, slug='barbaz', description='whatever')


class ElectionDetailViewTest(TestCase):
    def test_detail_existing_election_view(self):
        user = User.objects.create(username='foobar')
        user2 = User.objects.create(username='foobar2')
        election = Election.objects.create(name='elec foo', slug='elec-foo', owner=user)
        election2 = Election.objects.create(name='elec foo', slug='elec-foo', owner=user2)
        response = self.client.get(reverse('election_detail', 
                                           kwargs={
                                               'username': user.username, 
                                               'slug': election.slug}))
        self.assertEquals(response.status_code, 200)
        self.assertTrue('election' in response.context)
        self.assertEquals(response.context['election'], election)

    def test_detail_non_existing_election_view(self):
        user = User.objects.create(username='foobar')
        election = Election.objects.create(name='elec foo', slug='elec-foo', owner=user)
        response = self.client.get(reverse('election_detail', 
                                           kwargs={
                                               'username': user.username, 
                                               'slug': 'asd-asd'}))
        self.assertEquals(response.status_code, 404)

    def test_detail_non_existing_election_for_user_view(self):
        user = User.objects.create(username='foobar')
        user2 = User.objects.create(username='barbaz')
        election = Election.objects.create(name='elec foo', slug='elec-foo', owner=user2)
        response = self.client.get(reverse('election_detail', 
                                           kwargs={
                                               'username': user.username, 
                                               'slug': election.slug}))
        self.assertEquals(response.status_code, 404)


class ElectionCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='joe', password='doe', email='joe@doe.cl')
        
    def test_create_election_by_user_without_login(self):
        user = self.user
        
        request = self.client.get(reverse('election_create'))
        
        self.assertEquals(request.status_code, 302)

    def test_create_election_by_user_success(self):
        user = self.user

        self.client.login(username='joe', password='doe')
        request = self.client.get(reverse('election_create'))

        self.assertTrue(request.context.has_key('form'))
        self.assertTrue(isinstance(request.context['form'], ElectionForm))

    def test_post_election_create_with_same_slug(self):
        election = Election.objects.create(name='BarBaz1', slug='barbaz', description='whatever', owner=self.user)

        self.client.login(username='joe', password='doe')
        params = {'name': 'BarBaz', 'slug': 'barbaz', 'description': 'esta es una descripcion'}
        response = self.client.post(reverse('election_create'), params)
        
        self.assertEquals(response.status_code, 200)
   
    def test_post_election_create_without_login(self):
        params = {'name': 'BarBaz', 'slug': 'barbaz', 'description': 'esta es una descripcion'}
        response = self.client.post(reverse('election_create'), params)
        
        self.assertEquals(response.status_code, 302)

    def test_post_election_create_logged(self):
        self.client.login(username='joe', password='doe')
        params = {'name': 'BarBaz', 'slug': 'barbaz', 'description': 'esta es una descripcion'}
        response = self.client.post(reverse('election_create'), params, follow=True)

        self.assertEquals(response.status_code, 200)
        qs = Election.objects.filter(name='BarBaz')
        self.assertEquals(qs.count(), 1)
        election = qs.get()
        self.assertEquals(election.name, 'BarBaz')
        self.assertEquals(election.slug, 'barbaz')
        self.assertEquals(election.description, 'esta es una descripcion')
        self.assertEquals(election.owner, self.user)
        self.assertRedirects(response, reverse('candidate_create',
                                               kwargs={'slug': election.slug}))
        

class ElectionUrlsTest(TestCase):
    def test_create_url(self):
        expected = '/election/create'
        result = reverse('election_create')
        self.assertEquals(result, expected)

    def test_detail_url(self):
        expected = '/juanito/eleccion-la-florida'
        result = reverse('election_detail', kwargs={'username': 'juanito', 'slug': 'eleccion-la-florida'})
        self.assertEquals(result, expected)