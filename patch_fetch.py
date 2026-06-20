with open("fetch_fixtures.py", "r") as f:
    code = f.read()

new_code = code.replace(
    'base_url = "https://api.wr-rims-prod.pulselive.com/rugby/v3/match?startDate={}&endDate={}&sport=mru&pageSize=100&page={}"',
    'base_url = "https://api.wr-rims-prod.pulselive.com/rugby/v3/match?startDate={}&endDate={}&pageSize=100&page={}"'
)

with open("fetch_fixtures.py", "w") as f:
    f.write(new_code)
