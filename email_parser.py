import html5_parser
from beautifultable import BeautifulTable


def look_for_outermost_tag(root, tag_name, initial_caller=True):
    """
    Look for the outermost tag in a bunch of HTML
    :param root: The root <html> node
    :param tag_name: The name of the node you're searching for
    :param initial_caller: True.
    :return: The appropriate Node
    """
    if root.tag == tag_name and not initial_caller:
        return root
    if len(root) == 0:
        return None
    else:
        for child in root:
            maybe_table = look_for_outermost_tag(child, tag_name, False)
            if maybe_table is not None:
                return maybe_table
        else:
            return None


def flatten_text_in_td(root):
    """
    Given an HTML tag, turn it into a string (i.e what a user may read if it was rendered)
    :param root: The node to flatten
    :return: The text that the tag represents OR a beautifultable, if the node contained a table.
    """
    text = ""
    if root.text is not None:
        text += root.text + " "

    if root.tag == 'tbody':
        return table_to_beautifultable(root)

    for child in root:
        child_text = flatten_text_in_td(child)
        if type(child_text) == str:
            text += child_text
        elif type(child_text) == BeautifulTable:
            return child_text
        else:
            raise Exception(type(child_text))

    if root.tail is not None:
        text += root.tail + " "
    return str(text.strip().replace("\t", ""))


def table_to_beautifultable(root):
    assert root.tag == 'tbody'

    bt_table = BeautifulTable()

    for child in root:
        assert child.tag == 'tr'
        row = []
        for data in child:
            assert data.tag == 'td'
            row.append(flatten_text_in_td(data))

        bt_table.append_row(row)

    return bt_table


def parse_email(email_string):
    """
    Given the raw HTML that makes up a GrabCAD notification email, turn it into an ASCII table that is mildly human readable
    :param email_string: The raw HTML of the email
    :return: *preformatted text* that goes into Slack
    """
    root = html5_parser.parse(email_string)

    for child in root:
        if child.tag == 'body':
            body = child
            break
    else:
        raise Exception("body not found??")

    table = look_for_outermost_tag(body, 'td')

    email_content_tbody = table[0][0][1][0][0][0]

    return str(table_to_beautifultable(email_content_tbody))
