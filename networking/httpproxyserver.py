#!/usr/bin/env python
#
# AUTHOR
#    Caleb Madrigal
#
# DATE CREATED:
#    9/25/2011
#
# DATE MODIFIED:
#    10/1/2011
#
# DESCRIPTION
#    Transparent HTTP proxy with hooks for doing stream manipulation. There are a few subclasses
#    included to do things like flip all images, change text, and replace images with a 
#    specified one. To use, you have to do a MITM attack and use something like iptables to direct
#    traffic into it.
#
# NOTES:
#    TODO: HTTP 2.0
#    TODO: POST body
#    TODO: Exception handling (particularly on connection refused)
#    TODO: Decode before modifying if necessary and change headers accordingly

import BaseHTTPServer
import struct
import httplib
from urllib2 import urlopen
from socket import *

import mimetypes
import Image
import PIL.ImageOps

""" HTTP Proxy with hooks for manipulation

To use, extend ProxyHandler and override manipulate_response and/or manipulate_request in order to modify HTTP traffic.

"""

############################################ METADATA
__all__ = ["ProxyHandler"]
__author__ = "Caleb Madrigal"
__version = "1.0.0"

############################################ GLOBALS

HOST = ""
PORT = 8888
ORIGINAL_PORT = 80

log_file = open("http_proxy.log", "w")

class ProxyHandler(BaseHTTPServer.BaseHTTPRequestHandler):

   """ Override and hook into manipulate_request and/or manipulate_response. """

   def do_HEAD(self):
      self.send_response(200)
      self.send_header("Content-type", "text/html")
      self.end_headers()

   def do_GET(self):
      try:
         # Get original request IP and send original request to it
         original_ip = self.get_original_ip(self.request)
   
         # Call modification function for request
         (m_ip, m_port, m_command, m_path, m_body, m_headers) = self.manipulate_request(
                                                           original_ip,
                                                           ORIGINAL_PORT,
                                                           self.command,
                                                           self.path,
                                                           None,
                                                           self.headers.dict)
   
         print "Doing request: ip=[%s], port=[%s], path=[%s]" % (m_ip, m_port, m_path)
   
         original_host_conn = httplib.HTTPConnection(m_ip, m_port)
         # Request HTTP/1.0 so we don't have to handle with chunking and stuff for now :)
         original_host_conn._http_vsn = 10
         original_host_conn._http_vsn_str = "HTTP/1.0"
         original_host_conn.request(m_command, m_path, m_body, m_headers)
   
         # Read the response from the original destination
         response = original_host_conn.getresponse()
         response_status = response.status
         response_headers = response.getheaders()
         response_data = response.read()
   
         # Call manipulation functions
         (mod_status, mod_headers, mod_data) = self.manipulate_response(
                                                  response_status,
                                                  response_headers,
                                                  response_data)
   
         # Send status code (e.g. 200, 404)
         self.send_response(mod_status)
   
         # Send headers from original destination
         for header in mod_headers:
            self.send_header(header[0], header[1])
         self.end_headers()
   
         # Send response from original destination
         self.wfile.write(mod_data)
      except KeyboardInterrupt, e: #Exception, e:
         print "Error in get: %s" % str(e)

   def do_POST(self):
      self.do_GET(self)

   def manipulate_request(self, o_ip, o_port, o_command, o_path, o_body, o_headers):
      """ Function to be overridden in order to manipulate the HTTP request

      This function returns the same set of data as it takes as input.  So there are
      5 parameters that come into this function and this function must return a 5-tuple
      in the same order.  This tuple consist of the following pieces of data:
         * Server ip (e.g. "127.0.0.1")
         * Command (e.g. "GET")
         * Request path (e.g. "/index.php?name=CalebMadrigal")
         * POST body (this is only used for a post)
         * HTTP headers as a dictionary (e.g. {"Content-type":"text/html"}) 

      By default, don't modify anything.  This is just a holding place which should be
      overridden in order to manipulate the HTTP request before passing it to the 
      original destination.
      """

      return (o_ip, o_port, o_command, o_path, o_body, o_headers)

   def manipulate_response(self, o_status, o_headers, o_data):
      """ Function to be overridden in order to manipulate the HTTP response

      This function returns the same set of data as it takes as input.  So there are
      5 parameters that come into this function and this function must return a 5-tuple
      in the same order.  This tuple consist of the following pieces of data:
         * HTTP Status code as an integer (e.g. 200)
         * HTTP headers as a tuple (e.g. {"Content-type": "text/html"})
         * Data - this is the content of the response

      By default, don't modify anything.  This is just a holding place which should be
      overridden in order to manipulate the HTTP response before sending it back to the client.
      """

      return (o_status, o_headers, o_data)

   def get_original_ip(self, sock):
      sockaddr_in = sock.getsockopt(SOL_IP, ORIGINAL_PORT, 16)
      svr_port, svr_ip = struct.unpack("!2xH4s8x", sockaddr_in)
      svr_ip = inet_ntoa(svr_ip)
      return svr_ip

class FlipImageHandler(ProxyHandler):
   def content_type_is_image(self, headers_dict):
      return (headers_dict.has_key("content-type") and headers_dict["content-type"].find("image") == 0)

   def get_content_length(self, headers_dict):
      retval = 0
      if headers_dict.has_key("content-length"):
         retval = headers_dict["content-length"]
      return retval

   def get_image_ext(self, headers_dict):
      retval = ""
      if headers_dict.has_key("content-type") and headers_dict["content-type"].find("image") == 0:
         content_type = headers_dict["content-type"]
         start = content_type.find("/")+1
         end = content_type.find(";")
         if end > 0:
            retval = content_type[start:end]
         else:
            retval = content_type[start:]
      return retval

   def adjust_content_length_header(self, headers_dict, new_len):
      if headers_dict.has_key("content-length"):
         headers_dict["content-length"] = new_len

   def is_img(self, path):
      mime = mimetypes.guess_type(path)[0]
      retval = False
      if mime == None or mime.find("image") != 0:
         retval = False
      else:
         retval = True
      return retval

   def flip_image(self, img_data, img_ext):
      flipped_image_data = img_data
      # TODO: Random
      temp_filename = "temp_file." + img_ext
      temp_file = open(temp_filename, "wb")
      temp_file.write(img_data)
      temp_file.close()

      image = Image.open(temp_filename)
      rotated_image = image.rotate(180)
      rotated_image.save(temp_filename)

      modified_img = open(temp_filename, "rb")
      flipped_image_data = modified_img.read()
      modified_img.close()
      return flipped_image_data

   def manipulate_request(self, o_ip, o_port, o_command, o_path, o_body, o_headers):
      m_headers = o_headers
      m_headers["connection"] = "close" # Force new connection per request
      return (o_ip, o_port, o_command, o_path, o_body, m_headers)

   def manipulate_response(self, o_status, o_headers, o_data):
      m_headers = o_headers
      m_data = o_data
      headers_dict = dict(o_headers)
      if self.content_type_is_image(headers_dict) and (self.get_content_length(headers_dict) != 0):
         img_ext = self.get_image_ext(headers_dict)
         m_data = self.flip_image(o_data, img_ext)
         self.adjust_content_length_header(headers_dict, len(m_data))
         m_headers = [(k,v) for k,v in headers_dict.items()]
      return (o_status, m_headers, m_data)

class ReplaceImagesHandler(ProxyHandler):
   def manipulate_request(self, o_ip, o_port, o_command, o_path, o_body, o_headers):
      m_ip = o_ip
      m_port = o_port
      m_path = o_path
      if is_img(o_path):
         m_ip = "127.0.0.1"
         m_port = 8000
         m_path = "/hastin.jpg"
      return (m_ip, m_port, o_command, m_path, o_body, o_headers)

class ModifyTextHandler(ProxyHandler):
   def manipulate_response(self, o_status, o_header, o_data):
      m_data = o_data.replace("This", "DEATH").replace("XKCD", "DEATH2").replace("Archive", "CALEB")
      return (o_status, o_header, m_data)

if __name__ == "__main__":
   httpd = BaseHTTPServer.HTTPServer((HOST, PORT), ModifyTextHandler) #FlipImageHandler)
   try:
      httpd.serve_forever()
   except KeyboardInterrupt:
      pass
   httpd.server_close()
   log_file.close()

