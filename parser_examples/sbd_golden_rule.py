import unittest
from sent_seg import spacy_sbd, py_sbd

# use spacy sbd
test_fun = spacy_sbd

# use pySBD
# test_fun = py_sbd


class TestStringMethods(unittest.TestCase):

    # Simple period to end sentence
    def test_sent1(self):
        text = "Hello World. My name is Jonas."
        self.assertEqual(test_fun(text), ["Hello World.", "My name is Jonas."])

    # Question mark to end sentence
    def test_sent2(self):
        text = "What is your name? My name is Jonas."
        self.assertEqual(test_fun(text), ["What is your name?", "My name is Jonas."])

    # Exclamation point to end sentence
    def test_sent3(self):
        text = "There it is! I found it."
        self.assertEqual(test_fun(text), ["There it is!", "I found it."])

    # One letter upper case abbreviations
    def test_sent4(self):
        text = "My name is Jonas E. Smith."
        self.assertEqual(test_fun(text), ["My name is Jonas E. Smith."])

    # One letter lower case abbreviations
    def test_sent5(self):
        text = "Please turn to p. 55."
        self.assertEqual(test_fun(text), ["Please turn to p. 55."])

    # Two letter lower case abbreviations in the middle of a sentence
    def test_sent6(self):
        text = "Were Jane and co. at the party?"
        self.assertEqual(test_fun(text), ["Were Jane and co. at the party?"])

    # Two letter upper case abbreviations in the middle of a sentence
    def test_sent7(self):
        text = "They closed the deal with Pitt, Briggs & Co. at noon."
        self.assertEqual(test_fun(text), ["They closed the deal with Pitt, Briggs & Co. at noon."])

    # Two letter lower case abbreviations at the end of a sentence
    def test_sent8(self):
        text = "Let's ask Jane and co. They should know."
        self.assertEqual(test_fun(text), ["Let's ask Jane and co.", "They should know."])

    # Two letter upper case abbreviations at the end of a sentence
    def test_sent9(self):
        text = "They closed the deal with Pitt, Briggs & Co. It closed yesterday."
        self.assertEqual(test_fun(text), ["They closed the deal with Pitt, Briggs & Co.", "It closed yesterday."])

    # Two letter (prepositive) abbreviations
    def test_sent10(self):
        text = "I can see Mt. Fuji from here."
        self.assertEqual(test_fun(text), ["I can see Mt. Fuji from here."])

    # Two letter (prepositive & postpositive) abbreviations
    def test_sent11(self):
        text = "St. Michael's Church is on 5th st. near the light."
        self.assertEqual(test_fun(text), ["St. Michael's Church is on 5th st. near the light."])

    # Possesive two letter abbreviations
    def test_sent12(self):
        text = "That is JFK Jr.'s book."
        self.assertEqual(test_fun(text), ["That is JFK Jr.'s book."])

    # Multi-period abbreviations in the middle of a sentence
    def test_sent13(self):
        text = "I visited the U.S.A. last year."
        self.assertEqual(test_fun(text), ["I visited the U.S.A. last year."])

    # Multi-period abbreviations at the end of a sentence
    def test_sent14(self):
        text = "I live in the E.U. How about you?"
        self.assertEqual(test_fun(text), ["I live in the E.U.", "How about you?"])

    # U.S. as sentence boundary
    def test_sent15(self):
        text = "I live in the U.S. How about you?"
        self.assertEqual(test_fun(text), ["I live in the U.S.", "How about you?"])

    # U.S. as non sentence boundary with next word capitalized
    def test_sent16(self):
        text = "I work for the U.S. Government in Virginia."
        self.assertEqual(test_fun(text), ["I work for the U.S. Government in Virginia."])

    # U.S. as non sentence boundary
    def test_sent17(self):
        text = "I have lived in the U.S. for 20 years."
        self.assertEqual(test_fun(text), ["I have lived in the U.S. for 20 years."])

    # .M. / P.M. as non sentence boundary and sentence boundary
    def test_sent18(self):
        text = "At 5 a.m. Mr. Smith went to the bank. He left the bank at 6 P.M. Mr. Smith then went to the store."
        self.assertEqual(test_fun(text), ["At 5 a.m. Mr. Smith went to the bank.", "He left the bank at 6 P.M.", "Mr. Smith then went to the store."])

    # Number as non sentence boundary
    def test_sent19(self):
        text = "She has $100.00 in her bag."
        self.assertEqual(test_fun(text), ["She has $100.00 in her bag."])

    # 20) Number as sentence boundary
    def test_sent20(self):
        text = "She has $100.00. It is in her bag."
        self.assertEqual(test_fun(text),["She has $100.00.", "It is in her bag."])

    # Parenthetical inside sentence
    def test_sent21(self):
        text = "He teaches science (He previously worked for 5 years as an engineer.) at the local University."
        self.assertEqual(test_fun(text), ["He teaches science (He previously worked for 5 years as an engineer.) at the local University."])

    #  Email addresses
    def test_sent22(self):
        text = "Her email is Jane.Doe@example.com. I sent her an email."
        self.assertEqual(test_fun(text), ["Her email is Jane.Doe@example.com.", "I sent her an email."])

    # Web addresses
    def test_sent23(self):
        text = "The site is: https://www.example.50.com/new-site/awesome_content.html. Please check it out."
        self.assertEqual(test_fun(text),
                         ["The site is: https://www.example.50.com/new-site/awesome_content.html.", "Please check it out."])

    # Single quotations inside sentence
    def test_sent24(self):
        text = "She turned to him, 'This is great.' she said."
        self.assertEqual(test_fun(text),
                         ["She turned to him, 'This is great.' she said."])

    # Double quotations inside sentence
    def test_sent25(self):
        text = "She turned to him, 'This is great.' she said."
        self.assertEqual(test_fun(text),
                         ["She turned to him, 'This is great.' she said."])

    # Double quotations at the end of a sentence
    def test_sent26(self):
        text = "She turned to him, 'This is great.' She held the book out to show him."
        self.assertEqual(test_fun(text),
                         ["She turned to him, 'This is great.'", "She held the book out to show him."])

    # Double punctuation (exclamation point)
    def test_sent27(self):
        text = "Hello!! Long time no see."
        self.assertEqual(test_fun(text),
                         ["Hello!!", "Long time no see."])

    # Double punctuation (question mark)
    def test_sent28(self):
        text = "Hello?? Who is there?"
        self.assertEqual(test_fun(text),
                         ["Hello??", "Who is there?"])

    # Double punctuation (exclamation point / question mark)
    def test_sent29(self):
        text = "Hello!? Is that you?"
        self.assertEqual(test_fun(text),
                         ["Hello!?", "Is that you?"])

    # Double punctuation (question mark / exclamation point)
    def test_sent30(self):
        text = "Hello?! Is that you?"
        self.assertEqual(test_fun(text),
                         ["Hello?!", "Is that you?"])

    # List (period followed by parens and no period to end item)
    def test_sent31(self):
        text = "1.) The first item 2.) The second item"
        self.assertEqual(test_fun(text),
                         ["1.) The first item", "2.) The second item"])

    # List (period followed by parens and period to end item)
    def test_sent32(self):
        text = "1.) The first item. 2.) The second item."
        self.assertEqual(test_fun(text),
                         ["1.) The first item.", "2.) The second item."])

    # List (parens and no period to end item)
    def test_sent33(self):
        text = "1) The first item 2) The second item"
        self.assertEqual(test_fun(text),
                         ["1) The first item", "2) The second item"])

    # List (parens and period to end item)
    def test_sent34(self):
        text = "1) The first item. 2) The second item."
        self.assertEqual(test_fun(text),
                         ["1) The first item.", "2) The second item."])

    # List (period to mark list and no period to end item)
    def test_sent35(self):
        text = "1. The first item 2. The second item"
        self.assertEqual(test_fun(text),
                         ["1. The first item", "2. The second item"])

    # List (period to mark list and period to end item)
    def test_sent36(self):
        text = "1. The first item. 2. The second item."
        self.assertEqual(test_fun(text),
                         ["1. The first item.", "2. The second item."])

    # List with bullet
    def test_sent37(self):
        text = "â€¢ 9. The first item â€¢ 10. The second item"
        self.assertEqual(test_fun(text),
                         ["â€¢ 9. The first item", "â€¢ 10. The second item"])

    # List with hypthen
    def test_sent38(self):
        text = "âƒ9. The first item âƒ10. The second item"
        self.assertEqual(test_fun(text),
                         ["âƒ9. The first item", "âƒ10. The second item"])

    # Alphabetical list
    def test_sent39(self):
        text = "a. The first item b. The second item c. The third list item"
        self.assertEqual(test_fun(text),
                         ["a. The first item", "b. The second item", "c. The third list item"])

    # Errant newlines in the middle of sentences (PDF)
    def test_sent40(self):
        text = "This is a sentence\ncut off in the middle because pdf."
        self.assertEqual(test_fun(text),
                         ["This is a sentence cut off in the middle because pdf."])

    # Errant newlines in the middle of sentences
    def test_sent41(self):
        text = "It was a cold \nnight in the city."
        self.assertEqual(test_fun(text),
                         ["It was a cold night in the city."])

    # Lower case list separated by newline
    def test_sent42(self):
        text = "features\ncontact manager\nevents, activities\n"
        self.assertEqual(test_fun(text),
                         ["features", "contact manager", "events, activities"])

    # Geo Coordinates
    def test_sent43(self):
        text = "You can find it at NÂ°. 1026.253.553. That is where the treasure is."
        self.assertEqual(test_fun(text),
                         ["You can find it at NÂ°. 1026.253.553.", "That is where the treasure is."])

    # Named entities with an exclamation point
    def test_sent44(self):
        text = "She works at Yahoo! in the accounting department."
        self.assertEqual(test_fun(text),
                         ["She works at Yahoo! in the accounting department."])

    # I as a sentence boundary and I as an abbreviation
    def test_sent45(self):
        text = "We make a good team, you and I. Did you see Albert I. Jones yesterday?"
        self.assertEqual(test_fun(text),
                         ["We make a good team, you and I.", "Did you see Albert I. Jones yesterday?"])

    # Ellipsis at end of quotation
    def test_sent46(self):
        text = "Thoreau argues that by simplifying oneâ€™s life, â€œthe laws of the universe will appear less complex. . . .â€"
        self.assertEqual(test_fun(text),
                         ["Thoreau argues that by simplifying oneâ€™s life, â€œthe laws of the universe will appear less complex. . . .â€"])

    # Ellipsis with square brackets
    def test_sent47(self):
        text = "'Bohr [...] used the analogy of parallel stairways [...]' (Smith 55)."
        self.assertEqual(test_fun(text),
                         ["'Bohr [...] used the analogy of parallel stairways [...]' (Smith 55)."])

    # Ellipsis as sentence boundary (standard ellipsis rules)
    def test_sent48(self):
        text = "If words are left off at the end of a sentence, and that is all that is omitted, indicate the omission with ellipsis marks (preceded and followed by a space) and then indicate the end of the sentence with a period . . . . Next sentence."
        self.assertEqual(test_fun(text),
                         ["If words are left off at the end of a sentence, and that is all that is omitted, indicate the omission with ellipsis marks (preceded and followed by a space) and then indicate the end of the sentence with a period . . . .", "Next sentence."])

    # Ellipsis as sentence boundary (non-standard ellipsis rules)
    def test_sent49(self):
        text = "I never meant that.... She left the store."
        self.assertEqual(test_fun(text),
                         ["I never meant that....", "She left the store."])

    # Ellipsis as non sentence boundary
    def test_sent50(self):
        text = "I wasnâ€™t really ... well, what I mean...see . . . what I'm saying, the thing is . . . I didnâ€™t mean it."
        self.assertEqual(test_fun(text),
                         ["I wasnâ€™t really ... well, what I mean...see . . . what I'm saying, the thing is . . . I didnâ€™t mean it."])

    # 4-dot ellipsis
    def test_sent51(self):
        text = "One further habit which was somewhat weakened . . . was that of combining words into self-interpreting compounds. . . . The practice was not abandoned. . . ."
        self.assertEqual(test_fun(text),
                         ["One further habit which was somewhat weakened . . . was that of combining words into self-interpreting compounds.", ". . . The practice was not abandoned. . . ."])


if __name__ == '__main__':
    unittest.main()
