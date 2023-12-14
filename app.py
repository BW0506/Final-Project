from flask import Flask, render_template, request
from functions import most_similar_info, most_similar_info2
import os
import requests

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


# Create a view function for /results
@app.route("/results", methods=["POST"])
def results():
    url = 'https://graphql.anilist.co'
    query = '''
        query {
          Page(page: 1, perPage: 5) {
            media(sort: TRENDING_DESC, type: ANIME) {
              title {
                english
              }
              popularity
              trending
              genres
              episodes
              coverImage{
              large
              }
            }
          }
        }
        '''
    response = requests.post(url, json={'query': query})
    data = response.json()
    if "file" in request.files and request.files["file"].filename != "" and "blackborder" not in request.form:
        file = request.files["file"]
        save_path = "path/to/save"
        filepath = os.path.join(save_path, file.filename)
        file.save(filepath)
        search_results = most_similar_info(filepath)
        return render_template("results.html", results=search_results, anime_data=data["data"]["Page"]["media"])
    elif "file" in request.files and request.files["file"].filename != "" and "blackborder" in request.form:
        file = request.files["file"]
        save_path = "path/to/save"
        filepath = os.path.join(save_path, file.filename)
        file.save(filepath)
        search_results = most_similar_info2(filepath)
        return render_template("results.html", results=search_results, anime_data=data["data"]["Page"]["media"])
    elif "url" in request.form and request.form["url"] != "" and "blackborder" not in request.form:
        input = request.form["url"]
        search_results = most_similar_info(input)
        return render_template("results.html", results=search_results, anime_data=data["data"]["Page"]["media"])
    elif "url" in request.form and request.form["url"] != "" and "blackborder" in request.form:
        input = request.form["url"]
        search_results = most_similar_info2(input)
        return render_template("results.html", results=search_results, anime_data=data["data"]["Page"]["media"])
    return "No file or url submitted"

if __name__=="__main__":
    app.run()