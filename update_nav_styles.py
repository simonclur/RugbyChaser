import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Make .bottom-nav dark blue and remove neon green glow
html = re.sub(
    r'(\.bottom-nav\s*\{[^}]*background-color:\s*)[^;]+(;)',
    r'\g<1>#000033\g<2>',
    html
)
html = re.sub(
    r'(box-shadow:\s*0 -4px 12px )rgba\(57, 255, 20, 0\.4\)',
    r'\g<1>rgba(0,0,0,0.4)',
    html
)


# Add white border/rounding for normal .nav-tab items 
html = re.sub(
    r'(\.nav-tab\s*\{[^}]*border:\s*)[^;]+(;)',
    r'\g<1>1px solid rgba(255,255,255,0.7)\g<2>',
    html
)

html = re.sub(
    r'(\.nav-tab\s*\{[^}]*background-color:\s*)[^;]+(;)',
    r'\g<1>rgba(255,255,255,0.1)\g<2>',
    html
)
html = re.sub(
    r'(\.nav-tab\s*\{[^}]*color:\s*)[^;]+(;)',
    r'\g<1>#ffffff\g<2>',
    html
)



# Make them deep blue when highlighted
html = re.sub(
    r'(\.nav-tab:hover,\s*\.nav-tab:active,\s*\.nav-tab\.active-section\s*\{[^}]*background-color:\s*)[^;]+(;)',
    r'\g<1>#000080\g<2>',
    html
)
html = re.sub(
    r'(\.nav-tab:hover,\s*\.nav-tab:active,\s*\.nav-tab\.active-section\s*\{[^}]*border-color:\s*)[^;]+(;)',
    r'\g<1>#ffffff\g<2>',
    html
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
