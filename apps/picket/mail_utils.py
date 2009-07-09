"""
Copyright 2009 Serge Matveenko

This file is part of Picket.

Picket is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Picket is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Picket.  If not, see <http://www.gnu.org/licenses/>.
"""

from django.utils.html import strip_tags

def markdown_from_part(part):
    if part.get_content_subtype() == 'html':
        return '\n\r%s\n\r' % part.get_payload(decode=True)
    else:
        return '\n\r<pre>%s</pre>\n\r' % part.get_payload(decode=True)

def text_from_part(part):
    if part.get_content_subtype() == 'html':
        return strip_tags(part.get_payload(decode=True))
    else:
        return part.get_payload(decode=True)

def decode(hdr):
    import chardet
    from email import header

    result = []
    for text, enc in header.decode_header(hdr):
        enc = enc if enc else chardet.detect(text)['encoding']
        result.append(unicode(text.decode(enc)) if enc else unicode(text))

    return ''.join(result)
