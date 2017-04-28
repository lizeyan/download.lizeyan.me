import os


HOME = "/home/lizeyan/avail-download"
CONTENT_TEMPLATE = """
<html>
    <head>
    <title>Download</title>
    <link rel="stylesheet" href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
    <style>
    body {
        font-family: "Microsoft Yahei UI", serif;
    }
    .center-inner-control {
        max-width: 1024px;
        margin-left: auto;
        margin-right: auto;
    }
    </style>
    </head>
    <body>
    <div class=\"page-header text-center\">
    <h1> Welcome to <a href="#">download.lizeyan.me</a></h1>
    </div>
        %s
    <script src="//cdn.bootcss.com/jquery/3.1.1/jquery.min.js"></script>
    <script src="https://cdn.bootcss.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
    </body>
</html>
"""


def application(environ, start_response):
    """
    @param environ: http request
    @param start_response: http response header
    @return body of html document
    """
    path = os.path.realpath(os.path.join(HOME, environ['PATH_INFO'].lstrip('/')))
    body = b""
    if not os.path.exists(path):
        start_response('200 OK', [('Content-Type', 'text/html')])
        body += (CONTENT_TEMPLATE % ("<h1>Path %s is not accessible.</h1>" % path)).encode("utf-8")
    elif not os.path.isdir(path):
        if path.endswith((".html", ".htm", ".txt", ".md")):
            start_response('200 OK', [('Content-Type', 'text/html')])
        else:
            start_response('200 OK', [('Content-Type', 'application/octet-stream')])
        with open(path, "rb") as target_file:
            body += target_file.read()
    else:
        start_response('200 OK', [('Content-Type', 'text/html')])
        body += (CONTENT_TEMPLATE % generate(path, root=True)).encode("utf-8")
    return [body]


def generate(path, root=False, depth=0):
    """
    @param path: absolute path to root
    @return string of html tag
    """
    rst = "<ul class=\"list-group collapse text-left center-inner-control %s\" id=\"%s\">" % ("in" if root else "", path.replace('/', '_'))
    for entry in os.listdir(path):
        if entry.startswith("."):
            continue
        if root and entry == "wsgi.py":
            continue
        f_abs = os.path.join(path, entry)
        if os.path.isdir(f_abs):
            f_id = f_abs.replace("/", "_")
            rst += "<li class=\"list-group-item\"><button class=\"btn btn-info\" data-toggle=\"collapse\" data-target=\"#%s\" aria-expanded=\"true\" aria-controls=\"%s\">%s</button>" % (f_id, f_id, entry)
            rst += generate(f_abs, depth=depth+1)
            rst += "</li>"
        else:
            rst += "<li class=\"inline list-group-item\">%s<a href=\"/%s\"><button class=\"btn btn-success\">%s</button></li></a>" % ("<span class=\"glyphicon glyphicon-arrow-right\"><span>" * depth, os.path.relpath(f_abs, HOME), entry)
    rst += "</ul>"
    return rst
