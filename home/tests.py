import json
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch

from home.models import (
    AboutPage,
    BranchPage,
    CommunityPage,
    ContactPage,
    EventPage,
    HomePage,
    MagazinePage,
    MediaPage,
    MusicPage,
    SectionContent,
)


class HomePageTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_signup_page_loads(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_church_content_models_exist(self):
        self.assertTrue(HomePage._meta.label == 'home.HomePage')
        self.assertTrue(AboutPage._meta.label == 'home.AboutPage')
        self.assertTrue(BranchPage._meta.label == 'home.BranchPage')
        self.assertTrue(EventPage._meta.label == 'home.EventPage')
        self.assertTrue(MagazinePage._meta.label == 'home.MagazinePage')
        self.assertTrue(MusicPage._meta.label == 'home.MusicPage')
        self.assertTrue(MediaPage._meta.label == 'home.MediaPage')
        self.assertTrue(CommunityPage._meta.label == 'home.CommunityPage')
        self.assertTrue(ContactPage._meta.label == 'home.ContactPage')

    def test_coming_soon_pages_load(self):
        for slug in ['about', 'events', 'magazine', 'music', 'media', 'community', 'contact', 'search', 'branches']:
            response = self.client.get(reverse(slug))
            self.assertEqual(response.status_code, 200)

    @patch('home.views.urlopen')
    def test_new_songs_page_displays_api_results(self, mocked_urlopen):
        mocked_urlopen.return_value.__enter__.return_value.read.return_value = json.dumps(
            {
                'total': 1,
                'page': 1,
                'pages': 1,
                'songs': [
                    {
                        'slug': 'sample-song',
                        'title_ta': 'தமிழ் பாடல்',
                        'title_en': 'Tamil Paadal',
                        'artist': 'Church Choir',
                        'album': None,
                        'url': 'https://tamilchristianworld.com/songs/sample-song',
                    }
                ],
            }
        ).encode('utf-8')

        response = self.client.get(reverse('new_songs'), {'q': 'paadal'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'தமிழ் பாடல்')
        self.assertContains(response, 'Tamil Paadal')
        self.assertContains(response, 'Church Choir')
        self.assertIn('q=paadal', mocked_urlopen.call_args.args[0].full_url)

    def test_new_songs_music_card_links_to_catalogue(self):
        response = self.client.get(reverse('music'))

        self.assertContains(response, reverse('new_songs'))

    def test_admin_page_is_available(self):
        response = self.client.get('/admin/')
        self.assertIn(response.status_code, [200, 302])

    def test_subheading_content_only_appears_on_its_detail_page(self):
        SectionContent.objects.create(
            main_heading='Community',
            subheading='Sunday School',
            title='Sunday School announcement',
            body='Sunday School content',
        )
        SectionContent.objects.create(
            main_heading='Community',
            subheading='Youth Fellowship',
            title='Youth fellowship announcement',
            body='Youth fellowship content',
        )

        parent_response = self.client.get(reverse('community'))
        detail_url = reverse(
            'subheading_detail',
            kwargs={'main_heading': 'community', 'subheading': 'sunday-school'},
        )
        self.assertContains(parent_response, detail_url)
        self.assertNotContains(parent_response, 'Sunday School announcement')
        self.assertNotContains(parent_response, 'Youth fellowship announcement')

        detail_response = self.client.get(detail_url)
        self.assertContains(detail_response, 'Sunday School announcement')
        self.assertContains(detail_response, 'Sunday School content')
        self.assertNotContains(detail_response, 'Youth fellowship announcement')
