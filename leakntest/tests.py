from django.test import TestCase
from django.test import Client
from leakntest.models import Entry
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
import time


class BasicTest(TestCase):
    fixtures = ['model.yaml']

    def setUp(self):
        self.filters = ['search_name',
                        'search_mail',
                        'search_password',
                        'search_hashword',
                        'search_website']

    def test_home_to_search(self):
        # GET the form
        c = Client()
        response = c.get('/')
        # retrieve form data as dict
        form = response.context['form']
        data = form.initial

        # manipulate some data
        data['entry'] = 'mario'
        data['search_name'] = True
        data['search_mail'] = True
        data['search_password'] = True
        data['search_hashword'] = True
        data['search_website'] = True

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
                          new_entry.get_all_by_entry('mario', self.filters))

    def test_search_by_entry(self):
        '''
        Vérifie si la méthode get_all_by_entry()
        de la classe Entry renvoie le bon query set composé
        '''
        entry = Entry()
        assertion = list() + list(
            Entry.objects.all().filter(name='Princess-Peach'))
        self.assertEqual(entry.get_all_by_entry('Princess-Peach', self.filters)
                         ['names'],
                         assertion)
        self.assertTrue(len(entry.get_all_by_entry('mario', self.filters)) > 0)

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
        self.assertEqual(str(entry.get_all_by_entry('donkey@kong.com',
                                                    self.filters)
                             ['names'][0]),
                         'donkey@kong.com donkey@kong.com donkey@kong.com ' +
                         'donkey@kong.com donkey@kong.com')
        self.assertEqual(
            entry.get_all_by_name('donkey@kong.com').count(),
            len(entry.get_all_by_entry('donkey@kong.com',
                                       self.filters)['names']))
        self.assertEqual(
            entry.get_all_by_mail('donkey@kong.com').count(),
            len(entry.get_all_by_entry('donkey@kong.com',
                                       self.filters)['mails']))
        self.assertEqual(
            entry.get_all_by_password('donkey@kong.com').count(),
            len(entry.get_all_by_entry('donkey@kong.com',
                                       self.filters)['passwords']))
        self.assertEqual(
            entry.get_all_by_hashword('donkey@kong.com').count(),
            len(entry.get_all_by_entry('donkey@kong.com',
                                       self.filters)['hashwords']))
        self.assertEqual(
            entry.get_all_by_website('donkey@kong.com').count(),
            len(entry.get_all_by_entry('donkey@kong.com',
                                       self.filters)['websites']))

    def test_bad_search(self):
        '''
        Vérifie si la méthode get_all_by_website()
        de la classe Entry renvoie le bon query set
        '''
        entry = Entry()

        self.assertFalse(entry.get_all_by_website('www.apple.com').count() > 0)


class MySeleniumTests(StaticLiveServerTestCase):
    fixtures = ['model.yaml']

    @classmethod
    def setUpClass(cls):
        super(MySeleniumTests, cls).setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(MySeleniumTests, cls).tearDownClass()

    def test_github_link(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        githubLink = self.selenium.find_element_by_link_text('Github')
        self.assertEqual('Github',
                         githubLink.text)
        self.assertEqual('https://github.com/AmarOk1412/8INF958_pres/',
                         githubLink.get_attribute('href'))

    def test_no_result(self):
        driver = self.selenium
        driver.get(self.live_server_url + '/')
        driver.find_element_by_id('id_entry').clear()
        driver.find_element_by_id('id_entry').send_keys('noresult')
        driver.find_element_by_css_selector('input[type=\"submit\"]').click()
        try:
            time.sleep(1)  # Wait for result
            self.assertEqual('No result found...',
                             driver.find_element_by_css_selector('p').text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))

    def test_search_mario(self):
        driver = self.selenium
        driver.get(self.live_server_url + '/')
        driver.find_element_by_id('id_entry').clear()
        driver.find_element_by_id('id_entry').send_keys('mario')
        driver.find_element_by_css_selector('input[type=\"submit\"]').click()
        try:
            self.assertEqual('Results for: mario',
                             driver.find_element_by_css_selector('h1').text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        try:
            self.assertEqual('As Name:',
                             driver.find_element_by_css_selector('h2').text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        try:
            self.assertEqual('Mail',
                             driver.find_element_by_css_selector('th').text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        try:
            content = '//div[@id=\"results\"]/table/tbody/tr/th[2]'
            self.assertEqual('Password',
                             driver.find_element_by_xpath(content).text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        try:
            content = '//div[@id=\"results\"]/table/tbody/tr/th[3]'
            self.assertEqual('Hashword',
                             driver.find_element_by_xpath(content).text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        try:
            content = '//div[@id=\"results\"]/table/tbody/tr/th[4]'
            self.assertEqual('Website',
                             driver.find_element_by_xpath(content).text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        try:
            self.assertEqual('mario@gmail.com',
                             driver.find_element_by_css_selector('td').text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        try:
            content = '//div[@id=\"results\"]/table/tbody/tr[2]/td[2]'
            self.assertEqual('x_IamTheBest_x666',
                             driver.find_element_by_xpath(content).text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        try:
            content = '//div[@id=\"results\"]/table/tbody/tr[2]/td[3]'
            self.assertEqual('de2f15d014d40b93578d255e6221fd60',
                             driver.find_element_by_xpath(content).text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        try:
            content = '//div[@id=\"results\"]/table/tbody/tr[2]/td[4]'
            self.assertEqual('www.facebook.com',
                             driver.find_element_by_xpath(content).text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))

    def test_search_donkey(self):
        driver = self.selenium
        driver.get(self.live_server_url + '/')
        driver.find_element_by_id('id_entry').clear()
        driver.find_element_by_id('id_entry').send_keys('donkey@kong.com')
        driver.find_element_by_css_selector('input[type=\"submit\"]').click()
        try:
            self.assertEqual('Results for: donkey@kong.com',
                             driver.find_element_by_css_selector('h1').text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        try:
            self.assertEqual('As Name:',
                             driver.find_element_by_css_selector('h2').text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        try:
            self.assertEqual('Mail',
                             driver.find_element_by_css_selector('th').text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        try:
            self.assertEqual('donkey@kong.com',
                             driver.find_element_by_css_selector('td').text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        try:
            content = '//div[@id=\"results\"]/table/tbody/tr/th[2]'
            self.assertEqual('Password',
                             driver.find_element_by_xpath(content).text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        try:
            content = '//div[@id=\"results\"]/table/tbody/tr[2]/td[2]'
            self.assertEqual('donkey@kong.com',
                             driver.find_element_by_xpath(content).text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        try:
            content = '//div[@id=\"results\"]/table/tbody/tr/th[3]'
            self.assertEqual('Hashword',
                             driver.find_element_by_xpath(content).text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        try:
            content = '//div[@id=\"results\"]/table/tbody/tr[2]/td[3]'
            self.assertEqual('donkey@kong.com',
                             driver.find_element_by_xpath(content).text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        try:
            content = '//div[@id=\"results\"]/table/tbody/tr/th[4]'
            self.assertEqual('Website',
                             driver.find_element_by_xpath(content).text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        try:
            content = '//div[@id=\"results\"]/table/tbody/tr[2]/td[4]'
            self.assertEqual('donkey@kong.com',
                             driver.find_element_by_xpath(content).text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        try:
            content = '//div[@id=\"results\"]/h2[2]'
            self.assertEqual('As Mail:',
                             driver.find_element_by_xpath(content).text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        try:
            content = '//div[@id=\"results\"]/h2[3]'
            self.assertEqual('As Password:',
                             driver.find_element_by_xpath(content).text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        try:
            content = '//div[@id=\"results\"]/h2[4]'
            self.assertEqual('As Hash:',
                             driver.find_element_by_xpath(content).text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        try:
            content = '//div[@id=\"results\"]/h2[5]'
            self.assertEqual('As Website:',
                             driver.find_element_by_xpath(content).text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))

    def test_no_checkbox(self):
        driver = self.selenium
        driver.get(self.live_server_url + '/')
        driver.find_element_by_id('id_entry').clear()
        driver.find_element_by_id('id_entry').send_keys('donkey@kong.com')
        driver.find_element_by_id('id_search_name').click()
        driver.find_element_by_id('id_search_mail').click()
        driver.find_element_by_id('id_search_password').click()
        driver.find_element_by_id('id_search_hashword').click()
        driver.find_element_by_id('id_search_website').click()
        driver.find_element_by_css_selector('input[type=\"submit\"]').click()
        try:
            self.assertEqual('No result found...',
                             driver.find_element_by_css_selector('p').text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))

    def test_3_checkboxes(self):
        driver = self.selenium
        driver.get(self.live_server_url + '/')
        driver.find_element_by_id('id_entry').clear()
        driver.find_element_by_id('id_entry').send_keys('donkey@kong.com')
        driver.find_element_by_id('id_search_mail').click()
        driver.find_element_by_id('id_search_hashword').click()
        driver.find_element_by_css_selector('input[type=\"submit\"]').click()
        try:
            self.assertEqual('As Name:',
                             driver.find_element_by_css_selector('h2').text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        try:
            content = '//div[@id="results"]/h2[2]'
            self.assertEqual('As Password:',
                             driver.find_element_by_xpath(content).text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        try:
            content = '//div[@id="results"]/h2[3]'
            self.assertEqual('As Website:',
                             driver.find_element_by_xpath(content).text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))

    def test_2_checkboxes(self):
        driver = self.selenium
        driver.get(self.live_server_url + '/')
        driver.find_element_by_id('id_entry').clear()
        driver.find_element_by_id('id_entry').send_keys('donkey@kong.com')
        driver.find_element_by_id('id_search_name').click()
        driver.find_element_by_id('id_search_password').click()
        driver.find_element_by_id('id_search_website').click()
        driver.find_element_by_css_selector('input[type=\"submit\"]').click()
        try:
            self.assertEqual('As Mail:',
                             driver.find_element_by_css_selector('h2').text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))
        try:
            content = '//div[@id="results"]/h2[2]'
            self.assertEqual('As Hash:',
                             driver.find_element_by_xpath(content).text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))
