import requests
import os
from datetime import datetime

# --- CONFIGURATION (Safe Version) ---
API_KEY = os.getenv("NEWS_API_KEY")
GITHUB_USER = os.getenv("GH_USER")
GITHUB_PAT = os.getenv("GH_TOKEN")
REPO_NAME = "daily-tech-archive"
# ------------------------------------

def run():
    print(f"Starting update at {datetime.now()}")
    
    # 1. Fetch Tech News
    url = f"https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey={API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        articles = data.get('articles', [])[:5]
    except Exception as e:
        print(f"API Error: {e}")
        return

    # 2. Format the log entry
    date_str = datetime.now().strftime("%Y-%m-%d")
    new_content = f"\n### 🛡️ Daily Archive: {date_str}\n"
    for art in articles:
        new_content += f"- [{art['title']}]({art['url']})\n"

    # 3. Write to file
    with open("DAILY_LOG.md", "a") as f:
        f.write(new_content)

    # 4. Git Push Automation
    # Using the PAT in the URL for headless authentication
    remote_url = f"https://{GITHUB_USER}:{GITHUB_PAT}@github.com/{GITHUB_USER}/{REPO_NAME}.git"
    
    os.system('git config --global user.name "NAS-Bot"')
    os.system('git config --global user.email "bot@nas.local"')
    os.system('git add DAILY_LOG.md')
    os.system(f'git commit -m "Automated update: {date_str}"')
    os.system(f'git push {remote_url} main')
    print("Update pushed to GitHub successfully.")

if __name__ == "__main__":
    run()