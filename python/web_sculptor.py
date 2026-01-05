import re
import os
import argparse

class MarkSculpt:
    """A minimal Markdown to HTML converter."""
    def __init__(self):
        self.rules = [
            (r'^# (.*)$', r'<h1>\1</h1>'),
            (r'^## (.*)$', r'<h2>\1</h2>'),
            (r'^### (.*)$', r'<h3>\1</h3>'),
            (r'\*\*(.*?)\*\*', r'<strong>\1</strong>'),
            (r'\*(.*?)\*', r'<em>\1</em>'),
            (r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1">'),
            (r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>'),
            (r'^- (.*)$', r'<li>\1</li>'),
            (r'^> (.*)$', r'<blockquote>\1</blockquote>'),
            (r'`(.*?)`', r'<code>\1</code>'),
        ]

    def convert(self, md_text):
        html_lines = []
        in_list = False
        
        for line in md_text.split('\n'):
            line = line.strip()
            
            # List processing
            if line.startswith('- '):
                if not in_list:
                    html_lines.append('<ul>')
                    in_list = True
            elif in_list:
                html_lines.append('</ul>')
                in_list = False

            # Apply regex rules
            processed = False
            for pattern, replacement in self.rules:
                new_line = re.sub(pattern, replacement, line)
                if new_line != line:
                    html_lines.append(new_line)
                    processed = True
                    break
            
            if not processed:
                if line == "":
                    html_lines.append('<br>')
                else:
                    html_lines.append(f'<p>{line}</p>')
        
        if in_list:
            html_lines.append('</ul>')
            
        return self._wrap_html('\n'.join(html_lines))

    def _wrap_html(self, body):
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MarkSculpt Preview</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 40px auto; padding: 20px; background: #f9f9f9; }}
        h1, h2, h3 {{ color: #2c3e50; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
        code {{ background: #eee; padding: 2px 5px; border-radius: 3px; font-family: monospace; }}
        blockquote {{ border-left: 5px solid #ccc; margin: 20px 0; padding: 10px 20px; color: #666; font-style: italic; }}
        a {{ color: #3498db; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        strong {{ color: #e74c3c; }}
    </style>
</head>
<body>
{body}
</body>
</html>"""

def main():
    parser = argparse.ArgumentParser(description="MarkSculpt: Markdown to Styled HTML")
    parser.add_argument("input", help="Path to input markdown file")
    parser.add_argument("--output", "-o", help="Path to output html file", default="preview.html")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"❌ Error: File '{args.input}' not found.")
        return

    with open(args.input, "r", encoding="utf-8") as f:
        md_content = f.read()

    sculptor = MarkSculpt()
    html_content = sculptor.convert(md_content)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"🎨 Success! Markdown converted to: {args.output}")

if __name__ == "__main__":
    main()
