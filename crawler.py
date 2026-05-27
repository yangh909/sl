import requests
from bs4 import BeautifulSoup
import urllib.parse

# 基础请求头（模拟浏览器访问）
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def search_public_resources(keyword):
    """根据关键词爬取公开可访问的资源索引信息"""
    result_list = []
    encoded_key = urllib.parse.quote(keyword)

    # --------------------------
    # 爬取来源 1：GitHub 公开项目
    # --------------------------
    try:
        github_url = f"https://github.com/search?q={encoded_key}&type=repositories"
        resp = requests.get(github_url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")

        for item in soup.select(".Box-sc-g0xbh4-0 .repo-list-item")[:5]:
            title = item.select_one("a").get_text(strip=True)
            link = "https://github.com" + item.select_one("a")["href"]
            result_list.append({"title": title, "url": link, "source": "GitHub"})
    except:
        pass

    # --------------------------
    # 爬取来源 2：Pypi 开源工具
    # --------------------------
    try:
        pypi_url = f"https://pypi.org/search/?q={encoded_key}"
        resp = requests.get(pypi_url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")

        for pkg in soup.select(".package-snippet")[:5]:
            title = pkg.select_one(".package-snippet__title").get_text(strip=True)
            link = "https://pypi.org" + pkg.select_one("a")["href"]
            result_list.append({"title": title, "url": link, "source": "PyPI"})
    except:
        pass

    # --------------------------
    # 爬取来源 3：Stack Overflow 技术资源
    # --------------------------
    try:
        so_url = f"https://stackoverflow.com/search?q={encoded_key}"
        resp = requests.get(so_url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")

        for question in soup.select(".question-summary")[:5]:
            title = question.select_one(".question-hyperlink").get_text(strip=True)
            link = "https://stackoverflow.com" + question.select_one(".question-hyperlink")["href"]
            result_list.append({"title": title, "url": link, "source": "StackOverflow"})
    except:
        pass

    return result_list

if __name__ == "__main__":
    print("=" * 50)
    print("      公开资源爬取工具（安全合规版）")
    print("=" * 50)
    keyword = input("\n请输入搜索关键词：")

    print("\n正在搜索中，请稍候...\n")
    results = search_public_resources(keyword)

    if not results:
        print("未找到相关公开资源")
    else:
        print(f"找到 {len(results)} 条相关信息：\n")
        for idx, res in enumerate(results, 1):
            print(f"{idx}. 【{res['source']}】{res['title']}")
            print(f"   链接：{res['url']}\n")
