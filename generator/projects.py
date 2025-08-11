import random
import string
from comtypes.client import CreateObject
import os
import getopt
import sys

try:
    opts, args = getopt.getopt(sys.argv[1:], "n:f:", ["number of projects", "file"])
except getopt.GetoptError as err:
    print(err)
    getopt.usage()
    sys.exit(2)

n = 5
f = "data/projects.xlsx"

for o, a in opts:
    if o == "-n":
        n = int(a)
    elif o == "-f":
        f = a

project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits  + " "*10
    return (prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])).strip()

xl = CreateObject("Excel.Application")
xl.Visible = 1
wb = xl.Workbooks.Add()
list_status = [str(10), str(30), str(50), str(70)]
for i in range(n):
    xl.Range["A%s" % (i+1)].Value[()] = random_string("name", 10)
for j in range(n):
    xl.Range["B%s" % (j + 1)].Value[()] = random.choice(list_status)
for k in range(n):
    xl.Range["C%s" % (k + 1)].Value[()] = random_string("description", 20)
if os.path.exists(os.path.join(project_dir, f)) == True:
    os.remove(os.path.join(project_dir, f))
wb.SaveAs(os.path.join(project_dir, f))
xl.Quit()