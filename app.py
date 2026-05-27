from flask import Flask, render_template, request, send_file
import requests
from bs4 import BeautifulSoup
import urllib.parse
import pandas as pd
import os

app = Flask(__name__)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def search_resources(keyword):
    results = []
    encoded = urllib.parse.quote(keyword)

    # GitHub
    try:
        url = f"https://github.com/search?q={encoded}&type=repositories"
        soup = BeautifulSoup(requests.get(url, headers=HEADERS, timeout=10).text, "html.parser")
        for item in soup.select(".repo-list-item")[:5]:
            title = item.get_text(strip=True)
            link = "https://github.com" + item.find("a")["href"]
            results.append([title, link, "GitHub"])
    except:
        pass

    # PyPI
    try:
        url = f"https://pypi.org/search/?q={encoded}"
        soup = BeautifulSoup(requests.get(url, headers=HEADERS, timeout=10).text, "html.parser")
        for item in soup.select(".package-snippet")[:5]:
            title = item.find("span", class_="package-snippet__name").get_text(strip=True)
            link = "https://pypi.org" + item.find("a")["href"]
            results.append([title, link, "PyPI"])
    except:
        pass

    # Stack Overflow
    try:
        url = f"https://stackoverflow.com/search?q={encoded}"
        soup = BeautifulSoup(requests.get(url, headers=HEADERS, timeout=10).text, "html.parser")
        for item in soup.select(".question-summary")[:5]:
            title = item.find("a", class_="question-hyperlink").get_text(strip=True)
            link = "https://stackoverflow.com" + item.find("a")["href"]
            results.append([title, link, "StackOverflow"])
    except:
        pass

    return results

@app.route("/", methods=["GET", "POST"])
def index():
    data = []
    keyword = ""
    if request.method == "POST":
        keyword = request.form.get("keyword")
        data = search_resources(keyword)
    return render_template("index.html", data=data, keyword=keyword)

@app.route("/export")
def export():
    keyword = request.args.get("keyword", "export")
    data = search_resources(keyword)
    df = pd.DataFrame(data, columns=["标题", "链接", "来源"])
    path = "搜索结果.xlsx"
    df.to_excel(path, index=False)
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
