# Answer: ? (Got help).
import xmlrpclib
phonebook = xmlrpclib.ServerProxy('http://www.pythonchallenge.com/pc/phonebook.php')
print phonebook.system.listMethods()

