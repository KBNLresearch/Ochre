import click

from lxml import etree


@click.command()
@click.argument('in_file', type=click.Path(exists=True))
def create_corpus(in_file):
    quote = '{http://ilk.uvt.nl/folia}quote'

    ocr_text = []
    gold_standard = []
    has_ocroutput = []
    ocr_word = None
    prev_parent = None

    # TODO: how to handle headings? They are sentences without a closing
    # punctuation mark.
    # I think the existing LSTM code does not take into account documents (all
    # text is simply concatenated together).

    context = etree.iterparse(in_file, tag='{http://ilk.uvt.nl/folia}w')
    for action, elem in context:
        parent = elem.getparent().tag
        for t in elem.iterchildren(tag='{http://ilk.uvt.nl/folia}t'):
            if t.get('class') == 'ocroutput':
                ocr_word = t.text
            else:
                gs_word = t.text

        if ocr_word:
            space = True
            ocr_text.append(ocr_word)
        # Add a space if the word is a " and it is the start of a quote.
        # Otherwise, the " will be stuck to the previous word (which it should
        # be if it is the end of the quote or any othe punctuation mark).
        elif gs_word == '"' and parent == quote and prev_parent != qoute:
            space = True
        else:
            space = False

        if space:
            gold_standard.append(' ')
        gold_standard.append(gs_word)
        ocr_word = None
        space = False
        prev_parent = parent

    # We need to normalize ' " ' in the gold standard to ' "', because we have
    # introduced an additional space.
    print 'Gold standard'
    print ''.join(gold_standard).replace(' " ', ' "').strip()
    print
    print 'OCR text'
    print ' '.join(ocr_text)

if __name__ == '__main__':
    create_corpus()