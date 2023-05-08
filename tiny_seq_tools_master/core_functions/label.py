import textwrap

def split_lines(context, text, parent, split=.5):
    chars = int(context.region.width*split)   # 7 pix on 1 character
    wrapper = textwrap.TextWrapper(width=chars)
    text_lines = wrapper.wrap(text=text)
    for line in text_lines:
        parent.label(text=line)
