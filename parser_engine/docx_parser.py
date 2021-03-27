from docx import Document
import pysbd


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

        # header & one sentence paragraph
        if len(sentences) == 1:
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
    segments = docx_parser(filepath='/home/ywang/SSApp/static/docxs/Banco Pop Exhibit - Required Insurance BP v. 12.14.18.docx')
