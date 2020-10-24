import os
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT
import glob
import csv


schema = Schema(title=TEXT(stored=True), author=TEXT(stored=True), abstract=TEXT(stored=True))

if not os.path.exists("index"):
    os.mkdir("index")

# ix = create_in("index", schema, indexname="cs")
# ix = create_in("index", schema, indexname="math")
# ix = create_in("index", schema, indexname="physics")

# ix = open_dir("index", indexname="math")
# writer = ix.writer()
#
# for file in glob.glob("data/per_category/math.*.tsv"):
#     with open(file, 'r', encoding="utf-8") as f:
#         rd = csv.reader(f, delimiter="\t")
#         for doc in rd:
#             writer.add_document(title=doc[12], author=doc[4], abstract=doc[1])
#     print(file)
# writer.commit()
# print("math done")

ix = open_dir("index", indexname="cs")
writer = ix.writer()

for file in glob.glob("data/per_category/cs.*.tsv"):
    with open(file, 'r', encoding="utf-8") as f:
        rd = csv.reader(f, delimiter="\t")
        for doc in rd:
            writer.add_document(title=doc[12], author=doc[4], abstract=doc[1])
    print(file)
writer.commit()
print("cs done")

# ix = open_dir("index", indexname="physics")
# writer = ix.writer()
#
# for file in glob.glob("data/per_category/physics.*.tsv"):
#     with open(file, 'r', encoding="utf-8") as f:
#         rd = csv.reader(f, delimiter="\t")
#         for doc in rd:
#             writer.add_document(title=doc[12], author=doc[4], abstract=doc[1])
#     print(file)
# writer.commit()
# print("physics done")