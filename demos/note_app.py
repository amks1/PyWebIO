from pywebio import start_server

from pywebio.output import *
from pywebio.input import *
from pywebio.pin import *
from pywebio.session import set_env, download, hold
import os
import os.path as op
from functools import partial

NOTE_HOME = op.join(op.expanduser("~"), 'pywebio-notes-app')


@page(silent_quit=True)
def note_editor(file):
    set_env(title=file)
    if not op.exists(op.join(NOTE_HOME, file)):
        open(op.join(NOTE_HOME, file), 'w')

    with open(op.join(NOTE_HOME, file), 'r+') as f:
        md = f.read()
        put_textarea('md_text', rows=18, code={'mode': 'markdown'}, value=md)

        put_markdown('## Preview')
        with use_scope('md', clear=True):
            put_markdown(md)

        while True:
            change_detail = pin_wait_change('md_text')
            with use_scope('md', clear=True):
                f.truncate(0)  # empty the file
                f.write(change_detail['value'])
                put_markdown(change_detail['value'], sanitize=False)


@page()
def note_viewer(file):
    set_env(title=file)

    md = open(op.join(NOTE_HOME, file)).read()
    put_markdown(md)

    put_button("Edit", lambda: note_editor(file))
    hold()


def main():
    """PyWebIO Markdown Notes Application"""
    set_env(output_animation=False)
    files = [
        f
        for f in os.listdir(NOTE_HOME)
        if op.isfile(op.join(NOTE_HOME, f)) and f.endswith('.md')
    ]

    put_button("New Note", lambda: note_editor(input("Note name")))

    if not files:
        put_info("No existing notes found")
    else:
        put_table([
            (
                idx,
                put_button(name, partial(note_viewer, name), link_style=True),
                put_buttons(['Edit', 'Delete'], [partial(note_editor, name), None])
            )
            for idx, name in enumerate(files, start=1)
        ])


if __name__ == '__main__':
    if not op.exists(NOTE_HOME):
        os.makedirs(NOTE_HOME, exist_ok=True)

    start_server(main, port=8080, debug=True, cdn=False)
