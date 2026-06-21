import http.server
import socketserver
import json
import os

PORT = 8080

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            
            html = """<!DOCTYPE html>
<html>
<head>
    <title>Logo Verifier</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; padding: 20px; background: #f4f6f8; color: #333; }
        .container { max-width: 1000px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; vertical-align: middle; }
        th { background: #f9f9f9; }
        img { max-height: 40px; max-width: 40px; object-fit: contain; border-radius: 4px; border: 1px solid #eee; }
        input { width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
        .header-bar { display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; background: white; padding: 10px 0; border-bottom: 2px solid #eee; z-index: 10; margin-bottom: 20px;}
        button { padding: 10px 20px; background: #21ce99; border: none; color: white; cursor: pointer; font-size: 16px; border-radius: 5px; font-weight: bold; }
        button:hover { background: #1bae7f; }
        .hint { color: #666; font-size: 0.9em; margin-top: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header-bar">
            <div>
                <h1 style="margin:0;">Team Logo Verifier</h1>
                <div class="hint">Type in the URL box to search available Wikipedia logos, or paste any flag URL (e.g. from Wikipedia).</div>
            </div>
            <button onclick="save()">Save Mappings</button>
        </div>
        <div id="app">Loading team data...</div>
    </div>

    <script>
        let logos = {};
        let teams = [];
        async function init() {
            const res = await fetch('/api/data');
            const data = await res.json();
            logos = data.logos;
            teams = data.teams;
            render();
        }
        
        function render() {
            // Prepare datalist for autocomplete
            let datalist = '<datalist id="all_logos">';
            for (const key in logos) {
                // Using the team/file name as the text so people can search by typing the country/team name
                datalist += `<option value="${logos[key]}">${key}</option>`;
            }
            datalist += '</datalist>';
            
            let html = datalist + '<table><tr><th width="25%">Team Name</th><th width="10%">Preview</th><th width="65%">Logo URL (Search or Paste)</th></tr>';
            teams.forEach(t => {
                let defaultAvatar = `https://ui-avatars.com/api/?name=${encodeURIComponent(t)}&background=random&color=fff&bold=true`;
                let currentUrl = logos[t] || '';
                let previewUrl = currentUrl || defaultAvatar;
                
                html += `<tr>
                    <td><strong>${t}</strong></td>
                    <td style="text-align:center;"><img src="${previewUrl}" id="img_${t}" onerror="this.src='${defaultAvatar}'"></td>
                    <td>
                        <input type="url" list="all_logos" id="input_${t}" value="${currentUrl}" placeholder="Search alternatives or paste a URL..." onchange="document.getElementById('img_${t}').src = this.value || '${defaultAvatar}'" onkeyup="document.getElementById('img_${t}').src = this.value || '${defaultAvatar}'">
                    </td>
                </tr>`;
            });
            html += '</table>';
            document.getElementById('app').innerHTML = html;
        }
        
        async function save() {
            const btn = document.querySelector('button');
            btn.textContent = 'Saving...';
            
            let mappings = {};
            teams.forEach(t => {
                let val = document.getElementById('input_' + t).value.trim();
                // Only save if a URL is provided
                if (val) mappings[t] = val;
            });
            
            try {
                const res = await fetch('/api/save', { 
                    method: 'POST', 
                    body: JSON.stringify(mappings),
                    headers: { 'Content-Type': 'application/json' }
                });
                if(res.ok) {
                    btn.textContent = 'Saved! ✅';
                    btn.style.background = '#333';
                    setTimeout(() => { btn.textContent = 'Save Mappings'; btn.style.background = '#21ce99'; }, 3000);
                    alert('Mappings saved successfully! Go back to VS Code and let Copilot know you are done so I can commit the changes.');
                }
            } catch(e) {
                alert('Error saving: ' + e);
                btn.textContent = 'Save Mappings';
            }
        }
        init();
    </script>
</body>
</html>
            """
            self.wfile.write(html.encode('utf-8'))

        elif self.path == '/api/data':
            with open('fixtures.json', 'r') as f:
                fixtures = json.load(f)
            with open('team_logos.json', 'r') as f:
                logos = json.load(f)
                
            teams = set()
            for m in fixtures.get('matches', []):
                for t in m.get('teams', []):
                    if 'name' in t:
                        teams.add(t['name'].strip())
                        
            data = {
                "teams": sorted(list(teams)),
                "logos": logos
            }
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode('utf-8'))
            
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/api/save':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            new_mappings = json.loads(post_data.decode('utf-8'))
            
            with open('team_logos.json', 'r') as f:
                current_logos = json.load(f)
                
            # Update current mappings with the specified URLs
            current_logos.update(new_mappings)
            
            with open('team_logos.json', 'w', encoding='utf-8') as f:
                json.dump(current_logos, f, indent=2, ensure_ascii=False)
                
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode('utf-8'))

# Allow port reuse so we don't get 'address already in use' locally
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"UI Verification server running at http://localhost:{PORT}")
    httpd.serve_forever()
