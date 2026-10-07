import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.text import slugify

from .models import SectionContent


SECTION_PAGE_NAMES = {
    'About': 'about',
    'Branches': 'branches',
    'Events': 'events',
    'Community': 'community',
    'Music': 'music',
    'Media': 'media',
    'Magazine': 'magazine',
    'Contact': 'contact',
}


def index(request):
    return render(request, 'home/home.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'home/signup.html', {'form': form})


def render_section_page(request, title, subtitle, items):
    for item in items:
        item.setdefault(
            'detail_url',
            reverse(
                'subheading_detail',
                kwargs={
                    'main_heading': slugify(title),
                    'subheading': slugify(item['title']),
                },
            ),
        )

    return render(
        request,
        'home/section_page.html',
        {'page_title': title, 'page_subtitle': subtitle, 'items': items},
    )


def subheading_detail(request, main_heading, subheading):
    heading_and_subheading = next(
        (
            (heading, item)
            for heading, subheadings in SectionContent.SUBHEADING_GROUPS
            for item in subheadings
            if slugify(heading) == main_heading and slugify(item) == subheading
        ),
        None,
    )
    if heading_and_subheading is None:
        raise Http404

    heading, subheading_title = heading_and_subheading
    content_items = SectionContent.objects.filter(
        main_heading=heading,
        subheading=subheading_title,
        is_published=True,
    ).order_by('-created_at')
    return render(
        request,
        'home/subheading_detail.html',
        {
            'main_heading': heading,
            'subheading_title': subheading_title,
            'content_items': content_items,
            'parent_url': reverse(SECTION_PAGE_NAMES[heading]),
        },
    )


def about(request):
    items = [
        {
            'title': 'About Church',
            'summary': 'A brief introduction to the church and its spiritual identity.',
            'detail': 'This section presents the church introduction and its mission among the congregation.',
        },
        {
            'title': 'Church History',
            'summary': 'A look at the journey, foundation, and growth of the church.',
            'detail': 'This page highlights the historical background of the church and its continuing testimony.',
        },
        {
            'title': 'Branches',
            'summary': 'Locations and fellowship communities connected to the church.',
            'detail': 'View the church branches and their places of worship.',
            'link': 'branches',
            'link_label': 'View branches',
        },
    ]
    return render_section_page(request, 'About', 'Church identity and history', items)


def branches(request):
    branches_list = [
        {
            'title': 'CSI Christ Church, Kambenery',
            'summary': 'Branch fellowship and worship community.',
        },
        {
            'title': 'CSI Christ Church, Sundarapandiyapuram',
            'summary': 'Branch fellowship and worship community.',
        },
        {
            'title': 'CSI Rhenius Memorial Church, Bharathi Nagar',
            'summary': 'Branch fellowship and worship community.',
        },
        {
            'title': 'CSI Christ Church, Poigai-Kovilaandanoor',
            'summary': 'Branch fellowship and worship community.',
        },
    ]
    return render_section_page(request, 'Branches', 'Church branches and locations', branches_list)


def events(request):
    items = [
        {'title': 'Upcoming Events', 'summary': 'Church gatherings and upcoming activities.', 'detail': 'Information about upcoming church events and fellowship opportunities.'},
        {'title': 'Church Activities', 'summary': 'Regular church activities for worship and service.', 'detail': 'A schedule of church activities and service opportunities.'},
        {'title': 'Important Events', 'summary': 'Special church occasions and important dates.', 'detail': 'Key church events and notable celebration dates.'},
        {'title': 'Special Festivals', 'summary': 'Festival worship and seasonal celebration times.', 'detail': 'Festival occasions and special gathering times.'},
        {'title': 'Prayer Meetings', 'summary': 'Dedicated times for prayer and worship.', 'detail': 'Prayer gatherings and intercession opportunities.'},
        {'title': 'Camps', 'summary': 'Spiritual camps and outdoor fellowship experiences.', 'detail': 'Camp opportunities for youth, families, and church groups.'},
        {'title': 'Retreats', 'summary': 'Quiet times of reflection, worship, and renewal.', 'detail': 'Retreat events for spiritual renewal and encouragement.'},
        {'title': 'Missionaries Place Travel', 'summary': 'Mission and outreach travel opportunities.', 'detail': 'Missionary travel and outreach journeys connected with the church.'},
    ]
    return render_section_page(request, 'Events', 'Upcoming church events and gatherings', items)


def community(request):
    items = [
        {'title': 'Sunday School', 'summary': 'Bible teaching and spiritual growth for children and families.', 'detail': 'A growing teaching ministry for children and families.'},
        {'title': 'Youth Fellowship', 'summary': 'Youth fellowship, prayer, and discipleship.', 'detail': 'An active youth fellowship for spiritual growth and community.'},
        {'title': 'Women\'s Fellowship', 'summary': 'Women’s prayer, fellowship, and encouragement.', 'detail': 'A supportive women’s ministry with prayer and sharing.'},
        {'title': 'Men\'s Fellowship', 'summary': 'Men’s fellowship and discipleship.', 'detail': 'A space for men to grow in faith, prayer, and responsibility.'},
    ]
    return render_section_page(request, 'Community', 'Church fellowship and discipleship ministries', items)


def music(request):
    items = [
        {'title': 'Keerthanai Songs', 'summary': 'Traditional devotional songs and worship songs.', 'detail': 'A collection of devotional songs and spiritual worship music.'},
        {'title': 'K.V. Songs', 'summary': 'K.V. song selections and worship music.', 'detail': 'Music resources and song collections connected to church worship.'},
        {'title': 'New Songs', 'summary': 'Browse and search the Tamil Christian song catalogue.', 'detail': 'Tamil song titles and English transliterations from the TCW collection.', 'detail_url': reverse('new_songs')},
        {'title': 'Music Training', 'summary': 'Training and development in worship music.', 'detail': 'Guidance and preparation for church music ministry and worship leadership.'},
    ]
    return render_section_page(request, 'Music', 'Worship songs and music resources', items)


def new_songs(request):
    query = request.GET.get('q', '').strip()[:120]
    try:
        page = max(1, int(request.GET.get('page', '1')))
    except (TypeError, ValueError):
        page = 1

    params = {'page': page, 'limit': 24}
    if query:
        params['q'] = query

    api_url = f"https://tamilchristianworld.com/api/v1/songs?{urlencode(params)}"
    songs = []
    total = 0
    pages = 1
    error = None

    try:
        api_request = Request(api_url, headers={'User-Agent': 'NPT-Grace-Fellowship-Website/1.0'})
        with urlopen(api_request, timeout=8) as response:
            payload = json.loads(response.read().decode('utf-8'))
        songs = payload.get('songs', [])
        total = payload.get('total', 0)
        pages = max(1, payload.get('pages', 1))
    except (HTTPError, URLError, TimeoutError, UnicodeDecodeError, json.JSONDecodeError, AttributeError, TypeError, ValueError):
        error = 'The song catalogue is temporarily unavailable. Please try again shortly.'

    return render(
        request,
        'home/song_catalog.html',
        {
            'query': query,
            'songs': songs,
            'total': total,
            'page': page,
            'pages': pages,
            'previous_page': page - 1,
            'next_page': page + 1,
            'has_previous': page > 1,
            'has_next': page < pages,
            'error': error,
            'parent_url': reverse('music'),
        },
    )


def media(request):
    items = [
        {'title': 'Short Videos', 'summary': 'Short message and worship videos.', 'detail': 'Short video clips for prayer, worship, and encouragement.'},
        {'title': 'Long Videos', 'summary': 'Extended teaching and worship sessions.', 'detail': 'Longer video content from church messages and meetings.'},
        {'title': 'Live', 'summary': 'Live worship and live church service content.', 'detail': 'Live streamed or live worship content for the church community.'},
    ]
    return render_section_page(request, 'Media', 'Videos and church media content', items)


def magazine(request):
    items = [
        {'title': 'Magazine Issue', 'summary': 'Current issue and church magazine editions.', 'detail': 'Magazine issues with church stories, teachings, and updates.'},
        {'title': 'Magazine Article', 'summary': 'Articles, reflections, and church teachings.', 'detail': 'Magazine articles covering sermons, stories, and inspirational messages.'},
        {'title': 'Bible Verse', 'summary': 'Scripture reflections and daily encouragement.', 'detail': 'Bible verses and devotional reflections for the church family.'},
        {'title': 'Magazine Photo', 'summary': 'Photo features from the church and community life.', 'detail': 'Photo highlights from worship, ministries, and church moments.'},
    ]
    return render_section_page(request, 'Magazine', 'Church magazine content and inspirations', items)


def contact(request):
    items = [
        {'title': 'Contact', 'summary': 'Reach the church office and fellowship team.', 'detail': 'Use this section for church contact information, inquiries, and communication.'},
        {'title': 'Prayer Requests', 'summary': 'Share prayer needs with the church community.', 'detail': 'A place for prayer requests and pastoral support.'},
        {'title': 'Visit the Church', 'summary': 'Information about worship and fellowship visits.', 'detail': 'Details for those visiting the church and planning a visit.'},
    ]
    return render_section_page(request, 'Contact', 'Get in touch with the church', items)


def coming_soon(request, page_name='page'):
    return render(request, 'home/coming_soon.html', {'page_name': page_name})
