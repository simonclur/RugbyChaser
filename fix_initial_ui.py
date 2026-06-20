with open('index.html', 'r') as f:
    text = f.read()

text = text.replace("const loadedMatchDetails = {};", "const loadedMatchDetails = {};\n        let isInitialUI = true;")

with open('index.html', 'w') as f:
    f.write(text)
