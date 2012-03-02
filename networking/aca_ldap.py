#!/usr/bin/env python
#
# AUTHOR
#    Caleb Madrigal
#
# DESCRIPTION
#    This is just a program I used to retrieve the emails of my coworkers via an LDAP server.
#    Obviously, the server, user, and password information must be set.

import ldap
import re
import sys

LDAP_USER = 'theuser'
LDAP_PASS = 'thepassword'
LDAP_SERVER = "thedomain.com"
LDAP_BASE = "dc=subdomain,dc=thedomain,dc=com"
LDAP_FIELDS = ['givenName','sn','displayName', 'telephoneNumber', 'mail', 'sAMAccountName', 'department', 'physicalDeliveryOfficeName','description']

def open_ldap(server, user, pw):
   ld = ldap.open(LDAP_SERVER)
   ld.set_option(ldap.OPT_REFERRALS,0)
   ld.simple_bind_s(LDAP_USER+"@thedomain.com", LDAP_PASS)
   return ld

def query_ldap(ld, query):
   try:
      result_id = ld.search(LDAP_BASE, ldap.SCOPE_SUBTREE, query, None)
   except ldap.LDAPError:
      return "LDAP search failed"

   result_set = []

   while 1:
      try:
         result_type, result_data = ld.result(result_id, 0)
      except ldap.LDAPError:
         return "LDAP search failed"
      if result_data == []:
         break
      else:
         if result_type == ldap.RES_SEARCH_ENTRY:
            result_set.append(result_data)

   ldap_results = []
   if result_set:
      for entry in result_set:
         result_dict = {}
         for field in LDAP_FIELDS:
            try:
               result_dict[field] = entry[0][1][field][0]
            except KeyError:
               result_dict[field] = 'not available'

         ldap_results.append(result_dict)

   return ldap_results

def query_user_by_name(ld, name):
   filter = "(&(objectClass=user)(cn=*%s*))" % name
   return query_ldap(ld, filter)

def print_users(user_list):
   for person in ldap_results:
      print "%-32s%-40s%-12s" % (person['displayName'], person['mail'], person['telephoneNumber'])

if __name__ == "__main__":
   try:
      name = sys.argv[1]
   except:
      print "usage: aca_ldap.py <name of user (first and/or last)>"
      sys.exit(1)

   ld = open_ldap(LDAP_SERVER, LDAP_USER, LDAP_PASS)
   ldap_results = query_user_by_name(ld, name)
   print_users(ldap_results)
