import urllib.request
import urllib.parse
import json
import time

def fetch_category_members(category, max_depth=2, current_depth=0, visited_cats=None):
    if visited_cats is None:
        visited_cats = set()
        
    if category in visited_cats or current_depth > max_depth:
        return [], []
        
    visited_cats.add(category)
    
    files = []
    subcats = []
    
    api_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": category,
        "cmlimit": "max",
        "format": "json"
    }
    
    cmcontinue = None
    
    while True:
        p = params.copy()
        if cmcontinue:
            p["cmcontinue"] = cmcontinue
            
        url = api_url + "?" + urllib.parse.urlencode(p)
        print(f"Fetching {category}..." if not cmcontinue else f"Fetching {category} (continue)...")
        time.sleep(2) # Be nice to the API
        
        req = urllib.request.Request(url, headers={'User-Agent': 'RugbyChaserLogos/1.0 (https://github.com/simonclur/RugbyChaser)'})
        try:
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                for member in data.get('query', {}).get('categorymembers', []):
                    if member['ns'] == 6:  # File
                        files.append(member['title'])
                    elif member['ns'] == 14:  # Category
                        subcats.append(member['title'])
                        
                cmcontinue = data.get('continue', {}).get('cmcontinue')
                if not cmcontinue:
                    break
        except Exception as e:
            print(f"Error: {e}")
            break
            
    return files, subcats

def fetch_all_files():
    all_files = set()
    categories_to_visit = ["Category:Rugby_union_logos", "Category:National_rugby_union_team_logos"]
    visited = set()
    
    while categories_to_visit:
        cat = categories_to_visit.pop(0)
        files, subcats = fetch_category_members(cat, max_depth=3, visited_cats=visited)
        for f in files:
            all_files.add(f)
        for sc in subcats:
            if sc not in visited:
                categories_to_visit.append(sc)
                
    return list(all_files)

def clean_team_name(filename):
    # Remove "File:"
    name = filename.replace("File:", "")
    # Remove extension
    name = name.rsplit(".", 1)[0]
    # Replace underscores with spaces
    name = name.replace("_", " ")
    
    # Remove common suffixes
    remove_phrases = [
        " national rugby union team",
        " national rugby sevens team",
        " national rugby team",
        " rugby union team",
        " rugby team",
        " logo",
        " crest",
        " emblem",
        " badge",
        " (rugby union)",
        " (rugby)",
        " Rugby",
        " RFC"
    ]
    
    for phrase in remove_phrases:
        if name.lower().endswith(phrase.lower()):
            name = name[:len(name) - len(phrase)]
            
    return name.strip()

def fetch_image_urls(file_titles):
    results = {}
    
    # Chunk requests by 50 (API limit)
    chunk_size = 50
    api_url = "https://en.wikipedia.org/w/api.php"
    
    print(f"Fetching URLs for {len(file_titles)} files...")
    
    for i in range(0, len(file_titles), chunk_size):
        chunk = file_titles[i:i+chunk_size]
        params = {
            "action": "query",
            "prop": "imageinfo",
            "iiprop": "url",
            "titles": "|".join(chunk),
            "format": "json"
        }
        
        req = urllib.request.Request(api_url, data=urllib.parse.urlencode(params).encode('utf-8'), headers={'User-Agent': 'RugbyChaserLogos/1.0 (https://github.com/simonclur/RugbyChaser)'})
        try:
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                pages = data.get('query', {}).get('pages', {})
                for page_id, page_data in pages.items():
                    if 'imageinfo' in page_data and len(page_data['imageinfo']) > 0:
                        url = page_data['imageinfo'][0]['url']
                        title = page_data['title']
                        guessed_name = clean_team_name(title)
                        results[guessed_name] = url
        except Exception as e:
            print(f"Error fetching URLs: {e}")
            
    return results

if __name__ == "__main__":
    files = fetch_all_files()
    print(f"Found {len(files)} logo files. Fetching URLs...")
    
    logos = fetch_image_urls(files)
    
    # Sort alphabetically by team name
    sorted_logos = dict(sorted(logos.items()))
    
    with open("team_logos.json", "w", encoding="utf-8") as f:
        json.dump(sorted_logos, f, indent=2, ensure_ascii=False)
        
    print(f"Saved {len(sorted_logos)} logos to team_logos.json")
