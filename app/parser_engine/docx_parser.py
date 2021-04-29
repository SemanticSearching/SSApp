from docx import Document
import pysbd
import re
import mammoth

def sents_preprocessor(sents: list):
    new_sents = []
    for sent in sents:
        if sent == 'AND':
            continue
        elif sent == 'and':
            continue
        elif sent == 'AND\t':
            continue
        elif sent == 'BETWEEN':
            continue

        # remove redundant spaces
        sent = re.sub(' +', ' ', sent)

        new_sents.append(sent)

    return new_sents

def segment_clipper(segment: list, max_words: int=100):
    """

    :param max_words:
    :param segment: list of sentences,["sent1", "sent2", "sent3", ...]
    :return: list: list of sentences that have total of words less than maximum_words
    """
    total_words = 0
    for i, sent in enumerate(segment):
        word_count = len(sent.split(' '))
        total_words += word_count

        if (total_words > max_words) and (i > 0):
            segment = segment[:i]
            break

    return segment

def docx_parser(filepath: str, sliding_window: int =3, max_words: int=100):
    """
    parser a given docx
    Args:
        :param filepath: path to the docs for parsing
        :param sliding_window: maximum number of sentences in each segment
        :param max_words: maximum number of words in each sentences (split by ' ')

    Returns: a list of list of sentences [["sent1", "sent2", "sent3", ...], # Segment1
                                          ["sent1", "sent2", "sent3", ...], # Segment2
                                          ...]

    requirements (03/22):
        - Header as a single segment
        - Three sentences per segment
        - Split paragraphs
        - Maximum 100 words per segment (delete sentences if it is longer)

    """
    document = Document(filepath)
    segmenter = pysbd.Segmenter(language="en", clean=False)
    segs = []

    for paragraph in document.paragraphs:

        sentences = segmenter.segment(paragraph.text)
        sentences = sents_preprocessor(sentences)

        if sentences:
            # header & one sentence paragraph
            if len(sentences) <= sliding_window:
                segs.append(sentences)
            else:
                # long paragraph
                end_idx = len(sentences) - 1
                for i in range(len(sentences)):
                    if i + sliding_window <= end_idx:
                        seg = segment_clipper(sentences[i: i+sliding_window], max_words)
                        segs.append(seg)

                        if (i + sliding_window == end_idx) and (len(seg) == sliding_window):
                            break
                    else:
                        seg = segment_clipper(sentences[i:], max_words)
                        segs.append(seg)

    return segs

if __name__ == '__main__':
    # Debug
    # segments = docx_parser(filepath='/home/ywang/SSApp/app/static/docxs/InformationSecurityRequirements.docx')
    # segments = docx_parser(filepath='/home/ywang/SSApp/static/docxs/BancoPopExhibit.docx')
    # segments = docx_parser(filepath='/home/ywang/SSApp/static/docxs/JLL_SAICContract.docx')
    # segments = docx_parser(filepath='/home/ywang/SSApp/static/docxs/NGXeroxeMPS.docx')

    with open("/home/ywang/SSApp/app/static/docxs/InformationSecurityRequirements.docx", "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        html = result.value  # The generated HTML
        print('done')