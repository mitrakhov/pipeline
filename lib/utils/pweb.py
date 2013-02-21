import httplib
import urlparse
import os
import filesys
import threading

URL_TRACKER = 'http://pipeline'

def upload(url,filename):
    def encode (file_path, fields=[]):
        BOUNDARY = '----------bundary------'
        CRLF = '\r\n'
        body = []
        # Add the metadata about the upload first
        for key, value in fields:
            body.extend(
              ['--' + BOUNDARY,
               'Content-Disposition: form-data; name="%s"' % key,
               '',
               value,
               ])
        # Now add the file itself
        file_name = os.path.basename(file_path)
        f = open(file_path, 'rb')
        file_content = f.read()
        f.close()
        body.extend(
          ['--' + BOUNDARY,
           'Content-Disposition: form-data; name="file"; filename="%s"'
           % file_name,
           # The upload server determines the mime-type, no need to set it.
           'Content-Type: application/octet-stream',
           '',
           file_content,
           ])
        # Finalize the form body
        body.extend(['--' + BOUNDARY + '--', ''])
        return 'multipart/form-data; boundary=%s' % BOUNDARY, CRLF.join(body)

    if os.path.exists(filename):
        content_type, body = encode(filename)
        headers = { 'Content-Type': content_type }
        u = urlparse.urlparse(url)
        server = httplib.HTTPConnection(u.netloc)
        server.request('POST', u.path, body, headers)
        resp = server.getresponse()
        server.close()

        if resp.status == 201:
            location = resp.getheader('Location', None)
        else :
            #print resp.status, resp.reason
            location = None
            #fl = open('/tmp/resp.html','w')
            #fl.write(resp.read())
            #fl.close()

        return location

def _logger_add_row(body,cmd,status_id,path_file_log):
    t = threading.Thread(target=_logger_add_row, args= (body,cmd,status_id,path_file_log))
    t.start()
    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is main_thread: continue
        t.join()

def logger_add_row(body,cmd,status_id,path_file_log):
    url = URL_TRACKER + '/loggger_add/'
    #url = 'http://127.0.0.1:8080/loggger_add/'
    user = filesys.USERNAME
    host = filesys.HOST
    def encode (fields = []):
        BOUNDARY = '----------bundary------'
        CRLF = '\r\n'
        body = []
        # Add the metadata about the upload first
        for key, value in fields:
            body.extend(
                          ['--' + BOUNDARY,
                           'Content-Disposition: form-data; name="%s"' % key,
                           '',
                           value,
                           ])
        # Finalize the form body
        body.extend(['--' + BOUNDARY + '--', ''])
        return 'multipart/form-data; boundary=%s' % BOUNDARY, CRLF.join(body)
    
    content_type, body = encode([('user',user),('host',host),('body',body),('cmd',cmd),('status_id',status_id),('path_file_log',path_file_log)])
    headers = { 'Content-Type': content_type }
    u = urlparse.urlparse(url)
    server = httplib.HTTPConnection(u.netloc)
    server.request('POST', u.path, body, headers)
    resp = server.getresponse()
    server.close()
    
    if resp.status == 201:
        location = resp.getheader('Location', None)
    else :
        #print resp.status, resp.reason
        location = None   
        #fl = open('/tmp/resp.html','w')
        #fl.write(resp.read())
        #fl.close()
    

#upload('http://127.0.0.1:8080/pic_up/3/4/123/','/mnt/karramba/test_zzz/temp/src/XX01/sh_16.jpg')
#logger_add_row('nazarenko','muzzy','the body of message','the command','1','no path for log')
