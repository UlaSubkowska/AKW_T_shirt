import json
from  functools import reduce
from flask import Flask,redirect, render_template
app = Flask(__name__)

def save_votes(dict_votes):
    try:
        with open('votes.json','w') as outfile:
            json.dump(dict_votes,outfile)
        return True
    except Exception as e:
        print(e)

def load_votes():
    try:
        with open('votes.json','r') as infile:
            data=json.load(infile)
        return data
    except Exception as e:
        print(e)
        return None

def count_percent():
    votes_n = load_votes()
    votes_sum = reduce(lambda a, b: a + b, votes_n.values(), 0)
    votes_percent = {}
    for key in votes_n.keys():
        votes_percent["vote_" + key] = int(votes_n[key] / votes_sum * 100)
    return votes_percent

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/votes')
def votes():
    return app.send_static_file('votes.html')

@app.route('/results')
def results():
    votes_percent=count_percent()
    return render_template('results.html', **votes_percent)

@app.route('/winner')
def winner():
    votes_percent=count_percent()
    winner=0
    winner_key=''
    for key in votes_percent:
        if votes_percent[key]>winner:
            winner=votes_percent[key]
            winner_key=key
    t_shirts = {'vote_1': 'ekspresowo', 'vote_2': 'kości', 'vote_3': 'pociag', 'vote_4': 'mierzymy',
                'vote_5': 'natopie', 'vote_6': 'zajdziesz'}
    winner_img=t_shirts[winner_key]
    winner_link="static/assets/img/{0}.png".format(winner_img)
    return render_template('winner.html',winner_link=winner_link)

@app.route('/vote/<int:vote_id>')
def vote(vote_id):
    try:
        votes_n=load_votes()
        votes_n[str(vote_id)]+=1
        print(votes_n)
        save_votes(votes_n)
    except:
        print("Error: No index " + str(vote_id))

    return redirect("results", code=302)


app.run()
