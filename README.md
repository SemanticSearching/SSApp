# Install Env
```angular2html
conda env create -f py38.pml
```
# master branch
Very basic pipline which uses googleviewer to show doc files.
# html branch
## APIs
### [pySBD](https://github.com/nipunsadvilkar/pySBD)
**pySBD** is a sentence boundary disambiguate api which supports 22 languages. In the original [paper](chrome-extension://oemmndcbldboiebfnladdacbdfmadadm/https://www.aclweb.org/anthology/2020.nlposs-1.15.pdf),
they use [Golden Rules](https://s3.amazonaws.com/tm-town-nlp-resources/golden_rules.txt) to measure the performance of their SBD.

In */parser_examples/sbd_golden_rule.py*, you can choose to test SpaCy SBD or pySBD on the english golden rules. For pySBD,
the accuracy is 45/51. The accuracy of SpaCy SBD is 24/51. In pySBD paper, they got a higher accuracy than 45/51 on
golden rules. I haven't figure out why we get a lower accuracy.

## [mammoth](https://pypi.org/project/mammoth/)
**mammoth** is an api to parser .docx files. It can be also used to convert .docx file to htmls.
In */parser_examples/parser.py*, I list some examples to extract the paragraphs and headings.

## Parser Interface
Like the function *text_from_html* in file */parser_engine/htmlparser.py*, the parser interface takes one file path *filepath*
as input and outputs a list of windows:
```python
def docx_parser(filepath):
    """
    parser a given docx
    Args:
        filepath: the path of the .docx file

    Returns: a list of windows each of which is a list of sents:
    [["sent1", "sent2", "sent3"], ["sent1", "sent2", "sent3"] ...]

    """
```
### Window
+ consists of three sentences
+ no more than 100 words, if not, delete one sentence until it has no more then 100 words
+ each heading is one window
+ the three sentences in one window should in the same paragraph

I create a new branch on html branch and add docx_parser.py under parser_engine folder. You can implement the docx_parser function in it.


# Deploy to Server
## Install Packages
```angular2html
sudo apt update
sudo apt install apache2
sudo apt-get install libapache2-mod-wsgi-py3
```

## Configure Site
```angular2html
sudo ln -sT /project/path/of/website /var/www/html/website
```
