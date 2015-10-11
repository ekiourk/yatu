
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
