import urllib, sys, re
from lxml import etree
from collections import defaultdict
import json
import csv
'''
Crawls ABA API for projection connectivity btw 2 brain regions
- iterates over all ABA brain region names
  - fetches ABA API for connectivity, using above as 'target_domain' (and 'root' as 'injection_domain')
  - for each experiment (<object>)
    - for each <injection-structure>
      - print its <id>, and the experiment's '<sum>'

API documentation:
http://help.brain-map.org/display/api/Connected+Services+and+Pipes#ConnectedServicesandPipes-service%3A%3Amouseconnectivityinjectionstructure

@author renaud.richardet@epfl.ch 20131125
'''

API="http://api.brain-map.org/api/v2/data/query.xml?criteria=service::mouse_connectivity_injection_structure[injection_domain$eqroot][target_domain$eq{}]"

counts = defaultdict(lambda : defaultdict(int))
sums = defaultdict(lambda : defaultdict(int))

def crawl(br_target):
    try:
        murl = API.format(br_target)
        print murl
        tree = etree.parse(urllib.urlopen(murl))
        #print etree.tostring(tree)

        result_cnt = tree.getroot().get('num_rows')
        #total_result_cnt = tree.getroot().get('total_rows')
        print "result_cnt "+result_cnt

        for obj in tree.xpath('/Response/objects/object'):
            id = obj.xpath('id')[0].text
            #print "experiment " + id

            sum = float(obj.xpath('sum')[0].text)
            #print " sum " + sum

            for injection in obj.xpath('injection-structures/injection-structure'):
                id = injection.xpath('id')[0].text #
                print "{}\t{}\t{}".format(id, br_target, sum)
                #counts[id][br_target] += 1
                #sums[id][br_target] += sum

    except Exception, e:
        print 'error with {}'.format(br_target)

def crawl_aba():
    ONTO = "/Users/richarde/Desktop/BBP_experiments/23_extract_brainregions/ABA/mouse_regions.tsv"

    with open(ONTO) as tsv:
        next(tsv) # skip one line
        next(tsv) # skip root
        for line in csv.reader(tsv, delimiter='\t'):
            id=line[0]
            #print id
            crawl(id)


# def write_results():
#     json.dump(counts, open("counts.json",'w'))
#     json.dump(sums, open("sums.json",'w'))



crawl_aba()

#crawl('LGd')
#write_results()
#crawl('LGd')
#crawl('Isocortex')
