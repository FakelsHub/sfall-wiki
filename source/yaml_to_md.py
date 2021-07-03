#!/usr/bin/env python3
# coding: utf-8

import sys, os
import ruamel.yaml
yaml = ruamel.yaml.YAML(typ="rt")
yaml.width = 4096
yaml.indent(mapping=2, sequence=4, offset=2)

functions_yaml = sys.argv[1]
hooks_yaml = sys.argv[2]
md_dir = sys.argv[3]

base_url = "sfall-wiki\\"

# template for functions pages
function_header_template = '''---
layout: page
title: '{name}' # quote just in case
{has_children}
# parent - could be empty
{grand_parent}
{parent}
permalink: {permalink}
has_toc: false
nav_order: 10
---

# {name}
{{: .no_toc}}
'''

# template for hooks types page - hardcoded
hooks_header = '''---
layout: page
title: Типы кючков
#nav_order: 6
parent: Крючки (Hooks)
permalink: /hook-types/
---

# Hook types
{: .no_toc}

* TOC
{:toc}
---
'''

def get_slug(string):
  return string.lower().replace(' ','-').replace(':','-').replace('/','-').replace('--','-')

# functions pages
with open(functions_yaml) as yf:
  data = yaml.load(yf)
  for cat in data: # list categories
    text = ""

    # check for childre
    has_children = ""
    children = [x for x in data if "parent" in x and x["parent"] == cat["name"]]
    if len(children) > 0 or 'has_children' in cat and cat['has_children'] is True:
      has_children = "has_children: true"

    # used in filename and permalink
    slug = get_slug(cat['name'])

    grand_parent = ""
    if 'grand_parent' in cat:
      grand_parent = "grand_parent: " + cat['grand_parent']

    # if parent is present, this is a subcategory
    parent = ""
    if 'parent' in cat:
      parent = "parent: " + cat['parent']

    if 'permalink' in cat:
      slug = get_slug(cat['permalink'])

    text += function_header_template.format(name=cat['name'], grand_parent=grand_parent, parent=parent, has_children=has_children, permalink="/{}/".format(slug))

    # common doc for category
    if 'doc' in cat:
      text = text + '\n' + cat['doc'] + '\n'

    if len(children) > 0:
      #children = sorted(children, key=lambda k: k['name'])
      text += "\n## Подкатегории\n{: .no_toc}\n\n"
      for c in children:
        subparent = base_url
        if 'permalink' in c:
          subparent += get_slug(c['permalink'])
        else:
          subparent += get_slug(c["name"])
        text += "- [**{}**](/{}/)\n".format(c["name"], subparent)
      text += "\n"

    if 'items' in cat: # allow parent pages with no immediate items
      text += "## Функции\n{: .no_toc}\n\n"
      text += "* TOC\n{: toc}\n"
      # individual functions
      items = cat['items']
      items = sorted(items, key=lambda k: k['name'])

      for i in items:
        # header
        text += "\n---\n\n### **{}**\n".format(i['name'])
        # macro label
        if 'macro' in i:
          text += "{: .d-inline-block }\n" + format(i['macro']) + "\n{: .label .label-green }\n"
        # unsafe label
        if 'unsafe' in i and i['unsafe'] is True:
          text += '{: .d-inline-block }\nUNSAFE\n{: .label .label-red }\n'
        # usage
        text += "```c\n{}\n```\n".format(i['detail'].rstrip())
        # doc, if present
        if 'doc' in i:
          text += i['doc'] + '\n'

    md_path = os.path.join(md_dir, slug + ".md")
    with open(md_path, 'w') as f:
      f.write(text)


# hook types page
with open(hooks_yaml) as yf:
  hooks = yaml.load(yf)
  hooks = sorted(hooks, key=lambda k: k['name']) # alphabetical sort
  text = hooks_header

  for h in hooks:
    name = h['name']
    doc = h['doc']
    try:
      hid = h['id']
    except:
      hid = "HOOK_" + name.upper()
    if 'filename' in h: # overriden filename?
      filename = h['filename']
    else:
      filename = "hs_" + name.lower() + ".int"

    text += "\n## {}\n\n".format(name) # header
    if filename != "": # if not skip
      text += "`{}` ({})\n\n".format(hid, filename) # `HOOK_SETLIGHTING` (hs_setlighting.int)
    text += doc # actual documentation

    md_path = os.path.join(md_dir, "hook-types.md")
    with open(md_path, 'w') as f:
      f.write(text)
