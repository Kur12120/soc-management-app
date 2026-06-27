import os

fname = 'backend/src/routes/users.ts'
if os.path.exists(fname):
    c = open(fname, encoding='utf-8').read()
    
    # Locate the POST handler for user creation
    old_route = 'router.post("/", requireAuth, requireRole(["admin"]), async (req: Request, res: Response) => {'
    
    if old_route in c and "try {" not in c[c.find(old_route):c.find(old_route)+150]:
        # Inject try block at the start of the route handler
        new_route = old_route + "\n  try {"
        c = c.replace(old_route, new_route)
        
        # Inject the catch block right before the final closing brace of the post route
        # Looking for the standard response line inside the route
        old_res = 'res.status(201).json(user);'
        if old_res in c:
            new_res = 'res.status(201).json(user);\n  } catch (err: any) { \n    if (err.code === "23514") {\n      res.status(400).json({ message: "Invalid role selected. Allowed roles are: admin, analyst, super_admin." });\n    } else {\n      res.status(500).json({ message: err.message || "Internal server error" });\n    }\n  }'
            c = c.replace(old_res, new_res)
            
        open(fname, 'w', encoding='utf-8').write(c)
        print("Successfully injected validation catch constraints into users.ts!")
    else:
        print("Target pattern already updated or not found.")