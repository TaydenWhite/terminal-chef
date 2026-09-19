"""Box rendering engine.

Every menu is a Box: a title bar (one or more segments, each padded by two
spaces) sitting on top of a body made of sections. Body width is the widest
body line, never narrower than the title bar. When the body is wider than the
title the join line ends in a backslash pair, otherwise in a bar pair.
"""

MARGIN = '   '  # every printed line starts with a three-space margin


class Line:
    """One body row. Subclasses know their natural width and how to fill a width."""

    def natural(self):
        raise NotImplementedError

    def render(self, width):
        raise NotImplementedError


class L(Line):
    """Left-aligned text. The text carries its own leading spaces."""

    def __init__(self, text):
        self.text = text

    def natural(self):
        return len(self.text) + 2

    def render(self, width):
        return self.text.ljust(width)


class LR(Line):
    """Left text plus a value right-aligned two spaces before the border."""

    def __init__(self, left, right):
        self.left, self.right = left, right

    def natural(self):
        return len(self.left) + 4 + len(self.right) + 2

    def render(self, width):
        gap = width - len(self.left) - len(self.right) - 2
        return self.left + ' ' * gap + self.right + '  '


class C(Line):
    """Centered text. Odd leftover space goes to the right."""

    def __init__(self, text):
        self.text = text

    def natural(self):
        return len(self.text) + 4

    def render(self, width):
        return center(self.text, width)


class Cells(Line):
    """Equal-width cells separated by '||', each with centered content."""

    def __init__(self, *cells):
        self.cells = list(cells)

    def natural(self):
        n = len(self.cells)
        return n * (max(len(c) for c in self.cells) + 4) + 2 * (n - 1)

    def render(self, width):
        n = len(self.cells)
        inner = width - 2 * (n - 1)
        widths = [inner // n] * n
        widths[-1] += inner - sum(widths)
        return '||'.join(center(c, w) for c, w in zip(self.cells, widths))


def center(text, width):
    pad = width - len(text)
    left = pad // 2
    return ' ' * left + text + ' ' * (pad - left)


def numbered(n, text=''):
    """'    1) text' with the number right-aligned so 10) lines up with 9)."""
    return f'   {n:>2}) {text}'.rstrip()


class Box:
    def __init__(self, title, sections=(), title_extra=()):
        self.segments = [title] if isinstance(title, str) else list(title)
        self.sections = [list(s) for s in sections]
        self.title_extra = list(title_extra)  # centered lines inside the title tier

    def lines(self):
        title = '||'.join(f'  {s}  ' for s in self.segments)
        t = len(title)
        out = ['//' + '=' * t + '\\\\', '||' + title + '||']
        for extra in self.title_extra:
            out.append('||' + '=' * t + '||')
            out.append('||' + center(extra, t) + '||')
        if not self.sections:
            out.append('\\\\' + '=' * t + '//')
            return out
        w = max([t] + [ln.natural() for s in self.sections for ln in s])
        out.append('||' + '=' * w + ('\\\\' if w > t else '||'))
        for i, section in enumerate(self.sections):
            if i:
                out.append('||' + '=' * w + '||')
            out.extend('||' + ln.render(w) + '||' for ln in section)
        out.append('\\\\' + '=' * w + '//')
        return out

    def render(self):
        return '\n'.join(MARGIN + ln for ln in self.lines())
