import tkinter
import whoosh
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
import whoosh.qparser
from tkinter import *
from whoosh import sorting
import spacy

en_nlp = spacy.load('en')
window = tkinter.Tk()
window.geometry("930x620")
window.title("search interface")

query = tkinter.StringVar()

output_frame = tkinter.Frame(window).grid(row=1)
entry = tkinter.Entry(window, width=75, textvariable=query).grid(row=0, column=0, sticky=S + W + E + N)

tkinter.Label(output_frame, text="RESULT:", font='times 15 bold', height=3).grid(row=1, column=0, sticky=W)

out_text = Text(window, height=38, width=100, highlightbackground='black', highlightthickness=1, bd=10, wrap=WORD)
out_text.tag_config("highlight", foreground='red')
out_text.grid(row=2, columnspan=4, sticky=S + W + E + N)
scroll = Scrollbar(orient='vertical', command=out_text.yview)
out_text['yscrollcommand'] = scroll.set
scroll.grid(row=2, column=5, sticky=S + W + E + N)

out_text.tag_config('abs', font='times 16', spacing1=5, spacing2=1, spacing3=5)
out_text.tag_config('highlight', font='times 16 bold', background="cyan")

facet = sorting.FieldFacet('date', reverse=True)

def rank(doc, query):
    words = len(query.split(' '))
    txt = doc.highlights('content')
    sentence_words = en_nlp(txt)
    idxs = [idx for idx in range(len(sentence_words) - words) if query == str(sentence_words[idx: idx + words])]
    if not idxs:
        return 200
    loc = doc['location']
    length = len(sentence_words)
    num = len(idxs)
    word_tag = [sentence_words[idx + words - 1].dep_.lower() for idx in idxs]
    auxs = [str(sentence_words[idx + words]).lower() for idx in idxs]
    aux_tag = [sentence_words[idx + words].dep_.lower() for idx in idxs]
    try:
        i = aux_tag.index('punct')
        find = False
        for word in sentence_words[idxs[i]+words+1:]:
            if find:
                aux_tag.append(word.dep_.lower())
                break
            if word.dep_.lower() == 'punct':
                find = True
    except:
        pass
    pre_tag = [sentence_words[idx - 1].dep_.lower() for idx in idxs if idx != 0]
    aux_pre = [str(sentence_words[idx-1]).lower() for idx in idxs if idx != 0]
    tag = 0
    if ('pobj' in word_tag) or ('dobj' in word_tag) or ('obj' in word_tag) or ('nsubj' in word_tag) or ('nsubjpass' in word_tag) or ('root' in word_tag):
        tag -= 20
    if ('amod' in pre_tag) or ('compound' in pre_tag):
        tag += 15
    if 'is' in auxs:
        tag -= 20
    elif 'aux' in aux_tag or 'auxpass' in aux_tag or 'root' in aux_tag:
        tag -= 10
    if 'is' in aux_pre:
        tag -= 15
    # if (txt == 'Crowdsourcing and DATA MINING can be used to effectively reduce the effort associated with the partial replication and enhancement of qualitative studies.'):
    #     print(0.3 * length)
    #     print(2 * idxs[0])
    #     print(num)
    #     print(tag)
    #     print("A")
    # if (txt == 'DATA MINING (driven by appropriate knowledge discovery tools) is about processing available (observed, known and understood) samples of DATA aiming to build a model (e.g., a classifier) to handle DATA samples, which are not yet observed, known or understood.'):
    #     print(0.3 * length)
    #     print(2 * idxs[0])
    #     print(num)
    #     print(tag)
    #     print("B")
    return 0.1 * length + 3 * idxs[0] + loc - num + tag

def search_ph(query, text):
    text.delete(1.0, END)
    query_str = query.get()
    ix = open_dir("index", indexname="physics")
    mp = QueryParser("content", schema=ix.schema)
    q = mp.parse('"%s"' % query_str)
    with ix.searcher() as searcher:
        ph_re = searcher.search(q, limit=500, terms=True, sortedby=facet)
        ph_re.formatter = whoosh.highlight.UppercaseFormatter()
        ph_re.fragmenter = whoosh.highlight.WholeFragmenter()
        ph_re = [x for x in ph_re]
        ph_re.sort(key=lambda x: rank(x, query_str.upper()))
        docs = []
        for doc in ph_re:
            if doc.highlights('content') not in docs:
                docs.append(doc.highlights('content'))
        for abs in docs:
            abs = abs.split(query_str.upper())
            for snippet in abs[:-1]:
                text.insert(END, snippet, 'abs')
                text.insert(END, query_str, 'highlight')
            text.insert(END, abs[-1], 'abs')
            text.insert(END, '\n\n')

def search_cs(query, text):
    text.delete(1.0, END)
    query_str = query.get()
    ix = open_dir("index", indexname="cs")
    mp = QueryParser("content", schema=ix.schema)
    q = mp.parse('"%s"' % query_str)
    with ix.searcher() as searcher:
        cs_re = searcher.search(q, limit=800, terms=True, sortedby=facet)
        cs_re.formatter = whoosh.highlight.UppercaseFormatter()
        cs_re.fragmenter = whoosh.highlight.WholeFragmenter()
        cs_re = [x for x in cs_re]
        cs_re.sort(key=lambda x: rank(x, query_str.upper()))
        docs = []
        for doc in cs_re:
            if doc.highlights('content') not in docs:
                docs.append(doc.highlights('content'))
        for abs in docs:
            abs = abs.split(query_str.upper())
            for snippet in abs[:-1]:
                text.insert(END, snippet, 'abs')
                text.insert(END, query_str, 'highlight')
            text.insert(END, abs[-1], 'abs')
            text.insert(END, '\n\n')

def search_math(query, text):
    text.delete(1.0, END)
    query_str = query.get()
    ix = open_dir("index", indexname="math")
    mp = QueryParser("content", schema=ix.schema)
    q = mp.parse(query_str)
    with ix.searcher() as searcher:
        ma_re = searcher.search(q, limit=500, terms=True, sortedby=facet)
        ma_re.formatter = whoosh.highlight.UppercaseFormatter()
        ma_re.fragmenter = whoosh.highlight.WholeFragmenter()
        ma_re = [x for x in ma_re]
        ma_re.sort(key=lambda x: rank(x, query_str.upper()))
        docs = []
        for doc in ma_re:
            if doc.highlights('content') not in docs:
                docs.append(doc.highlights('content'))
        for abs in docs:
            abs = abs.split(query_str.upper())
            for snippet in abs[:-1]:
                text.insert(END, snippet, 'abs')
                text.insert(END, query_str, 'highlight')
            text.insert(END, abs[-1], 'abs')
            text.insert(END, '\n\n')

button_cs = tkinter.Button(window, text="cs", fg="red", width=8, command=lambda : search_cs(query, out_text)).grid(row=0, column=1, sticky=S + W + E + N)
button_math = tkinter.Button(window, text="math", fg="green", width=8, command=lambda : search_math(query, out_text)).grid(row=0, column=2, sticky=S + W + E + N)
button_ph = tkinter.Button(window, text="physics", fg="purple", width=8, command=lambda : search_ph(query, out_text)).grid(row=0, column=3, sticky=S + W + E + N)

window.mainloop()