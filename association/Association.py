# coding: utf-8

# In[1]:

import Orange
import string
print "The following is the list of games"
print "Dota 2"
#print "\n "
print "Fifa"
#print "\n "
print  "cs"
#print "\n "
print "MW3"
#print "\n "
print "ghost reccon "
#print "\n "
print "nfs"


var = raw_input("Please enter from the above mentioned list: ")
#print "you entered", var





raw_data = ["Fifa, Dota 2, cs",
            "Dota 2, MW3, reccon",
            "Fifa, ghost reccon",
            "Fifa, Dota 2, MW3",
            "Fifa, cs, ghost reccon",
            "Dota 2, cs",
            "ghost reccon,Fifa, MW3,nfs"]
raw_data.append(var)

print raw_data

# write data to the text file: data.basket
f = open('data.basket', 'w')
for item in raw_data:
    f.write(item + '\n')
f.close()

# Load data from the text file: data.basket
data = Orange.data.Table("data.basket")


# Identify association rules with supports at least 0.3
rules = Orange.associate.AssociationRulesSparseInducer(data, support = 0.2)


# print out rules
#print "%4s %4s  %s" % ("Supp", "Conf", "Rule")
#for r in rules[:]:
 #   print "%4.1f %4.1f  %s" % (r.support, r.confidence, r)

rule = rules[0]
maximum = 0.1
for idx, d in enumerate(data):
    if idx is 7:
        print '\nYour Entered Choice are {0}'.format(raw_data[idx])
        for r in rules:
            if r.applies_left(d) and not r.applies_right(d):
                if r.confidence > maximum:
                    printing_str = r
                    maximum = r.confidence

string_1= str(printing_str)
print "\n"
print "The following games is the next best game you should be playing"
print string_1.split("->",1)[1]