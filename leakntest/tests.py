from django.test import TestCase
from django.test import Client
from leakntest.models import Entry

# Create your tests here.


class BasicTest(TestCase):

    fixtures = ['model.yaml']

    def setUp(self):
        pass

    def test_home_to_search(self):
        # GET the form
        c = Client()
        response = c.get('/')
        # retrieve form data as dict
        form = response.context['form']
        data = form.initial

        # manipulate some data
        data['entry'] = 'mario'

        # POST to the form
        response = self.client.post('/', data)

        ''' Vérifie si après la redirection l'URL ajoutée
            est bien dans la liste '''
        data = {
            'entry': '[<Entry: mario mario@gmail.com x_IamTheBest_x666' +
            ' de2f15d014d40b93578d255e6221fd60 www.facebook.com>,' +
            ' <Entry: mario mario@gmail.com x_IamTheBest_x666' +
            ' de2f15d014d40b93578d255e6221fd60 www.twitter.com>,' +
            ' <Entry: mario mario@gmail.com x_IamTheBest_x666' +
            ' de2f15d014d40b93578d255e6221fd60 www.amazon.com>,' +
            ' <Entry: mario mario@gmail.com IhateLuigi' +
            ' cf8b39a97771ade35fae64a2fc53893b www.twitter.com>]',
        }
        new_entry = Entry()

        self.assertContains(response, 'mario')
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.context['entry'],
                          new_entry.get_all_by_entry('mario'))

    def test_search_by_entry(self):
        '''
        Vérifie si la méthode get_all_by_entry()
        de la classe Entry renvoie le bon query set composé
        '''
        entry = Entry()
        assertion = list() + list(
            Entry.objects.all().filter(name='Princess-Peach'))
        self.assertEqual(entry.get_all_by_entry('Princess-Peach')['names'],
                         assertion)
        self.assertTrue(len(entry.get_all_by_entry('mario')) > 0)

    def test_search_by_name(self):
        '''
        Vérifie si la méthode get_all_by_name()
        de la classe Entry renvoie le bon query set
        '''
        entry = Entry()

        self.assertEqual(entry.get_all_by_name('mario')[0].name, 'mario')
        self.assertEqual(entry.get_all_by_name('mario').count(), 4)

    def test_search_by_mail(self):
        '''
        Vérifie si la méthode get_all_by_mail()
        de la classe Entry renvoie le bon query set
        '''
        entry = Entry()

        self.assertEqual(
            entry.get_all_by_mail('mario@gmail.com')[0].name, 'mario')
        self.assertEqual(
            entry.get_all_by_mail('mario@gmail.com').count(), 5)

    def test_search_by_password(self):
        '''
        Vérifie si la méthode get_all_by_password()
        de la classe Entry renvoie le bon query set
        '''
        entry = Entry()

        self.assertEqual(
            entry.get_all_by_password('x_IamTheBest_x666')[0].name, 'mario')
        self.assertEqual(
            entry.get_all_by_password('x_IamTheBest_x666').count(), 3)

    def test_search_by_hashword(self):
        '''
        Vérifie si la méthode get_all_by_hashword()
        de la classe Entry renvoie le bon query set
        '''
        entry = Entry()

        self.assertEqual(
            entry.get_all_by_hashword('de2f15d014d40b93578d255e6221fd60')[0]
            .name, 'mario')
        self.assertEqual(
            entry.get_all_by_hashword('de2f15d014d40b93578d255e6221fd60')
            .count(), 3)

    def test_search_by_website(self):
        '''
        Vérifie si la méthode get_all_by_website()
        de la classe Entry renvoie le bon query set
        '''
        entry = Entry()

        self.assertEqual(
            entry.get_all_by_website('www.facebook.com')[0].name, 'mario')
        self.assertEqual(
            entry.get_all_by_website('www.facebook.com').count(), 2)

    def test_search_by_similarities(self):
        '''
        Vérifie si la méthode get_all_* récupère correctement le bon nombre
        d'Entry
        '''
        entry = Entry()
        self.assertEqual(
            entry.get_all_by_name('donkey@kong.com').count(),
            len(entry.get_all_by_entry('donkey@kong.com')['names']))
        self.assertEqual(
            entry.get_all_by_mail('donkey@kong.com').count(),
            len(entry.get_all_by_entry('donkey@kong.com')['mails']))
        self.assertEqual(
            entry.get_all_by_password('donkey@kong.com').count(),
            len(entry.get_all_by_entry('donkey@kong.com')['passwords']))
        self.assertEqual(
            entry.get_all_by_hashword('donkey@kong.com').count(),
            len(entry.get_all_by_entry('donkey@kong.com')['hashwords']))
        self.assertEqual(
            entry.get_all_by_website('donkey@kong.com').count(),
            len(entry.get_all_by_entry('donkey@kong.com')['websites']))

    def test_bad_search(self):
        '''
        Vérifie si la méthode get_all_by_website()
        de la classe Entry renvoie le bon query set
        '''
        entry = Entry()

        self.assertFalse(entry.get_all_by_website('www.apple.com').count() > 0)
