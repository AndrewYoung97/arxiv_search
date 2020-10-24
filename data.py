import csv
import glob
from nltk.tokenize import sent_tokenize
import nltk
import datetime

i = 0
print(len(glob.glob("data/per_category/physics.*.tsv")))
# for file in glob.glob("data/per_category/physics.*"):
#     # if not file.endswith("xz"):
#     i += 1
#     print(file)
# print(i)
# i = 0
# nltk.download('punkt')
# p= "I am Dr. Chen, you are my sister. Thank you."
# print(sent_tokenize(p))
# with open("data/per_category/physics.*.tsv",  encoding="utf-8") as f:
#     rd = csv.reader(f, delimiter="\t")
#     for doc in rd:
#         print(doc[7])
#         break
#         time = datetime.datetime(*map(int, doc[7].split('-')))
#         for idk, sen in enumerate(sent_tokenize(doc[1])):
#             print(sen)
print(i)