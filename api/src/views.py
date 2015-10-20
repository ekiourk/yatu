from yatu.utils import make_uri


def moved_permanently_view(url):
    return """
<HTML>
<HEAD>
<TITLE>Moved Permanently</TITLE>
</HEAD>
<BODY BGCOLOR="#FFFFFF" TEXT="#000000">
<H1>Moved Permanently</H1>
The document has moved <A HREF="{url}">here</A>.
</BODY>
</HTML>
""".format(url=url)


def not_found_view():
    return """
<HTML>
<HEAD>
<TITLE>Not Found</TITLE>
</HEAD>
<BODY BGCOLOR="#FFFFFF" TEXT="#000000">
<H1>Not Found</H1>
The document has not found.
</BODY>
</HTML>
"""


def error_500_view(message):
    #TODO: Show message only on debug mode
    return {
        'success': False,
        'short_message': "Internal server error",
        'error_message': message
    }


def not_found_404_view(message):
    return {
        'success': False,
        'short_message': "Not Found",
        'error_message': message
    }


def forbidden_found_403_view(message):
    return {
        'success': False,
        'short_message': "Forbidden",
        'error_message': message
    }


def short_it_success_view(url, sid):
    return {
        'success': True,
        'short_url': make_uri(sid),
        'url': url
    }


def short_it_collision_view(url, sid):
    return {
        'success': False,
        'short_message': "Short URL is not available.",
        'error_message': "The url {} is not available. Try another one.".format(make_uri(sid)),
        'short_url': sid,
        'url': url
    }


def short_url_single_view(short_url):
    return {
        'url': short_url.url,
        'short_url': make_uri(short_url.sid),
        'created': short_url.created_at,
        'clicks': short_url.visited_counter
    }


def short_urls_list_view(short_urls):
    items = []
    for item in short_urls:
        items.append(short_url_single_view(item))
    return {'items': items, 'count': len(items)}
