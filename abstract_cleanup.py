'''
This file consists of functions that helps clean up abstracts with errors found in QC.
'''

import re

def cleanup_pretagger_all(text):
    '''
    WRapper function that calls all the functions that should be used pre tagging
    '''
    # Add + at the start to make [0] a non-letter
    text = '+' + text
    # Replace ampredand
    text = text.replace('&amp;', '')  # sometimes & is coded as '&amp;'
    text = text.replace('&', '')
    text = text.replace('e.g.', '')
    text = text.replace('i.e.', '')
    text = text.replace('[?]', '')
    text = cleanup_text_ends_with_letters(text)
    text = cleanup_latin_names(text)
    text = cleanup_sentence_ends_with_etc(text)
    text = cleanup_remove_genes(text)
    text = cleanup_remove_decimal_numbers(text)
    text = cleanup_replace_hyphens(text)
    text = cleanup_remove_abrevs(text)
    text = cleanup_one_letter_words(text)
    text = cleanup_sentence_ends_in_number(text)
    text = cleanup_copyright_sentences(text)
    text = cleanup_sentence_with_missing_spaces(text)
    text = cleanup_remove_one_word_sentences(text)
    text = cleanup_add_space_after_period(text)
    text = cleanup_remove_extra_white_spaces(text)
    text = cleanup_multi_white_spaces(text)
    text = cleanup_split_nsf_verbage(text)
    text = cleanup_remove_html_tags(text)
    text = text.replace(r"*** //", '')

    # Remove + at the start
    # (if it is still there - gets removed if the first word was an abbreviation)
    if text[0] == '+':
        text = text[1:]
    return text

def cleanup_posttagger_all(text):
    '''
    Occaionally treetagger can parse strange abbreviations "e. g." as "e"
    being its own word. Remove these.
    '''
    text = cleanup_one_letter_words(text)
    text = text.replace('replaced-url', '')
    return text

def cleanup_sentence_ends_in_number(text):
    '''
    Correct occrances of "1230. New sentence" as treetagger will remove "1230." not just "1230"
    Find number occurances this occurs
    '''
    restr = re.compile(r'[0-9]+\. [A-Z]')
    # Get number of times it occurs
    number_occurs = restr.findall(text)
    if number_occurs:
        i = 0
        # Loop through in case there is more than one
        for _ in range(0, len(number_occurs)):
            reinfo = restr.search(text[i:])
            # Add a space when this occurs
            text = text[0:i] + text[i:i+reinfo.end()-3] + ' ' + \
                text[i+reinfo.end()-3:]
            i = i+reinfo.end()
    return text

def cleanup_latin_names(text):
    '''
    Sometimes "C. pylorium" becomes a new sentence. Removes all "C." that is found
    Find number occurances this occurs
    '''
    restr = re.compile(r' [A-Z]\. [a-z]')
    # Get number of times it occurs
    number_occurs = restr.findall(text)
    if number_occurs:
        # Loop through in case there is more than one
        for _ in range(0, len(number_occurs)):
            reinfo = restr.search(text)
            # Add a space when this occurs
            text = text[0:reinfo.start()+1] + text[reinfo.end()-2:]
    # Can also sometimes be C.pylorium
    restr = re.compile(r' [A-Z]\.[a-z]')
    # Get number of times it occurs
    number_occurs = restr.findall(text)
    if number_occurs:
        # Loop through in case there is more than one
        for _ in range(0, len(number_occurs)):
            reinfo = restr.search(text)
            # Remove C.
            text = text[0:reinfo.start()+1] + text[reinfo.end()-1:]
    # Can also sometimes be a. pylorium (note a. Pylorium and aa. Phylorium will not be detected)
    restr = re.compile(r' [a-z]\. [a-z]')
    # Get number of times it occurs
    number_occurs = restr.findall(text)
    if number_occurs:
        #    print('fo')
        # Loop through in case there is more than one
        for _ in range(0, len(number_occurs)):
            reinfo = restr.search(text)
            # Add a space when this occurs
            text = text[0:reinfo.end()-3] + text[reinfo.end()-2:]
    return text

def cleanup_sentence_with_missing_spaces(text):
    '''
    Some occurances of word.Word get misinterpreted by treetagger.
    add a space where there is word.Word and add a space
    '''
    # Find number occurances this occurs
    restr = re.compile(r'\W[a-z]+\.[A-Z]')
    # Get number of times it occurs
    number_occurs = restr.findall(text)
    if number_occurs:
        i = 0
        # Loop through in case there is more than one
        for _ in range(0, len(number_occurs)):
            reinfo = restr.search(text[i:])
            # Add a space when this occurs
            text = text[0:i] + text[i:i+reinfo.end()-1] + ' ' + \
                text[i+reinfo.end()-1:]
            i = i+reinfo.end()
    return text

def cleanup_remove_abrevs(text):
    '''
    Revmoves any occurance of ABC-23SDKL abbreviations.
    Any abbreviation including a lowercase is still kept

    Hyphens are still kept in the funciton, despite in the "pipeline"
    they are replaced by spaces before (just in case)
    '''
    # Find number occurances this occurs.
    # Has to be at least two occurances of A- AB A1 to be removed, PIX,
    restr = re.compile(r'[^A-Za-z0-9_\-][A-Z0-9][A-Z0-9\-]+[a-z]*')
    # Get number of times it occurs
    number_occurs = restr.findall(text)
    if number_occurs:
        # Loop through in case there is more than one
        for _ in range(0, len(number_occurs)):
            reinfo = restr.search(text)
            # remove whenever it occurs.
            # leave the second \W (modirfied to include hyphen). (e.g. if " NJNJA.", it returns '.')
            text = text[0:reinfo.start()+1] + text[reinfo.end():]
    #    print(text)
    # This string takes care of things like MyPy
    restr = re.compile(r'[\W][A-Z0-9]*[a-z]+[A-Z0-9\-]+[a-zA-Z0-9\-]*')
    # Get number of times it occurs
    number_occurs = restr.findall(text)
    if number_occurs:
        # Loop through in case there is more than one
        for _ in range(0, len(number_occurs)):
            reinfo = restr.search(text)
            # remove whenever it occurs.
            # leave the second \W (modirfied to include hyphen). (e.g. if " NJNJA.", it returns '.')
            text = text[0:reinfo.start()+1] + text[reinfo.end():]
    #    print(text)
    # This string removes any remaining numbers
    restr = re.compile('[0-9]+')
    # Get number of times it occurs
    number_occurs = restr.findall(text)
    if number_occurs:
        # Loop through in case there is more than one
        for _ in range(0, len(number_occurs)):
            reinfo = restr.search(text)
            text = text[0:reinfo.start()] + text[reinfo.end():]
    #    print(text)
    return text

def cleanup_remove_genes(text):
    '''
    Revmoves genes that contain at least 5 AG with optional hyphen in between
    '''
    # Find number occurances this occurs.
    # Has to be at least two occurances of A- AB A1 to be removed, PIX,
    restr = re.compile('[AGCT][-]?[AGCT][-]?[AGCT][-]?[AGCT][-]?[AGCT-]+')
    # Get number of times it occurs
    number_occurs = restr.findall(text)
    if number_occurs:
        # Loop through in case there is more than one
        for _ in range(0, len(number_occurs)):
            reinfo = restr.search(text)
            # remove whenever it occurs.
            # leave the second \W (modirfied to include hyphen). (e.g. if " NJNJA.", it returns '.')
            text = text[0:reinfo.start()] + text[reinfo.end():]
    return text

def cleanup_remove_decimal_numbers(text):
    '''
    Revmoves numbers which are seperated by a period (otherwise NN.NN becomes ".)
    '''
    # Find number occurances this occurs.
    # Has to be at least two occurances of A- AB A1 to be removed, PIX,
    restr = re.compile(r'[0-9]+\.[0-9]*')
    # Get number of times it occurs
    number_occurs = restr.findall(text)
    if number_occurs:
        # Loop through in case there is more than one
        for _ in range(0, len(number_occurs)):
            reinfo = restr.search(text)
            # remove whenever it occurs.
            # leave the second \W (modirfied to include hyphen). (e.g. if " NJNJA.", it returns '.')
            text = text[0:reinfo.start()] + text[reinfo.end():]
    return text

def cleanup_replace_hyphens(text):
    '''
    All hyphens get replaced with a blankspace. This means all hyphenated words become two.
    Any abbreviations with hyphens will be treated as two abbreviations
    '''
    # replace all hyphens
    text = text.replace('-', ' ')
    return text

def cleanup_sentence_ends_with_etc(text):
    '''
    Correct occuranges when there is a sentence that ends with "etc."
    and the period marks both the etc and the end of the sentence
    '''
    # Find number occurances this occurs
    restr = re.compile(r' etc\. [A-Z]')
    # Get number of times it occurs
    number_occurs = restr.findall(text)
    if number_occurs:
        # Loop through in case there is more than one
        for _ in range(0, len(number_occurs)):
            reinfo = restr.search(text)
            # delete the ' etc'
            text = text[0:reinfo.start()] + text[reinfo.start()+4:]
    return text

def cleanup_text_ends_with_letters(text):
    '''
    sometimes final punctuation is missing which excludes either final
    sentance or (in short abstract) entire text. Also fixes any occuranges where
    it might be ending in: "words " and adds a period to this as well.
    But in a case where it ends with "words. " , nothing will be added.
    '''
    # Find number occurances this occurs
    restr = re.compile(r'\w[\w ]*$')
    if restr.search(text):
        text = text + '.'
    return text

def cleanup_one_letter_words(text):
    '''
    Correct occrances of single letters appearing (that are not I, a or A)
    '''
    # Find number occurances this occurs
    restr = re.compile(
        r'\W[bcdefghijklmnopqrstuvwxyzBCDEFGHJKLMNOPQRSTUVWXYZ]\W')
    # Get number of times it occurs
    number_occurs = restr.findall(text)
    if number_occurs:
        # Loop through in case there is more than one
        for _ in range(0, len(number_occurs)):
            reinfo = restr.search(text)
            # remove whenever it occurs. leave the second \W. (e.g. if " A.", it returns '.')
            text = text[0:reinfo.start()+1] + text[reinfo.end()-1:]
    return text

def cleanup_add_space_after_period(text):
    '''
    Add extra space after every periods for safety
    '''
    # Find number occurances this occurs
    restr = re.compile(r'\.')
    # Get number of times it occurs
    number_occurs = restr.findall(text)
    if number_occurs:
        i = 0
        # Loop through in case there is more than one
        for _ in range(0, len(number_occurs)):
            reinfo = restr.search(text[i:])
            # Add a space when this occurs
            text = text[0:i] + text[i:i+reinfo.start()+1] + ' ' + \
                text[i+reinfo.end():]
            i = i+reinfo.end()
    return text

def cleanup_remove_extra_white_spaces(text):
    '''
    Now extra white spaces may exist. Remove these
    '''
    # Find number occurances this occurs
    restr = re.compile(' [ ]+')
    # Get number of times it occurs
    number_occurs = restr.findall(text)
    if number_occurs:
        # Loop through in case there is more than one
        for _ in range(0, len(number_occurs)):
            reinfo = restr.search(text)
            # remove whenever it occurs. leave the second \W. (e.g. if " A.", it returns '.')
            text = text[0:reinfo.start()+1] + text[reinfo.end():]
    return text

def cleanup_remove_one_word_sentences(text):
    '''
    Identifies sentences with one words in them
    '''
    zval = 0
    while zval == 0:
        restr = re.compile(r'\. ?[A-Za-z]+ ?\.')
        reinfo = restr.search(text)
        if not reinfo:
            zval = 1
        else:
            # remove whenever it occurs. leave the second \W. (e.g. if " A.", it returns '.')
            text = text[0:reinfo.start()+1] + text[reinfo.end():]
    return text

def cleanup_copyright_sentences(text):
    '''
    Remove copyright related sentences
    '''
    restr = re.compile('Hum Brain Mapp.*$')
    reinfo = restr.search(text)
    if reinfo:
        text = text[0:reinfo.start()]
    restr = re.compile('Copyright.*$')
    reinfo = restr.search(text)
    if reinfo:
        text = text[0:reinfo.start()]
    restr = re.compile(
        '[0-9]{4}The Association for the Study of Animal Behaviour.*$')
    reinfo = restr.search(text)
    if reinfo:
        text = text[0:reinfo.start()]
    restr = re.compile(r'VIDEO ABSTRACT\.$')
    reinfo = restr.search(text)
    if reinfo:
        text = text[0:reinfo.start()]
    restr = re.compile(r'\(PsycINFO Database Record\.$')
    reinfo = restr.search(text)
    if reinfo:
        text = text[0:reinfo.start()]
    restr = re.compile(r'\(Funded by.*$')
    reinfo = restr.search(text)
    if reinfo:
        text = text[0:reinfo.start()]
    restr = re.compile(
        r'This article is protected by copyright\. All rights reserved\.$')
    reinfo = restr.search(text)
    if reinfo:
        text = text[0:reinfo.start()]
    return text

def identify_bad_abstracts(text):
    '''
    Conditions for excluding abstract
    if abstract contains the phase "ABSTRACT TRUNCATED"
    '''
    restr = re.compile('ABSTRACT TRUNCATED')
    restr2 = re.compile('No abstract')
    keep = 1
    if restr.search(text):
        keep = 0
    if restr2.search(text):
        keep = 0
    return keep

def cleanup_multi_white_spaces(text):
    '''
    Remove multiple white spaces
    e.g science       and engineering --> science and engineering
    '''
    # regex for repeated whitespace
    restr = re.compile(r"\s+")
    text = restr.sub(' ', text)
    return text

def cleanup_split_nsf_verbage(text):
    '''
    Remove NSF's standard verbage about it's statutory mission
    '''
    # split text on matched verbage and keep first portion
    text = text.split(
        '''This award reflects NSF's statutory mission''', 1)[0]
    return text

def cleanup_remove_html_tags(text):
    '''
    Remove html tags
    e.g science </br> and engineering --> science and engineering
    '''
    restr = re.compile(r'<[^>]+>;')
    text = restr.sub(' ', text)
    return text
