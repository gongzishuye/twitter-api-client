import re


text = '如上篇關於 @protocol_fx 的介紹，$xETH我認為 f(x) 的核心是圍繞在 $fETH 上，並透過 $xETH 的輔助，來做到...'
pattern = r"\$([a-zA-Z0-9_]+)"
match = re.findall(pattern, text)
if match:
    print(match)