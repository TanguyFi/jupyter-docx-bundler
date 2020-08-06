from pathlib import Path
import re

import pypandoc

from .. import converters


def test_notebookcontent_to_docxbytes(test_notebook):
    converters.notebookcontent_to_docxbytes(
        test_notebook, 'test-notebook', test_notebook['metadata']['path'],
    )


def test_image_conversion(tmpdir, images_notebook):
    # convert notebook to docx
    docxbytes = converters.notebookcontent_to_docxbytes(
        images_notebook, 'test-notebook', images_notebook['metadata']['path'],
    )

    # write to file on disk
    filename = tmpdir / 'images-notebook.docx'
    with open(filename, 'wb') as file:
        file.write(docxbytes)

    # convert to markdown and extract media
    pypandoc.convert_file(
        f'{filename}',
        'markdown',
        'docx',
        extra_args=['--extract-media', f'{tmpdir}'],
        outputfile=f'{tmpdir / "images-notebook.md"}',
    )

    # compare number of extracted media with generated media
    media = list(Path(tmpdir / 'media').glob('*.*'))
    assert images_notebook['metadata']['image_count'] == len(media),\
        'Number of generated images does not match in docx-document.'


def test_remove_input(tmpdir, remove_input_notebook):
    # convert notebook to docx
    docxbytes = converters.notebookcontent_to_docxbytes(
        remove_input_notebook, 'test-notebook', remove_input_notebook['metadata']['path'],
    )

    # write to file on disk
    filename = tmpdir / 'images-notebook.docx'
    outfilename = tmpdir / 'remove-input-notebook.md'
    with open(filename, 'wb') as file:
        file.write(docxbytes)

    # convert to markdown and read text
    pypandoc.convert_file(
        f'{filename}',
        'markdown',
        'docx',
        outputfile=f'{outfilename}',
    )
    with open(outfilename, 'r') as file:
        lines = file.readlines()

    # Check for the occurence of code
    assert len(re.findall('print(.*Hide my input!.*)', ''.join(lines))) == 0, 'Input not hided.'


def test_remove_cell(tmpdir, remove_cell_notebook):
    # convert notebook to docx
    docxbytes = converters.notebookcontent_to_docxbytes(
        remove_cell_notebook, 'test-notebook', remove_cell_notebook['metadata']['path'],
    )

    # write to file on disk
    filename = tmpdir / 'images-notebook.docx'
    outfilename = tmpdir / 'remove-cell-notebook.md'
    with open(filename, 'wb') as file:
        file.write(docxbytes)

    # convert to markdown and read text
    pypandoc.convert_file(
        f'{filename}',
        'markdown',
        'docx',
        outputfile=f'{outfilename}',
    )
    with open(outfilename, 'r') as file:
        lines = file.readlines()

    # Check for the occurence of code
    assert len(re.findall('Hide me!', ''.join(lines))) == 0, 'Cell not hided.'
