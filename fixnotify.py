import re, os

for fname in ['backend/src/routes/tasks.ts', 'backend/src/routes/incidents.ts']:
    if not os.path.exists(fname):
        continue
    c = open(fname, encoding='utf-8').read()
    # Fix missing title in createNotification calls
    c = re.sub(
        r"createNotification\(\s*\{([^}]*?userId[^}]*?message[^}]*?)\}",
        lambda m: "createNotification({ title: 'Assignment', " + m.group(1).strip() + "}",
        c
    )
    open(fname, 'w', encoding='utf-8').write(c)
    print('Fixed: ' + fname)

print('Done')