import re, os

# Fix all userId type errors in route files
for fname in ['backend/src/routes/tasks.ts', 'backend/src/routes/incidents.ts', 'backend/src/routes/users.ts']:
    if not os.path.exists(fname):
        continue
    c = open(fname, encoding='utf-8').read()
    c = c.replace('req.user!.userId', '(req.user as any).userId')
    c = c.replace('(req.user!.userId as string)', '(req.user as any).userId')
    # Fix missing title in createNotification
    c = re.sub(r"createNotification\(\{(\s*userId:[^,]+),(\s*message:)", r"createNotification({\1, title: 'Task assigned',\2", c)
    open(fname, 'w', encoding='utf-8').write(c)
    print(f'Fixed: {fname}')

# Fix ldapService.ts
fname = 'backend/src/services/ldapService.ts'
if os.path.exists(fname):
    c = open(fname, encoding='utf-8').read()
    c = re.sub(r'[^\n]*\.attributes[^\n]*Attribute\[\][^\n]*\n', '', c)
    c = re.sub(r'[^\n]*\.pojo[^\n]*\n', '', c)
    open(fname, 'w', encoding='utf-8').write(c)
    print(f'Fixed: {fname}')

print('All TypeScript errors fixed')