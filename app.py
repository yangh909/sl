# --------------- 一键运行：资源搜索工具（网页版 + Excel导出）---------------
from flask import Flask, render_template_string, request, send_file
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

html_page = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>资源搜索工具</title>
    <style>
        body{max-width:1000px;margin:30px auto;font-family:Arial}
        .box{padding:20px;background:#f5f5f5;border-radius:10px}
        input{width:70%;padding:10px;font-size:16px}
        button{padding:10px 20px;background:#007bff;color:white;border:none;border-radius:5px;cursor:pointer}
        table{width:100%;margin-top:20px;border-collapse:collapse}
        td,th{border:1px solid #ddd;padding:10px;text-align:left}
        th{background:#007bff;color:white}
        .export{background:#28a745;margin-top:15px}
    </style>
</head>
<body>
    <h2>📌 公开资源搜索工具</h2>
    <div class="box">
        <form method="post">
            <input type="text" name="keyword" placeholder="输入关键词" required>
            <button type="submit">搜索</button>
        </form>
        {% if data %}
        <a href="/export?keyword={{ keyword }}"><button class="export">📥 导出 Excel</button></a>
        <table>
            <tr><th>标题</th><th>链接</th><th>来源</th></tr>
            {% for row in data %}
            <tr><td>{{ row[0] }}</td><td><a href="{{ row[1] }}" target="_blank">打开</a></td><td>{{ row[2] }}</td></tr>
            {% endfor %}
        </table>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    data = []
    keyword = ""
    if request.method == "POST":
        keyword = request.form.get("keyword")
        data = search_resources(keyword)
    return render_template_string(html_page, data=data, keyword=keyword)

@app.route("/export")
def export():
    keyword = request.args.get("keyword", "result")
    data = search_resources(keyword)
    df = pd.DataFrame(data, columns=["标题", "链接", "来源"])
    file_path = f"{keyword}_搜索结果.xlsx"
    df.to_excel(file_path, index=False)
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
