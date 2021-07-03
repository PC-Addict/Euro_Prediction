import flask
from flask import request, jsonify,Response,render_template
import json
import pandas as pd

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
@app.route('/#homepage', methods=['GET'])
def home():
	homeJsonObj = open("home.json", "r")
	homePageContent = homeJsonObj.read()
	homePage = json.loads(homePageContent)
	return render_template('index.html', homePageNews=homePage)

@app.route('/', methods=['POST'])
def stats():
	if request.method == 'POST':
		euroRawDF = pd.read_csv('EURO 2021 stats.csv')
		euroDF = euroRawDF.dropna()
		euroStatForm = request.form
		SelectTeam = euroStatForm['select team']
		SortByKey = euroStatForm['sort by']
		euroSelectedDF = euroDF[["Player","Team",SortByKey]]
		if SelectTeam == "All":
			euroSortedDF = euroSelectedDF.sort_values(by=[SortByKey], ascending=False)
		else :
			euroSelectedDF = euroSelectedDF[euroSelectedDF["Team"] == SelectTeam]
			euroSortedDF = euroSelectedDF.sort_values(by=[SortByKey], ascending=False)
		euroSortedDF.rename(columns = {SortByKey:'Result'}, inplace = True)
		euroSortedDF = euroSortedDF.head(20)
		euroSortedJson = euroSortedDF.to_json(orient="records")
		euroStats = json.loads(euroSortedJson)
		return render_template('index.html', statsData=euroStats,Player="Player",Team="Team",sortby=SortByKey)

app.run()