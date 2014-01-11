# coding: utf-8

import re

tpl = open('index.tpl', 'r')
src = open('slides.md', 'r')
out = open('index.html', 'w')

tpl_content = tpl.read()
src_content = src.read()
out_content = re.sub(r'__SOURCE__', src_content, tpl_content)
out.write(out_content)
out.close()
src.close()
tpl.close()
