import codecs, sys, re, gzip  
from indicnlp import loader
from indicnlp.script import indic_scripts as isc
from indicnlp.transliterate.unicode_transliterate import UnicodeIndicTransliterator as uit

import numpy as np
import itertools as it


def ned(srcw,tgtw,slang,tlang,w_del=1.0,w_ins=1.0,w_sub=1.0):
    score_mat=np.zeros((len(srcw)+1,len(tgtw)+1))

    score_mat[:,0]=np.array([si*w_del for si in xrange(score_mat.shape[0])])
    score_mat[0,:]=np.array([ti*w_ins for ti in xrange(score_mat.shape[1])])

    for si,sc in enumerate(srcw,1): 
        for ti,tc in enumerate(tgtw,1): 
            so=isc.get_offset(sc,slang)
            to=isc.get_offset(tc,tlang)
            if isc.in_coordinated_range_offset(so) and isc.in_coordinated_range_offset(to) and so==to: 
                score_mat[si,ti]=score_mat[si-1,ti-1]
            elif not (isc.in_coordinated_range_offset(so) or isc.in_coordinated_range_offset(to)) and sc==tc: 
                score_mat[si,ti]=score_mat[si-1,ti-1]
            else: 
                score_mat[si,ti]= min(
                    score_mat[si-1,ti-1]+w_sub,
                    score_mat[si,ti-1]+w_ins,
                    score_mat[si-1,ti]+w_del,
                )
    return (score_mat[-1,-1],float(len(srcw)),float(len(tgtw)))

def lcsr_indic(srcw,tgtw,slang,tlang):
    score_mat=np.zeros((len(srcw)+1,len(tgtw)+1))

    for si,sc in enumerate(srcw,1): 
        for ti,tc in enumerate(tgtw,1): 
            so=isc.get_offset(sc,slang)
            to=isc.get_offset(tc,tlang)

            if isc.in_coordinated_range_offset(so) and isc.in_coordinated_range_offset(to) and so==to: 
                score_mat[si,ti]=score_mat[si-1,ti-1]+1.0
            elif not (isc.in_coordinated_range_offset(so) or isc.in_coordinated_range_offset(to)) and sc==tc: 
                score_mat[si,ti]=score_mat[si-1,ti-1]+1.0
            else: 
                score_mat[si,ti]= max(
                    score_mat[si,ti-1],
                    score_mat[si-1,ti])

    return (score_mat[-1,-1]/float(max(len(srcw),len(tgtw))),float(len(srcw)),float(len(tgtw)))

def lcsr_any(srcw,tgtw,slang,tlang):
    score_mat=np.zeros((len(srcw)+1,len(tgtw)+1))

    for si,sc in enumerate(srcw,1): 
        for ti,tc in enumerate(tgtw,1): 

            if sc==tc: 
                score_mat[si,ti]=score_mat[si-1,ti-1]+1.0
            else: 
                score_mat[si,ti]= max(
                    score_mat[si,ti-1],
                    score_mat[si-1,ti])

    return (score_mat[-1,-1]/float(max(len(srcw),len(tgtw))),float(len(srcw)),float(len(tgtw)))

def lcsr(srcw,tgtw,slang,tlang):

    if slang==tlang or not isc.is_supported_language(slang) or not isc.is_supported_language(tlang):
        return lcsr_any(srcw,tgtw,slang,tlang)
    else:  
        return lcsr_indic(srcw,tgtw,slang,tlang)

def iterate_parallel_corpus(src_fname,tgt_fname):
    with codecs.open(src_fname,'r','utf-8') as src_file,\
         codecs.open(tgt_fname,'r','utf-8') as tgt_file:

        for sline, tline in it.izip(iter(src_file),iter(tgt_file)):           
            sline=re.sub(ur"\s\s+" , u" ", sline.strip()).replace(u" ",u"^")
            tline=re.sub(ur"\s\s+" , u" ", tline.strip()).replace(u" ",u"^")

            yield (sline,tline)

def linguistic_similarity(src_fname,tgt_fname,out_fname,src_lang,tgt_lang,sim_measure='lcsr'):

    sim_measure_func=None

    if sim_measure=='lcsr': 
        sim_measure_func=lcsr 
    elif sim_measure=='ned': 
        sim_measure_func=ned 
    else: 
        raise Exception("")
  
    total=0.0
    n=0.0
    with codecs.open(out_fname,'w','utf-8') as out_file: 
        for sline, tline in iterate_parallel_corpus(src_fname,tgt_fname):           
            score,sl,tl=sim_measure_func(sline,tline,src_lang,tgt_lang)
            total+=score
            n+=1.0

            out_file.write(u'{}|{}|{}\n'.format(score,sl,tl))

        print total/n

if __name__=='__main__': 

    loader.load()

    commands={
            'linguistic_similarity':linguistic_similarity,
            }

    commands[sys.argv[1]](*sys.argv[2:])