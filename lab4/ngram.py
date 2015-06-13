import random, string
 
infilename = "texts/2009-Obama.txt"
trainingdata = open(infilename).read()
trainingdata = trainingdata.translate(string.maketrans("",""), string.punctuation).lower()
 
contextconst = [""]
 
context = contextconst
model = {}
 
for word in trainingdata.split():
    #print (word)
    model[str(context)] = model.setdefault(str(context),[])+ [word]
    context = (context+[word])[1:]
 
#print(model)
 
context = contextconst
for i in range(100):
    word = random.choice(model[str(context)])
    print word
    context = (context+[word])[1:]
 
print