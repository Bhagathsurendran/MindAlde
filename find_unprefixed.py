import os, re

unprefixed = set()
files_with_issues = {}

for d in ['templates', 'routes']:
    if not os.path.isdir(d): continue
    for root, dirs, files in os.walk(d):
        for file in files:
            if file.endswith('.html') or file.endswith('.py'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                matches = re.findall(r"url_for\(['\"]([^.]+?)['\"]", content)
                for m in matches:
                    if m != 'static':
                        unprefixed.add(m)
                        if m not in files_with_issues:
                            files_with_issues[m] = []
                        files_with_issues[m].append(filepath)

with open('unprefixed_results.txt', 'w', encoding='utf-8') as f:
    f.write('UNPREFIXED ENDPOINTS FOUND:\n')
    for endpoint, flist in files_with_issues.items():
        f.write(f'- {endpoint} mapped in {len(flist)} files. e.g. {flist[0]}\n')
