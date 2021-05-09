import requests
from tkinter import *


def get_movies_from_tastedive(movie):
    parms = {'q': movie , 'type' : 'movies' , 'limit' : '5' }
    res = requests.get('https://tastedive.com/api/similar' , params=parms)
    js = res.json()
    return js

def extract_movie_titles(d) :
    rml = []
    for i in d['Similar']['Results'] :
        rml.append(i['Name'])
    return rml

def get_related_titles(lm) :
    if len(lm) == 0 :
        return []
    else :
        temp=[]
        for movie in lm :
            temp += extract_movie_titles(get_movies_from_tastedive(movie))
        movies = []
        movies.append(lm[-1])
        for i in temp :
            if i not in movies :
                movies.append(i)
        
        return list((movies))
    
def get_movie_data(title):
    params_d = { 't' : title,'r' : 'json'}
    resp = requests.get(' http://www.omdbapi.com/?i=tt3896198&apikey=65208678', params = params_d)
    page = resp.json()
    print(page['Title'])
    return page 

def  get_movie_rating(d) :
    r = 0
    for i in (d['Ratings']):
        if i['Source'] == 'Rotten Tomatoes' :
            r = int(i['Value'][:-1])
            return r
    return r

def get_sorted_recommendations(lom) :
    rel_mov = get_related_titles(lom)
    rel_mov.sort()
    rl=[]
    for i in rel_mov :
        rl.append(get_movie_rating(get_movie_data(i)))
    temp = list(zip(rel_mov,rl))
    sl = sorted(temp, key = lambda x:x[1],reverse=1)
    ans = []
    for i in sl :
        ans.append(i[0])
    return ans

def onClick():
    name = txtvar0.get()
    l=[]
    l.append(name)
    rel_movies = get_sorted_recommendations(l)
    rel_movies.remove(name)
    if rel_movies == [] :
        l = Label(top, text='Sorry ! No movies found : ^ ( ', font=('Calibri',14),fg='red').place(x=40,y=180)
    else :
        y_val = 220
        l2 = Label(top, text='You Might Also Like ',font=('Calibri',14),fg='red').place(x=40,y=180)
        for movie in rel_movies :
            l = Label(top, text = movie , font=('Calibri',15)).place(x=43,y=y_val)
            y_val += 25

top = Tk()
top.title('Movie Recommendation')
top.geometry('600x400')

txtvar0= StringVar()


l0 = Label(top, text = 'MOVIE RECOMMENDATION', font=('Calibri', 18), fg='Blue').place(x=300,y=30,a='center')
l1 = Label(top, text = 'Enter Movie Name', font=('Calibri',14),fg='red').place(x=40,y=80)
e0 = Entry(top ,textvariable = txtvar0, font = ('Calibri',12),width=30).place(x=230,y=80)
b0 = Button(top, text = 'Get Results !',font=('Calibri',12),height=1,width=20,command=onClick).place(x=300,y=140,a='center')


top.mainloop()







