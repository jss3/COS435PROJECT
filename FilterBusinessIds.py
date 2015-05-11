import json
__author__ = 'haass'

data_file = open('yelp_academic_dataset_business.json', 'r')
#output_file = open('business_ids.txt', 'w')
set = set()

for line in data_file.readlines():
    jitem = json.loads(line)
    businessId = jitem.get("business_id")
    if "Restaurants" in jitem.get("categories"):
        #output_file.write(businessId + '\n')
        set.add(businessId)

data_file.close()
#output_file.close()
review_output = open("yelp_rest_reviews.json", 'w')
review_file = open("yelp_academic_dataset_review.json", 'r')
for line in review_file.readlines():
    jitem = json.loads(line)
    if jitem.get("business_id") in set:
        review_output.write(line)

review_output.close()


