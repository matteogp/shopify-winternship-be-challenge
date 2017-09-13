# Shopify Winternship 2017 Application Backend Challenge
# Matteo Palarchio
# matteo.palarchio@gmail.com

import json, urllib2, sys

#global variables

baseurl = "https://backend-challenge-winter-2017.herokuapp.com/customers.json?page="
invalid_rules = []
customer_list = []

# populate variables for invalid customer data given a customer and a dictonary
#   of validations
def validate_entry (customer, requirements):

  customer_keys = list(customer.keys())
  invalid_rules = []
  for rule in requirements:
    field = list(rule.keys())[0];

    req = False
    #see if field is required
    if 'required' in (rule[field]).keys():
      req = (rule[field])['required']

    if field not in customer_keys or customer[field] is None:
      if (req):
        invalid_rules.append(field)
        continue

    #checking field typing
    input_type = 'null'
    if 'type' in ((rule[field]).keys()):
      input_type = rule[field]['type']

    check_type = None
    if (input_type == 'string'):
      check_type = unicode
    elif (input_type == 'boolean'):
      check_type = bool
    elif (input_type == 'number'):
      check_type = int

    if (check_type!= None and type(customer[field]) is not check_type and customer[field] is not None and   req):
          invalid_rules.append(field)

    #checking field length, if string
    maxlen = sys.maxsize
    minlen = 0

    if (input_type == 'string' and ('length' in (rule[field]).keys())):
      length_req = (rule[field])['length']
      if 'max' in (length_req).keys():
        maxlen = length_req['max']

      if 'min' in (length_req).keys():
        minlen = length_req['min']

      if ((minlen > len(customer[field])) or (maxlen < len(customer[field]))):
        invalid_rules.append(field)

  if (len(invalid_rules) > 0):
    customer = {'id': customer['id'], 'invalid_fields': invalid_rules}
    customer_list.append(customer)

# output JSON of invalid customer data given a page number (1-16) to access
#   from the API
def query_page (x):
  url = baseurl + str(x)
  page = urllib2.urlopen(url)
  response = json.loads(page.read())
  validations = response["validations"]
  customers = response["customers"]

  for entry in customers:
      validate_entry(entry, validations)

  output_dict = {'invalid_customers':None}
  output_dict['invalid_customers']=customer_list
  ##
  print json.dumps(output_dict, indent = 2, separators=(',',':'))


# generates invalid customer data from first page
query_page(1)
