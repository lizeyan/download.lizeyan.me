import os
import json


HOME = "/home/lizeyan/avail-download"
HOST = "https://download.lizeyan.me"


def application(environ, start_response):
    """
    @param environ: http request
    @param start_response: http response header
    @return body of html document
    """
    path = os.path.realpath(os.path.join(HOME, environ['PATH_INFO']))
    body = b""
    if not os.path.exists(path):
        start_response('200 OK', [('Content-Type', 'text/html')])
        body += json.dumps([])
    elif not os.path.isdir(path):
        if path.endswith((".html", ".htm", ".txt", ".md", ".js", ".css")):
            start_response('200 OK', [('Content-Type', 'text/html')])
        else:
            start_response('200 OK', [('Content-Type', 'application/octet-stream')])
        with open(path, "rb") as target_file:
            body += target_file.read()
    else:
        start_response('200 OK', [('Content-Type', 'text/html')])
        results = []
        for f in os.listdir(path) + [".."]:
            real_path = os.path.join(path, f)
            rel_path = os.path.relpath(real_path, HOME)
            if os.path.isdir(real_path):
                results.append({"name": f, "url": HOST + "/" + rel_path, "type": "dir"})
            else:
                results.append({"name": f, "url": HOST + "/" + rel_path, "type": "file", "size": os.path.getsize(real_path)})
        body += json.dumps(results)
    return [body]
