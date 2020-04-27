# cython: profile=False
import cravat
import pickle
import time
import os
import json
from cravat.util import most_severe_so
from cravat.constants import gene_level_so_exclude
import importlib

# bases
ADENINENUM = 0
THYMINENUM = 1
GUANINENUM = 2
CYTOSINENUM = 3
ADENINECHAR = 'A'
THYMINECHAR = 'T'
GUANINECHAR = 'G'
CYTOSINECHAR = 'C'
NBASECHAR = 'N'

def base_to_basenum (c):
    if c == ADENINECHAR:
        return ADENINENUM
    if c == THYMINECHAR:
        return THYMINENUM
    if c == GUANINECHAR:
        return GUANINENUM
    if c == CYTOSINECHAR:
        return CYTOSINENUM

MAPPING_UNIPROT_I = 0
MAPPING_ACHANGE_I = 1
MAPPING_SO_I = 2
MAPPING_TR_I = 3
MAPPING_CCHANGE_I = 4
MAPPING_AALEN_I = 5
MAPPING_GENENAME_I = 6
MAPPING_CODING_I = 7
MAPPING_CSN_I = 8

def _compare_mapping (m1, m2):
    m1csn = m1[MAPPING_CSN_I]
    m2csn = m2[MAPPING_CSN_I]
    m1uniprot = m1[MAPPING_UNIPROT_I]
    m2uniprot = m2[MAPPING_UNIPROT_I]
    m1so = m1[MAPPING_SO_I]
    m2so = m2[MAPPING_SO_I]
    m1aalen = m1[MAPPING_AALEN_I]
    m2aalen = m2[MAPPING_AALEN_I]
    better_csn = m1csn > m2csn
    same_csn = m1csn == m2csn
    acceptable_uniprot = m1uniprot is not None or m2uniprot is None
    higher_so = m1so > m2so
    same_so = m1so == m2so
    longer_aa = m1aalen > m2aalen
    same_aalen = m1aalen == m2aalen
    #self_is_better = (better_csn) or ((same_csn) and (higher_so or (same_so and longer_aa)))
    self_is_better = higher_so or (same_so and longer_aa)
    if self_is_better:
        return -1
    else:
        return 1

# strands
PLUSSTRAND = 1
MINUSSTRAND = -1
rev_bases = {'A':'T', 'T':'A', 'G':'C', 'C':'G', '-':'-','N':'N'}
# frag kind
FRAG_FLAG_2K =          0b00000010
FRAG_FLAG_UTR =         0b00000100
FRAG_FLAG_CDS =         0b00001000
FRAG_FLAG_INTRON =      0b00010000
FRAG_UP2K = FRAG_FLAG_2K | 0b0
FRAG_DN2K = FRAG_FLAG_2K | 0b1
FRAG_UTR5 = FRAG_FLAG_UTR | 0b0
FRAG_UTR3 = FRAG_FLAG_UTR | 0b1
FRAG_CDS =   FRAG_FLAG_CDS | 0b0
FRAG_NCRNA = FRAG_FLAG_CDS | 0b1
FRAG_UTR5INTRON =  FRAG_FLAG_INTRON | FRAG_UTR5
FRAG_UTR3INTRON =  FRAG_FLAG_INTRON | FRAG_UTR3
FRAG_CDSINTRON =   FRAG_FLAG_INTRON | FRAG_CDS
FRAG_NCRNAINTRON = FRAG_FLAG_INTRON | FRAG_NCRNA
# variant kind
SNV = 21
INS = 22
DEL = 23
COM = 24
# sequence ontology
SO_NSO = 30
SO_2KD = 31
SO_2KU = 32
SO_UT3 = 33
SO_UT5 = 34
SO_INT = 35
SO_UNK = 36
SO_SYN = 37
SO_MIS = 38
SO_CSS = 39
SO_IND = 40
SO_INI = 41
SO_STL = 42
SO_SPL = 43
SO_STG = 44
SO_FSD = 45
SO_FSI = 46
# csn: coding, splice, noncoding (legacy from old hg38)
CODING = 53
SPLICE = 52
NONCODING = 51
NOCSN = 50
sonum_to_so = {
    SO_2KD: '2KD',
    SO_2KU: '2KU',
    SO_UT3: 'UT3',
    SO_UT5: 'UT5',
    SO_INT: 'INT',
    SO_UNK: 'UNK',
    SO_SYN: 'SYN',
    SO_MIS: 'MIS',
    SO_CSS: 'CSS',
    SO_IND: 'IND',
    SO_INI: 'INI',
    SO_STL: 'STL',
    SO_SPL: 'SPL',
    SO_STG: 'STG',
    SO_FSD: 'FSD',
    SO_FSI: 'FSI',
    SO_NSO: '',
}
# aa
NDA = 60
NOA = 61
UNA = 62
STP = 63
ALA = 64
CYS = 65
ASP = 66
GLU = 67
PHE = 68
GLY = 69
HIS = 70
ILE = 71
LYS = 72
LEU = 73
MET = 74
ASN = 75
PRO = 76
GLN = 77
ARG = 78
SER = 79
THR = 80
VAL = 81
TRP = 82
TYR = 83
aa_to_num = {'A':ALA, 'C': CYS, 'D': ASP, 'E': GLU, 'F': PHE,
    'G': GLY, 'H': HIS, 'I': ILE, 'K': LYS, 'L': LEU,
    'M': MET, 'N': ASN, 'P': PRO, 'Q': GLN, 'R': ARG,
    'S': SER, 'T': THR, 'V': VAL, 'W': TRP, 'Y': TYR, 
    '*': STP, NOA: '_', UNA: '?', NDA: ''}
aanum_to_aa = {
    ALA: 'A', CYS: 'C', ASP: 'D', GLU: 'E', PHE: 'F', 
    GLY: 'G', HIS: 'H', ILE: 'I', LYS: 'K', LEU: 'L',
    MET: 'M', ASN: 'N', PRO: 'P', GLN: 'Q', ARG: 'R',
    SER: 'S', THR: 'T', VAL: 'V', TRP: 'W', TYR: 'Y',
    STP: '*', NOA: '_', UNA: '?', NDA: ''}

def convert_codon_to_codonnum (codon):
    codonnum = 0
    base1 = codon[0]
    base2 = codon[1]
    base3 = codon[2]
    basenum = 0
    if base1 == ADENINECHAR:
        basenum = ADENINENUM
    elif base1 == THYMINECHAR:
        basenum = THYMINENUM
    elif base1 == GUANINECHAR:
        basenum = GUANINENUM
    elif base1 == CYTOSINECHAR:
        basenum = CYTOSINENUM
    codonnum = codonnum | (base_to_basenum(codon[0]) << 4)
    codonnum = codonnum | (base_to_basenum(codon[1]) << 2)
    codonnum = codonnum | base_to_basenum(codon[2])
    return codonnum

codon_to_codonnum = {
    'AAA': convert_codon_to_codonnum('AAA'), 'AAT': convert_codon_to_codonnum('AAT'), 'AAG': convert_codon_to_codonnum('AAG'), 'AAC': convert_codon_to_codonnum('AAC'),
    'ATA': convert_codon_to_codonnum('ATA'), 'ATT': convert_codon_to_codonnum('ATT'), 'ATG': convert_codon_to_codonnum('ATG'), 'ATC': convert_codon_to_codonnum('ATC'),
    'AGA': convert_codon_to_codonnum('AGA'), 'AGT': convert_codon_to_codonnum('AGT'), 'AGG': convert_codon_to_codonnum('AGG'), 'AGC': convert_codon_to_codonnum('AGC'),
    'ACA': convert_codon_to_codonnum('ACA'), 'ACT': convert_codon_to_codonnum('ACT'), 'ACG': convert_codon_to_codonnum('ACG'), 'ACC': convert_codon_to_codonnum('ACC'),
    'TAA': convert_codon_to_codonnum('TAA'), 'TAT': convert_codon_to_codonnum('TAT'), 'TAG': convert_codon_to_codonnum('TAG'), 'TAC': convert_codon_to_codonnum('TAC'),
    'TTA': convert_codon_to_codonnum('TTA'), 'TTT': convert_codon_to_codonnum('TTT'), 'TTG': convert_codon_to_codonnum('TTG'), 'TTC': convert_codon_to_codonnum('TTC'),
    'TGA': convert_codon_to_codonnum('TGA'), 'TGT': convert_codon_to_codonnum('TGT'), 'TGG': convert_codon_to_codonnum('TGG'), 'TGC': convert_codon_to_codonnum('TGC'),
    'TCA': convert_codon_to_codonnum('TCA'), 'TCT': convert_codon_to_codonnum('TCT'), 'TCG': convert_codon_to_codonnum('TCG'), 'TCC': convert_codon_to_codonnum('TCC'),
    'GAA': convert_codon_to_codonnum('GAA'), 'GAT': convert_codon_to_codonnum('GAT'), 'GAG': convert_codon_to_codonnum('GAG'), 'GAC': convert_codon_to_codonnum('GAC'),
    'GTA': convert_codon_to_codonnum('GTA'), 'GTT': convert_codon_to_codonnum('GTT'), 'GTG': convert_codon_to_codonnum('GTG'), 'GTC': convert_codon_to_codonnum('GTC'),
    'GGA': convert_codon_to_codonnum('GGA'), 'GGT': convert_codon_to_codonnum('GGT'), 'GGG': convert_codon_to_codonnum('GGG'), 'GGC': convert_codon_to_codonnum('GGC'),
    'GCA': convert_codon_to_codonnum('GCA'), 'GCT': convert_codon_to_codonnum('GCT'), 'GCG': convert_codon_to_codonnum('GCG'), 'GCC': convert_codon_to_codonnum('GCC'),
    'CAA': convert_codon_to_codonnum('CAA'), 'CAT': convert_codon_to_codonnum('CAT'), 'CAG': convert_codon_to_codonnum('CAG'), 'CAC': convert_codon_to_codonnum('CAC'),
    'CTA': convert_codon_to_codonnum('CTA'), 'CTT': convert_codon_to_codonnum('CTT'), 'CTG': convert_codon_to_codonnum('CTG'), 'CTC': convert_codon_to_codonnum('CTC'),
    'CGA': convert_codon_to_codonnum('CGA'), 'CGT': convert_codon_to_codonnum('CGT'), 'CGG': convert_codon_to_codonnum('CGG'), 'CGC': convert_codon_to_codonnum('CGC'),
    'CCA': convert_codon_to_codonnum('CCA'), 'CCT': convert_codon_to_codonnum('CCT'), 'CCG': convert_codon_to_codonnum('CCG'), 'CCC': convert_codon_to_codonnum('CCC'),
}
codonnum_to_codon = {
    convert_codon_to_codonnum('AAA'): 'AAA', convert_codon_to_codonnum('AAT'): 'AAT', convert_codon_to_codonnum('AAG'): 'AAG', convert_codon_to_codonnum('AAC'): 'AAC',
    convert_codon_to_codonnum('ATA'): 'ATA', convert_codon_to_codonnum('ATT'): 'ATT', convert_codon_to_codonnum('ATG'): 'ATG', convert_codon_to_codonnum('ATC'): 'ATC',
    convert_codon_to_codonnum('AGA'): 'AGA', convert_codon_to_codonnum('AGT'): 'AGT', convert_codon_to_codonnum('AGG'): 'AGG', convert_codon_to_codonnum('AGC'): 'AGC',
    convert_codon_to_codonnum('ACA'): 'ACA', convert_codon_to_codonnum('ACT'): 'ACT', convert_codon_to_codonnum('ACG'): 'ACG', convert_codon_to_codonnum('ACC'): 'ACC',
    convert_codon_to_codonnum('TAA'): 'TAA', convert_codon_to_codonnum('TAT'): 'TAT', convert_codon_to_codonnum('TAG'): 'TAG', convert_codon_to_codonnum('TAC'): 'TAC',
    convert_codon_to_codonnum('TTA'): 'TTA', convert_codon_to_codonnum('TTT'): 'TTT', convert_codon_to_codonnum('TTG'): 'TTG', convert_codon_to_codonnum('TTC'): 'TTC',
    convert_codon_to_codonnum('TGA'): 'TGA', convert_codon_to_codonnum('TGT'): 'TGT', convert_codon_to_codonnum('TGG'): 'TGG', convert_codon_to_codonnum('TGC'): 'TGC',
    convert_codon_to_codonnum('TCA'): 'TCA', convert_codon_to_codonnum('TCT'): 'TCT', convert_codon_to_codonnum('TCG'): 'TCG', convert_codon_to_codonnum('TCC'): 'TCC',
    convert_codon_to_codonnum('GAA'): 'GAA', convert_codon_to_codonnum('GAT'): 'GAT', convert_codon_to_codonnum('GAG'): 'GAG', convert_codon_to_codonnum('GAC'): 'GAC',
    convert_codon_to_codonnum('GTA'): 'GTA', convert_codon_to_codonnum('GTT'): 'GTT', convert_codon_to_codonnum('GTG'): 'GTG', convert_codon_to_codonnum('GTC'): 'GTC',
    convert_codon_to_codonnum('GGA'): 'GGA', convert_codon_to_codonnum('GGT'): 'GGT', convert_codon_to_codonnum('GGG'): 'GGG', convert_codon_to_codonnum('GGC'): 'GGC',
    convert_codon_to_codonnum('GCA'): 'GCA', convert_codon_to_codonnum('GCT'): 'GCT', convert_codon_to_codonnum('GCG'): 'GCG', convert_codon_to_codonnum('GCC'): 'GCC',
    convert_codon_to_codonnum('CAA'): 'CAA', convert_codon_to_codonnum('CAT'): 'CAT', convert_codon_to_codonnum('CAG'): 'CAG', convert_codon_to_codonnum('CAC'): 'CAC',
    convert_codon_to_codonnum('CTA'): 'CTA', convert_codon_to_codonnum('CTT'): 'CTT', convert_codon_to_codonnum('CTG'): 'CTG', convert_codon_to_codonnum('CTC'): 'CTC',
    convert_codon_to_codonnum('CGA'): 'CGA', convert_codon_to_codonnum('CGT'): 'CGT', convert_codon_to_codonnum('CGG'): 'CGG', convert_codon_to_codonnum('CGC'): 'CGC',
    convert_codon_to_codonnum('CCA'): 'CCA', convert_codon_to_codonnum('CCT'): 'CCT', convert_codon_to_codonnum('CCG'): 'CCG', convert_codon_to_codonnum('CCC'): 'CCC',
}
codonnum_to_aanum = {
    convert_codon_to_codonnum('ATG'):aa_to_num['M'], convert_codon_to_codonnum('GCT'):aa_to_num['A'], convert_codon_to_codonnum('GCC'):aa_to_num['A'], 
    convert_codon_to_codonnum('GCA'):aa_to_num['A'], convert_codon_to_codonnum('GCG'):aa_to_num['A'], convert_codon_to_codonnum('TGT'):aa_to_num['C'], 
    convert_codon_to_codonnum('TGC'):aa_to_num['C'], convert_codon_to_codonnum('GAT'):aa_to_num['D'], convert_codon_to_codonnum('GAC'):aa_to_num['D'], 
    convert_codon_to_codonnum('GAA'):aa_to_num['E'], convert_codon_to_codonnum('GAG'):aa_to_num['E'], convert_codon_to_codonnum('TTT'):aa_to_num['F'], 
    convert_codon_to_codonnum('TTC'):aa_to_num['F'], convert_codon_to_codonnum('GGT'):aa_to_num['G'], convert_codon_to_codonnum('GGC'):aa_to_num['G'], 
    convert_codon_to_codonnum('GGA'):aa_to_num['G'], convert_codon_to_codonnum('GGG'):aa_to_num['G'], convert_codon_to_codonnum('CAT'):aa_to_num['H'], 
    convert_codon_to_codonnum('CAC'):aa_to_num['H'], convert_codon_to_codonnum('ATT'):aa_to_num['I'], convert_codon_to_codonnum('ATC'):aa_to_num['I'], 
    convert_codon_to_codonnum('ATA'):aa_to_num['I'], convert_codon_to_codonnum('AAA'):aa_to_num['K'], convert_codon_to_codonnum('AAG'):aa_to_num['K'], 
    convert_codon_to_codonnum('TTA'):aa_to_num['L'], convert_codon_to_codonnum('TTG'):aa_to_num['L'], convert_codon_to_codonnum('CTT'):aa_to_num['L'], 
    convert_codon_to_codonnum('CTC'):aa_to_num['L'], convert_codon_to_codonnum('CTA'):aa_to_num['L'], convert_codon_to_codonnum('CTG'):aa_to_num['L'], 
    convert_codon_to_codonnum('AAT'):aa_to_num['N'], convert_codon_to_codonnum('AAC'):aa_to_num['N'], convert_codon_to_codonnum('CCT'):aa_to_num['P'], 
    convert_codon_to_codonnum('CCC'):aa_to_num['P'], convert_codon_to_codonnum('CCA'):aa_to_num['P'], convert_codon_to_codonnum('CCG'):aa_to_num['P'], 
    convert_codon_to_codonnum('CAA'):aa_to_num['Q'], convert_codon_to_codonnum('CAG'):aa_to_num['Q'], convert_codon_to_codonnum('TCT'):aa_to_num['S'], 
    convert_codon_to_codonnum('TCC'):aa_to_num['S'], convert_codon_to_codonnum('TCA'):aa_to_num['S'], convert_codon_to_codonnum('TCG'):aa_to_num['S'], 
    convert_codon_to_codonnum('AGT'):aa_to_num['S'], convert_codon_to_codonnum('AGC'):aa_to_num['S'], convert_codon_to_codonnum('ACT'):aa_to_num['T'], 
    convert_codon_to_codonnum('ACC'):aa_to_num['T'], convert_codon_to_codonnum('ACA'):aa_to_num['T'], convert_codon_to_codonnum('ACG'):aa_to_num['T'], 
    convert_codon_to_codonnum('CGT'):aa_to_num['R'], convert_codon_to_codonnum('CGC'):aa_to_num['R'], convert_codon_to_codonnum('CGA'):aa_to_num['R'], 
    convert_codon_to_codonnum('CGG'):aa_to_num['R'], convert_codon_to_codonnum('AGA'):aa_to_num['R'], convert_codon_to_codonnum('AGG'):aa_to_num['R'], 
    convert_codon_to_codonnum('GTT'):aa_to_num['V'], convert_codon_to_codonnum('GTC'):aa_to_num['V'], convert_codon_to_codonnum('GTA'):aa_to_num['V'], 
    convert_codon_to_codonnum('GTG'):aa_to_num['V'], convert_codon_to_codonnum('TGG'):aa_to_num['W'], convert_codon_to_codonnum('TAT'):aa_to_num['Y'], 
    convert_codon_to_codonnum('TAC'):aa_to_num['Y'], convert_codon_to_codonnum('TGA'):aa_to_num['*'], convert_codon_to_codonnum('TAA'):aa_to_num['*'], 
    convert_codon_to_codonnum('TAG'):aa_to_num['*']}
codonnum_to_aa = {
    convert_codon_to_codonnum('ATG'):'M', convert_codon_to_codonnum('GCT'):'A', convert_codon_to_codonnum('GCC'):'A', 
    convert_codon_to_codonnum('GCA'):'A', convert_codon_to_codonnum('GCG'):'A', convert_codon_to_codonnum('TGT'):'C', 
    convert_codon_to_codonnum('TGC'):'C', convert_codon_to_codonnum('GAT'):'D', convert_codon_to_codonnum('GAC'):'D', 
    convert_codon_to_codonnum('GAA'):'E', convert_codon_to_codonnum('GAG'):'E', convert_codon_to_codonnum('TTT'):'F', 
    convert_codon_to_codonnum('TTC'):'F', convert_codon_to_codonnum('GGT'):'G', convert_codon_to_codonnum('GGC'):'G', 
    convert_codon_to_codonnum('GGA'):'G', convert_codon_to_codonnum('GGG'):'G', convert_codon_to_codonnum('CAT'):'H', 
    convert_codon_to_codonnum('CAC'):'H', convert_codon_to_codonnum('ATT'):'I', convert_codon_to_codonnum('ATC'):'I', 
    convert_codon_to_codonnum('ATA'):'I', convert_codon_to_codonnum('AAA'):'K', convert_codon_to_codonnum('AAG'):'K', 
    convert_codon_to_codonnum('TTA'):'L', convert_codon_to_codonnum('TTG'):'L', convert_codon_to_codonnum('CTT'):'L', 
    convert_codon_to_codonnum('CTC'):'L', convert_codon_to_codonnum('CTA'):'L', convert_codon_to_codonnum('CTG'):'L', 
    convert_codon_to_codonnum('AAT'):'N', convert_codon_to_codonnum('AAC'):'N', convert_codon_to_codonnum('CCT'):'P', 
    convert_codon_to_codonnum('CCC'):'P', convert_codon_to_codonnum('CCA'):'P', convert_codon_to_codonnum('CCG'):'P', 
    convert_codon_to_codonnum('CAA'):'Q', convert_codon_to_codonnum('CAG'):'Q', convert_codon_to_codonnum('TCT'):'S', 
    convert_codon_to_codonnum('TCC'):'S', convert_codon_to_codonnum('TCA'):'S', convert_codon_to_codonnum('TCG'):'S', 
    convert_codon_to_codonnum('AGT'):'S', convert_codon_to_codonnum('AGC'):'S', convert_codon_to_codonnum('ACT'):'T', 
    convert_codon_to_codonnum('ACC'):'T', convert_codon_to_codonnum('ACA'):'T', convert_codon_to_codonnum('ACG'):'T', 
    convert_codon_to_codonnum('CGT'):'R', convert_codon_to_codonnum('CGC'):'R', convert_codon_to_codonnum('CGA'):'R', 
    convert_codon_to_codonnum('CGG'):'R', convert_codon_to_codonnum('AGA'):'R', convert_codon_to_codonnum('AGG'):'R', 
    convert_codon_to_codonnum('GTT'):'V', convert_codon_to_codonnum('GTC'):'V', convert_codon_to_codonnum('GTA'):'V', 
    convert_codon_to_codonnum('GTG'):'V', convert_codon_to_codonnum('TGG'):'W', convert_codon_to_codonnum('TAT'):'Y', 
    convert_codon_to_codonnum('TAC'):'Y', convert_codon_to_codonnum('TGA'):'*', convert_codon_to_codonnum('TAA'):'*', 
    convert_codon_to_codonnum('TAG'):'*'}
codon_to_aanum = {
    'ATG':MET, 'GCT':ALA, 'GCC':ALA, 
    'GCA':ALA, 'GCG':ALA, 'TGT':CYS, 
    'TGC':CYS, 'GAT':ASP, 'GAC':ASP, 
    'GAA':GLU, 'GAG':GLU, 'TTT':PHE, 
    'TTC':PHE, 'GGT':GLY, 'GGC':GLY, 
    'GGA':GLY, 'GGG':GLY, 'CAT':HIS, 
    'CAC':HIS, 'ATT':ILE, 'ATC':ILE, 
    'ATA':ILE, 'AAA':LYS, 'AAG':LYS, 
    'TTA':LEU, 'TTG':LEU, 'CTT':LEU, 
    'CTC':LEU, 'CTA':LEU, 'CTG':LEU, 
    'AAT':ASN, 'AAC':ASN, 'CCT':PRO, 
    'CCC':PRO, 'CCA':PRO, 'CCG':PRO, 
    'CAA':GLN, 'CAG':GLN, 'TCT':SER, 
    'TCC':SER, 'TCA':SER, 'TCG':SER, 
    'AGT':SER, 'AGC':SER, 'ACT':THR, 
    'ACC':THR, 'ACA':THR, 'ACG':THR, 
    'CGT':ARG, 'CGC':ARG, 'CGA':ARG, 
    'CGG':ARG, 'AGA':ARG, 'AGG':ARG, 
    'GTT':VAL, 'GTC':VAL, 'GTA':VAL, 
    'GTG':VAL, 'TGG':TRP, 'TAT':TYR, 
    'TAC':TYR, 'TGA':STP, 'TAA':STP, 
    'TAG':STP}

codon_to_aa = {
    'ATG':'M', 'GCT':'A', 'GCC':'A', 
    'GCA':'A', 'GCG':'A', 'TGT':'C', 
    'TGC':'C', 'GAT':'D', 'GAC':'D', 
    'GAA':'E', 'GAG':'E', 'TTT':'F', 
    'TTC':'F', 'GGT':'G', 'GGC':'G', 
    'GGA':'G', 'GGG':'G', 'CAT':'H', 
    'CAC':'H', 'ATT':'I', 'ATC':'I', 
    'ATA':'I', 'AAA':'K', 'AAG':'K', 
    'TTA':'L', 'TTG':'L', 'CTT':'L', 
    'CTC':'L', 'CTA':'L', 'CTG':'L', 
    'AAT':'N', 'AAC':'N', 'CCT':'P', 
    'CCC':'P', 'CCA':'P', 'CCG':'P', 
    'CAA':'Q', 'CAG':'Q', 'TCT':'S', 
    'TCC':'S', 'TCA':'S', 'TCG':'S', 
    'AGT':'S', 'AGC':'S', 'ACT':'T', 
    'ACC':'T', 'ACA':'T', 'ACG':'T', 
    'CGT':'R', 'CGC':'R', 'CGA':'R', 
    'CGG':'R', 'AGA':'R', 'AGG':'R', 
    'GTT':'V', 'GTC':'V', 'GTA':'V', 
    'GTG':'V', 'TGG':'W', 'TAT':'Y', 
    'TAC':'Y', 'TGA':'*', 'TAA':'*', 
    'TAG':'*'}


def _get_base_str (tr_base, lenbase):
    tr_base_str = ''
    for i in range(lenbase):
        tr_base_str += chr(tr_base[i])
    return tr_base_str

class Mapper (cravat.BaseMapper):

    def setup (self):
        self.module_dir = os.path.dirname(__file__)
        data_dir = os.path.join(self.module_dir, 'data')
        db_path = os.path.join(data_dir, 'gene_24_10000_old.sqlite')
        self.db = self._get_db(db_path)
        self.c = self.db.cursor()
        self.c2 = self.db.cursor()
        self.c.execute('pragma synchronous=0;')
        q = 'select v from info where k="binsize"'
        self.c.execute(q)
        self.binsize = int(self.c.fetchone()[0])
        q = 'select v from info where k="gencode_ver"'
        self.c.execute(q)
        self.ver = self.c.fetchone()[0]
        mrnas_path = os.path.join(data_dir, 'mrnas_24_old.pickle')
        f = open(mrnas_path, 'rb')
        self.mrnas = pickle.load(f)
        f.close()
        self.logger.info(f'mapper database: {db_path}')
        self._make_tr_info()
        #self.wgs = cravat.get_wgs_reader('hg38') # TODO: revive in the 2nd phase of this mapper.

    def end (self):
        self.c.execute('pragma synchronous=2;')
        self.c.close()
        self.c2.close()
        self.db.close()
        
    def _make_tr_info (self):
        t = time.time()
        q = f'select t.tid, t.name, t.strand, t.refseq, t.uniprot, t.alen, g.desc from transcript as t, genenames as g where t.genename=g.genename'
        self.c.execute(q)
        self.tr_info = {}
        for r in self.c.fetchall():
            (tid, name, strand, refseq, uniprot, alen, genename) = r
            if refseq is None:
                refseqs = []
            else:
                refseqs = [v for v in refseq.split(',')]
            self.tr_info[tid] = [name, strand, refseqs, uniprot, alen, genename]

    def _get_db (self, db_path):
        try:
            import sqlite3
            diskdb = sqlite3.connect(db_path)
            db = sqlite3.connect(':memory:')
            diskdb.backup(db)
        except:
            try:
                import apsw
                diskdb = apsw.Connection(db_path)
                db = apsw.Connection(':memory:')
                db.backup('main', diskdb, 'main').step()
            except:
                try:
                    from supersqlite import sqlite3
                    diskdb = sqlite3.connect(db_path)
                    db = sqlite3.connect(':memory:')
                    diskdb.backup(db)
                except:
                    db = sqlite3.connect(db_path)
        return db

    def _get_snv_map_data (self, tid, cpos, cstart, tpos, tstart, tr_ref_base, tr_alt_base, strand, kind, apos, gpos, start, end, chrom, fragno, lenref, lenalt, prevcont, nextcont):
        so = SO_NSO
        csn = NOCSN
        if kind == FRAG_CDS:
            tr_ref_base_str = tr_ref_base
            tr_alt_base_str = tr_alt_base
            so, ref_aanum, alt_aanum = self._get_svn_cds_so(tid, cpos, cstart, tpos, tstart, tr_alt_base)
            ref_aas = [aanum_to_aa[ref_aanum]]
            alt_aas = [aanum_to_aa[alt_aanum]]
            achange = f'{"".join(ref_aas)}{apos}{"".join(alt_aas)}'
            cchange = f'{tr_ref_base_str}{cpos}{tr_alt_base_str}'
            coding = 'Y'
            csn = CODING
        elif kind == FRAG_UTR5:
            so = SO_UT5
            achange = None
            cchange = None
            ref_aas = [aanum_to_aa[NDA]]
            alt_aas = [aanum_to_aa[NDA]]
            coding = None
            csn = NONCODING
        elif kind == FRAG_UTR3:
            so = SO_UT3
            achange = None
            cchange = None
            ref_aas = [aanum_to_aa[NDA]]
            alt_aas = [aanum_to_aa[NDA]]
            coding = None
            csn = NONCODING
        elif kind == FRAG_UTR5INTRON or kind == FRAG_UTR3INTRON or kind == FRAG_NCRNAINTRON: # TODO: handle splice later.
            so = SO_INT
            achange = None
            cchange = None
            ref_aas = [aanum_to_aa[NDA]]
            alt_aas = [aanum_to_aa[NDA]]
            coding = None
            csn = NONCODING
        elif kind == FRAG_CDSINTRON:
            cchange = None
            coding = None
            ref_aas = [aanum_to_aa[NOA]]
            alt_aas = [aanum_to_aa[NOA]]
            achange = None
            if gpos == start or gpos == start + 1:
                if (prevcont == 1 and strand == PLUSSTRAND) or (nextcont == 1 and strand == MINUSSTRAND):
                    apos = -1
                    so = SO_INT
                    csn = NONCODING
                else:
                    if strand == PLUSSTRAND:
                        apos, so, csn = self._get_splice_apos_prevfrag(tid, fragno, chrom)
                    else:
                        apos, so, csn = self._get_splice_apos_nextfrag(tid, fragno, chrom)
                    if so == SO_SPL:
                        achange = f'{"".join(ref_aas)}{apos}{"".join(alt_aas)}'
            elif gpos == end or gpos == end - 1:
                if (nextcont == 1 and strand == PLUSSTRAND) or (prevcont == 1 and strand == MINUSSTRAND):
                    apos = -1
                    so = SO_INT
                    csn = NONCODING
                else:
                    if strand == PLUSSTRAND:
                        apos, so, csn = self._get_splice_apos_nextfrag(tid, fragno, chrom)
                    else:
                        apos, so, csn = self._get_splice_apos_prevfrag(tid, fragno, chrom)
                    if so == SO_SPL:
                        achange = f'{"".join(ref_aas)}{apos}{"".join(alt_aas)}'
            else:
                so = SO_INT
                csn = NONCODING
                ref_aas = [aanum_to_aa[NDA]]
                alt_aas = [aanum_to_aa[NDA]]
        elif kind == FRAG_NCRNA:
            so = SO_UNK
            achange = None
            cchange = None
            ref_aas = [aanum_to_aa[NDA]]
            alt_aas = [aanum_to_aa[NDA]]
            coding = None
            csn = NONCODING
        elif kind == FRAG_UP2K:
            so = SO_2KU
            achange = None
            cchange = None
            ref_aas = [aanum_to_aa[NDA]]
            alt_aas = [aanum_to_aa[NDA]]
            coding = None
            csn = NONCODING
        elif kind == FRAG_DN2K:
            so = SO_2KD
            achange = None
            cchange = None
            ref_aas = [aanum_to_aa[NDA]]
            alt_aas = [aanum_to_aa[NDA]]
            coding = None
            csn = NONCODING
        return so, ref_aas, alt_aas, achange, cchange, coding, csn

    def _get_ins_map_data (self, tid, cpos, cstart, tpos, tstart, tr_ref_base, tr_alt_base, strand, kind, apos, gpos, start, end, chrom, fragno, lenref, lenalt, prevcont, nextcont):
        so = SO_NSO
        if kind == FRAG_CDS:
            so, ref_aas, alt_aas = self._get_ins_cds_so(tid, cpos, cstart, tpos, tstart, tr_alt_base, chrom, strand, lenalt)
            tr_ref_base_str = tr_ref_base
            tr_alt_base_str = tr_alt_base
            achange = f'{"".join(ref_aas)}{apos}{"".join(alt_aas)}'
            cchange = f'{tr_ref_base_str}{cpos}{tr_alt_base_str}'
            coding = 'Y'
            csn = CODING
        elif kind == FRAG_UTR5:
            so = SO_UT5
            achange = None
            cchange = None
            ref_aas = [aanum_to_aa[NDA]]
            alt_aas = [aanum_to_aa[NDA]]
            coding = None
            csn = NONCODING
        elif kind == FRAG_UTR3:
            so = SO_UT3
            achange = None
            cchange = None
            ref_aas = [aanum_to_aa[NDA]]
            alt_aas = [aanum_to_aa[NDA]]
            coding = None
            csn = NONCODING
        elif kind == FRAG_UTR5INTRON or kind == FRAG_UTR3INTRON or kind == FRAG_NCRNAINTRON: # TODO: handle splice later.
            so = SO_INT
            achange = None
            cchange = None
            ref_aas = [aanum_to_aa[NDA]]
            alt_aas = [aanum_to_aa[NDA]]
            coding = None
            csn = NONCODING
        elif kind == FRAG_CDSINTRON:
            cchange = None
            coding = None
            ref_aas = [aanum_to_aa[NOA]]
            alt_aas = [aanum_to_aa[NOA]]
            achange = None
            if gpos == start or gpos == start + 1:
                if (prevcont == 1 and strand == PLUSSTRAND) or (nextcont == 1 and strand == MINUSSTRAND):
                    apos = -1
                    so = SO_INT
                    csn = NONCODING
                else:
                    if strand == PLUSSTRAND:
                        apos, so, csn = self._get_splice_apos_prevfrag(tid, fragno, chrom)
                    else:
                        apos, so, csn = self._get_splice_apos_nextfrag(tid, fragno, chrom)
                    if so == SO_SPL:
                        achange = f'{"".join(ref_aas)}{apos}{"".join(alt_aas)}'
            elif gpos == end or gpos == end - 1:
                if (nextcont == 1 and strand == PLUSSTRAND) or (prevcont == 1 and strand == MINUSSTRAND):
                    apos = -1
                    so = SO_INT
                    csn = NONCODING
                else:
                    if strand == PLUSSTRAND:
                        apos, so, csn = self._get_splice_apos_nextfrag(tid, fragno, chrom)
                    else:
                        apos, so, csn = self._get_splice_apos_prevfrag(tid, fragno, chrom)
                    if so == SO_SPL:
                        achange = f'{"".join(ref_aas)}{apos}{"".join(alt_aas)}'
            else:
                so = SO_INT
                csn = NONCODING
                ref_aas = [aanum_to_aa[NDA]]
                alt_aas = [aanum_to_aa[NDA]]
        elif kind == FRAG_NCRNA:
            so = SO_UNK
            achange = None
            cchange = None
            ref_aas = [aanum_to_aa[NDA]]
            alt_aas = [aanum_to_aa[NDA]]
            coding = None
            csn = NONCODING
        elif kind == FRAG_UP2K:
            so = SO_2KU
            achange = None
            cchange = None
            ref_aas = [aanum_to_aa[NDA]]
            alt_aas = [aanum_to_aa[NDA]]
            coding = None
            csn = NONCODING
        elif kind == FRAG_DN2K:
            so = SO_2KD
            achange = None
            cchange = None
            ref_aas = [aanum_to_aa[NDA]]
            alt_aas = [aanum_to_aa[NDA]]
            coding = None
            csn = NONCODING
        return so, ref_aas, alt_aas, achange, cchange, coding, csn

    def _get_del_map_data (self, tid, cpos, cstart, tpos, tstart, tr_ref_base, tr_alt_base, strand, kind, apos, gpos, start, end, chrom, gposendbin, gposend, fragno, lenref, lenalt, prevcont, nextcont):
        so = SO_NSO
        startplus = start + 1
        endminus = end - 1
        q = f'select kind from transcript_frags_{chrom} where tid={tid} and binno={gposendbin} and start<={gposend} and end>={gposend}'
        self.c2.execute(q)
        gposend_kind = self.c2.fetchone()
        if gposend_kind is not None:
            gposend_kind = gposend_kind[0]
        if kind != gposend_kind:
            so = SO_UNK
            coding = None
            achange = None
            cchange = None
            csn = NONCODING
            ref_aas = [aanum_to_aa[NDA]]
            alt_aas = [aanum_to_aa[NDA]]
        else:
            if kind == FRAG_CDS:
                ref_aas = [aanum_to_aa[NOA]]
                alt_aas = [aanum_to_aa[NOA]]
                if lenref % 3 == 0:
                    so = SO_IND
                else:
                    so = SO_FSD
                tr_ref_base_str = tr_ref_base
                tr_alt_base_str = tr_alt_base
                achange = f'{"".join(ref_aas)}{apos}{"".join(alt_aas)}'
                cchange = f'{tr_ref_base_str}{cpos}{tr_alt_base_str}'
                coding = 'Y'
                csn = CODING
            elif kind == FRAG_UTR5:
                so = SO_UT5
                achange = None
                cchange = None
                ref_aas = [aanum_to_aa[NDA]]
                alt_aas = [aanum_to_aa[NDA]]
                coding = None
                csn = NONCODING
            elif kind == FRAG_UTR3:
                so = SO_UT3
                achange = None
                cchange = None
                ref_aas = [aanum_to_aa[NDA]]
                alt_aas = [aanum_to_aa[NDA]]
                coding = None
                csn = NONCODING
            elif kind == FRAG_UTR5INTRON or kind == FRAG_UTR3INTRON or kind == FRAG_NCRNAINTRON: # TODO: handle splice later.
                so = SO_INT
                achange = None
                cchange = None
                ref_aas = [aanum_to_aa[NDA]]
                alt_aas = [aanum_to_aa[NDA]]
                coding = None
                csn = NONCODING
            elif kind == FRAG_CDSINTRON:
                cchange = None
                coding = None
                ref_aas = [aanum_to_aa[NOA]]
                alt_aas = [aanum_to_aa[NOA]]
                achange = None
                if gpos == start or gpos == startplus or gposend == start or gposend == startplus:
                    if (prevcont == 1 and strand == PLUSSTRAND) or (nextcont == 1 and strand == MINUSSTRAND):
                        apos = -1
                        so = SO_INT
                        csn = NONCODING
                    else:
                        if strand == PLUSSTRAND:
                            apos, so, csn = self._get_splice_apos_prevfrag(tid, fragno, chrom)
                        else:
                            apos, so, csn = self._get_splice_apos_nextfrag(tid, fragno, chrom)
                        if so == SO_SPL:
                            achange = f'{"".join(ref_aas)}{apos}{"".join(alt_aas)}'
                elif gpos == end or gpos == endminus or gposend == end or gposend == endminus:
                    if (nextcont == 1 and strand == PLUSSTRAND) or (prevcont == 1 and strand == MINUSSTRAND):
                        apos = -1
                        so = SO_INT
                        csn = NONCODING
                    else:
                        if strand == PLUSSTRAND:
                            apos, so, csn = self._get_splice_apos_nextfrag(tid, fragno, chrom)
                        else:
                            apos, so, csn = self._get_splice_apos_prevfrag(tid, fragno, chrom)
                        if so == SO_SPL:
                            achange = f'{"".join(ref_aas)}{apos}{"".join(alt_aas)}'
                else:
                    so = SO_INT
                    csn = NONCODING
                    ref_aas = [aanum_to_aa[NDA]]
                    alt_aas = [aanum_to_aa[NDA]]
            elif kind == FRAG_NCRNA:
                so = SO_UNK
                achange = None
                cchange = None
                ref_aas = [aanum_to_aa[NDA]]
                alt_aas = [aanum_to_aa[NDA]]
                coding = None
                csn = NONCODING
            elif kind == FRAG_UP2K:
                so = SO_2KU
                achange = None
                cchange = None
                ref_aas = [aanum_to_aa[NDA]]
                alt_aas = [aanum_to_aa[NDA]]
                coding = None
                csn = NONCODING
            elif kind == FRAG_DN2K:
                so = SO_2KD
                achange = None
                cchange = None
                ref_aas = [aanum_to_aa[NDA]]
                alt_aas = [aanum_to_aa[NDA]]
                coding = None
                csn = NONCODING
        return so, ref_aas, alt_aas, achange, cchange, coding, csn

    def _get_com_map_data (self, tid, cpos, cstart, tpos, tstart, tr_ref_base, tr_alt_base, strand, kind, apos, gpos, start, end, chrom, gposendbin, gposend, fragno, lenref, lenalt, prevcont, nextcont):
        so = SO_NSO
        startplus = start + 1
        endminus = end - 1
        if lenref > 1:
            q = f'select kind from transcript_frags_{chrom} where binno={gposendbin} and start<={gposend} and end>={gposend} and tid={tid}'
            self.c2.execute(q)
            gposend_kind = self.c2.fetchone()
            if gposend_kind is not None:
                gposend_kind = gposend_kind[0]
        else:
            gposend_kind = kind
        if kind != gposend_kind:
            so = SO_UNK
            coding = None
            achange = None
            cchange = None
            csn = NONCODING
        else:
            if kind == FRAG_CDS:
                so = SO_CSS
                achange = None
                cchange = None
                ref_aas = [aanum_to_aa[NOA]]
                alt_aas = [aanum_to_aa[NOA]]
                tr_ref_base_str = tr_ref_base
                tr_alt_base_str = tr_alt_base
                achange = f'{"".join(ref_aas)}{apos}{"".join(alt_aas)}'
                cchange = f'{tr_ref_base_str}{cpos}{tr_alt_base_str}'
                coding = 'Y'
                csn = CODING
            elif kind == FRAG_UTR5:
                so = SO_UT5
                achange = None
                cchange = None
                ref_aas = [aanum_to_aa[NDA]]
                alt_aas = [aanum_to_aa[NDA]]
                coding = None
                csn = NONCODING
            elif kind == FRAG_UTR3:
                so = SO_UT3
                achange = None
                cchange = None
                ref_aas = [aanum_to_aa[NDA]]
                alt_aas = [aanum_to_aa[NDA]]
                coding = None
                csn = NONCODING
            elif kind == FRAG_UTR5INTRON or kind == FRAG_UTR3INTRON or kind == FRAG_NCRNAINTRON: # TODO: handle splice later.
                so = SO_INT
                achange = None
                cchange = None
                ref_aas = [aanum_to_aa[NDA]]
                alt_aas = [aanum_to_aa[NDA]]
                coding = None
                csn = NONCODING
            elif kind == FRAG_CDSINTRON:
                cchange = None
                coding = None
                ref_aas = [aanum_to_aa[NOA]]
                alt_aas = [aanum_to_aa[NOA]]
                achange = None
                if gpos == start or gpos == startplus or gposend == start or gposend == startplus:
                    if (prevcont == 1 and strand == PLUSSTRAND) or (nextcont == 1 and strand == MINUSSTRAND):
                        apos = -1
                        so = SO_INT
                        csn = NONCODING
                    else:
                        if strand == PLUSSTRAND:
                            apos, so, csn = self._get_splice_apos_prevfrag(tid, fragno, chrom)
                        else:
                            apos, so, csn = self._get_splice_apos_nextfrag(tid, fragno, chrom)
                        if so == SO_SPL:
                            achange = f'{"".join(ref_aas)}{apos}{"".join(alt_aas)}'
                elif gpos == end or gpos == endminus or gposend == end or gposend == endminus:
                    if (nextcont == 1 and strand == PLUSSTRAND) or (prevcont == 1 and strand == MINUSSTRAND):
                        apos = -1
                        so = SO_INT
                        csn = NONCODING
                    else:
                        if strand == PLUSSTRAND:
                            apos, so, csn = self._get_splice_apos_nextfrag(tid, fragno, chrom)
                        else:
                            apos, so, csn = self._get_splice_apos_prevfrag(tid, fragno, chrom)
                        if so == SO_SPL:
                            achange = f'{"".join(ref_aas)}{apos}{"".join(alt_aas)}'
                else:
                    so = SO_INT
                    csn = NONCODING
                    ref_aas = [aanum_to_aa[NDA]]
                    alt_aas = [aanum_to_aa[NDA]]
            elif kind == FRAG_NCRNA:
                so = SO_UNK
                achange = None
                cchange = None
                ref_aas = [aanum_to_aa[NDA]]
                alt_aas = [aanum_to_aa[NDA]]
                coding = None
                csn = NONCODING
            elif kind == FRAG_UP2K:
                so = SO_2KU
                achange = None
                cchange = None
                ref_aas = [aanum_to_aa[NDA]]
                alt_aas = [aanum_to_aa[NDA]]
                coding = None
                csn = NONCODING
            elif kind == FRAG_DN2K:
                so = SO_2KD
                achange = None
                cchange = None
                ref_aas = [aanum_to_aa[NDA]]
                alt_aas = [aanum_to_aa[NDA]]
                coding = None
                csn = NONCODING
        return so, ref_aas, alt_aas, achange, cchange, coding, csn

    def _get_tr_map_data (self, chrom, gpos):
        gposbin = int(gpos / self.binsize)
        q = f'select * from transcript_frags_{chrom} where binno={gposbin} and start<={gpos} and end>={gpos} order by tid'
        try:
            self.c.execute(q)
            ret = self.c.fetchall()
        except Exception as e:
            if str(e).startswith('no such table'):
                ret = []
            else:
                raise
        return ret

    def map (self, crv_data):
        tpos = -1
        so = SO_NSO
        uid = crv_data['uid']
        chrom = crv_data['chrom']
        gpos = crv_data['pos']
        ref_base_str = crv_data['ref_base']
        alt_base_str = crv_data['alt_base']
        if alt_base_str == '*':
            return None, None
        if ref_base_str is None:
            # TODO: replace below with ref_base_str = self.wgs.get_bases(chrom, gpos) and delete the part with _get_codons in the 2nd phase of this mapper.
            ref_base_str = 'N'
            crv_data['ref_base'] = ref_base_str
        lenref = len(ref_base_str)
        lenalt = len(alt_base_str)
        tr_ref_base_plus = ''
        for i in range(lenref):
            tr_ref_base_plus += ref_base_str[i]
        tr_alt_base_plus = ''
        for i in range(lenalt):
            tr_alt_base_plus += alt_base_str[i]
        tr_ref_base_minus = ''
        for i in range(lenref):
            j = lenref - 1 - i
            tr_ref_base_minus += rev_bases[ref_base_str[j]]
        tr_alt_base_minus = ''
        for i in range(lenalt):
            j = lenalt - 1 - i
            tr_alt_base_minus += rev_bases[alt_base_str[j]]
        tr_ref_base = tr_ref_base_plus
        tr_alt_base = tr_alt_base_plus
        if ref_base_str == '-' and alt_base_str != '-' and lenalt >= 1:
            var_type = INS
        elif alt_base_str == '-' and ref_base_str != '-' and lenref >= 1:
            var_type = DEL
        elif ref_base_str != '-' and alt_base_str != '-' and lenref == 1 and lenalt == 1:
            var_type = SNV
        else:
            var_type = COM
        if var_type == DEL or var_type == COM:
            gposend = gpos + lenref - 1
            gposendbin = int(gposend / self.binsize)
        else:
            gposend = -1
            gposendbin = -1
        rs = self._get_tr_map_data(chrom, gpos)
        all_mappings = {}
        alt_transcripts = {}
        coding = None
        for r in rs:
            [tid, fragno, start, end, kind, exonno, tstart, cstart, binno, prevcont, nextcont] = r
            [tr, strand, refseqs, uniprot, alen, genename] = self.tr_info[tid]
            #strand = int(strand)
            if tr not in alt_transcripts:
                alt_transcripts[tr] = []
            for refseq in refseqs:
                if refseq not in alt_transcripts[tr]:
                    alt_transcripts[tr].append(refseq)
            if strand == PLUSSTRAND:
                tpos = gpos - start + tstart 
                tr_ref_base = tr_ref_base_plus
                tr_alt_base = tr_alt_base_plus
            elif strand == MINUSSTRAND:
                tpos = end - gpos + tstart
                tr_ref_base = tr_ref_base_minus
                tr_alt_base = tr_alt_base_minus
            # cpos, apos
            if kind == FRAG_CDS:
                if strand == PLUSSTRAND:
                    cpos = gpos - start + cstart
                else:
                    cpos = end - gpos + cstart
                    if var_type == DEL or var_type == COM:
                        cpos = cpos - lenref + 1
                    elif var_type == INS:
                        cpos += 1
                apos = int((cpos - 1) / 3) + 1
            else:
                cpos = -1
                apos = -1
            # fill in missing base. # TODO: delete in the 2nd phase of this mapper.
            if ref_base_str == 'N' and kind == FRAG_CDS:
                codon = codonnum_to_codon[self._get_codons(tid, chrom, tstart, cstart, cpos)[0]]
                cpos_codonpos = cpos % 3
                base = codon[cpos_codonpos - 1]
                if strand == PLUSSTRAND:
                    crv_data['ref_base'] = base
                if strand == MINUSSTRAND:
                    crv_data['ref_base'] = rev_bases[base]
                tr_ref_base = base
            # so, refaa, altaa
            ref_aanums = []
            alt_aanums = []
            ref_codonnum = -1
            alt_codonnum = -1
            if var_type == SNV:
                so, ref_aas, alt_aas, achange, cchange, coding, csn = self._get_snv_map_data(tid, cpos, cstart, tpos, tstart, tr_ref_base, tr_alt_base, strand, kind, apos, gpos, start, end, chrom, fragno, lenref, lenalt, prevcont, nextcont)
            if var_type == INS:
                so, ref_aas, alt_aas, achange, cchange, coding, csn = self._get_ins_map_data(tid, cpos, cstart, tpos, tstart, tr_ref_base, tr_alt_base, strand, kind, apos, gpos, start, end, chrom, fragno, lenref, lenalt, prevcont, nextcont)
            if var_type == DEL:
                so, ref_aas, alt_aas, achange, cchange, coding, csn = self._get_del_map_data(tid, cpos, cstart, tpos, tstart, tr_ref_base, tr_alt_base, strand, kind, apos, gpos, start, end, chrom, gposendbin, gposend, fragno, lenref, lenalt, prevcont, nextcont)
            if var_type == COM:
                so, ref_aas, alt_aas, achange, cchange, coding, csn = self._get_com_map_data(tid, cpos, cstart, tpos, tstart, tr_ref_base, tr_alt_base, strand, kind, apos, gpos, start, end, chrom, gposendbin, gposend, fragno, lenref, lenalt, prevcont, nextcont)
            mapping = (uniprot, achange, so, tr, cchange, alen, genename, coding, csn)
            if genename not in all_mappings:
                all_mappings[genename] = []
            all_mappings[genename].append(mapping)
        primary_mapping = self._get_primary_mapping(all_mappings)
        crx_data = {x['name']:'' for x in cravat.constants.crx_def}
        crx_data.update(crv_data)
        crx_data['hugo'] = primary_mapping[MAPPING_GENENAME_I]
        crx_data['coding'] = primary_mapping[MAPPING_CODING_I]
        crx_data['transcript'] = primary_mapping[MAPPING_TR_I]
        crx_data['so'] = sonum_to_so[primary_mapping[MAPPING_SO_I]]
        crx_data['achange'] = primary_mapping[MAPPING_ACHANGE_I]
        amd = {}
        for genename in sorted(all_mappings.keys()):
            amd[genename] = []
            for mapping in all_mappings[genename]:
                amd[genename].append([mapping[MAPPING_UNIPROT_I], mapping[MAPPING_ACHANGE_I], sonum_to_so[mapping[MAPPING_SO_I]], mapping[MAPPING_TR_I], mapping[MAPPING_CCHANGE_I]])
        crx_data['all_mappings'] = json.dumps(amd)
        return crx_data, alt_transcripts

    def _get_splice_apos_prevfrag (self, tid, fragno, chrom):
        apos = -1
        so = SO_NSO
        csn = NOCSN
        for search_frag_no in range(fragno - 1, -1, -1):
            q = f'select kind, start, end, cstart from transcript_frags_{chrom} where tid={tid} and fragno={search_frag_no}'
            self.c2.execute(q)
            [kind, prev_frag_start, prev_frag_end, prev_frag_cpos] = self.c2.fetchone()
            if kind == FRAG_CDS:
                prev_last_cpos = prev_frag_cpos + (prev_frag_end - prev_frag_start)
                cpos_for_apos = prev_last_cpos - 1
                apos = int(cpos_for_apos / 3) + 1
                so = SO_SPL
                csn = SPLICE
                break
            elif kind == FRAG_UTR3 or kind == FRAG_UTR5 or kind == FRAG_UP2K or kind == FRAG_DN2K:
                apos = -1
                so = SO_INT
                csn = SPLICE
                break
        return apos, so, csn

    def _get_splice_apos_nextfrag (self, tid, fragno, chrom):
        apos = -1
        so = SO_INT
        csn = NOCSN
        q = f'select max(fragno) from transcript_frags_{chrom} where tid={tid}'
        self.c2.execute(q)
        max_fragno = self.c2.fetchone()[0]
        for search_frag_no in range(fragno + 1, max_fragno + 1, 1):
            q = f'select kind, cstart from transcript_frags_{chrom} where tid={tid} and fragno={search_frag_no}'
            self.c2.execute(q)
            [kind, next_frag_cpos] = self.c2.fetchone()
            if kind == FRAG_CDS:
                next_first_cpos = next_frag_cpos
                cpos_for_apos = next_first_cpos - 1
                apos = int(cpos_for_apos / 3) + 1
                so = SO_SPL
                csn = SPLICE
                break
            elif kind == FRAG_UTR3 or kind == FRAG_UTR5 or kind == FRAG_UP2K or kind == FRAG_DN2K:
                apos = -1
                so = SO_INT
                csn = SPLICE
                break
        if apos is None:
            raise
        return apos, so, csn

    def _get_ins_cds_so (self, tid, cpos, cstart, tpos, tstart, alt_base, chrom, strand, lenalt):
        if lenalt % 3 == 0:
            so = SO_INI
        else:
            so = SO_FSI
        ref_aas = ['_']
        alt_aas = ['_']
        return so, ref_aas, alt_aas

    def _get_svn_cds_so (self, tid, cpos, cstart, tpos, tstart, alt_base):
        [seq, ex] = self.mrnas[tid]
        cpos_codonstart = int((cpos - 1) / 3) * 3 + 1
        ref_codonnum = 0
        alt_codonnum = 0
        tpos_codonstart = tstart + (cpos_codonstart - cstart)
        alt_basebits = base_to_basenum(alt_base[0])
        for i in range(3):
            tpos_q = tpos_codonstart + i
            if tpos_q in ex:
                ref_codonnum = 0b10000000
                alt_codonnum = 0b10000000
                break
            seqbyteno = int((tpos_q - 1) / 4)
            seqbitno = ((tpos_q - 1) % 4) * 2
            basebits = (seq[seqbyteno] >> (6 - seqbitno)) & 0b00000011
            num_shift = (2 - i) << 1
            shifted_basebits = (basebits << num_shift)
            ref_codonnum = ref_codonnum | shifted_basebits
            if tpos_q == tpos:
                alt_codonnum = alt_codonnum | (alt_basebits << num_shift)
            else:
                alt_codonnum = alt_codonnum | shifted_basebits
        ref_aanum = codonnum_to_aanum[ref_codonnum]
        alt_aanum = codonnum_to_aanum[alt_codonnum]
        if ref_aanum != STP:
            if alt_aanum != STP:
                if ref_aanum != alt_aanum:
                    so = SO_MIS
                else:
                    so = SO_SYN
            else:
                so = SO_STG
        else:
            if alt_aanum != STP:
                so = SO_STL
            else:
                so = SO_SYN
        return so, ref_aanum, alt_aanum

    def _get_primary_mapping (self, all_mappings):
        primary_mapping = ('', '', SO_NSO, '', '', -1, '', '', NOCSN)
        for genename, mappings in all_mappings.items():
            for i in range(len(mappings)):
                mapping = mappings[i]
                if primary_mapping[MAPPING_SO_I] == SO_NSO:
                    primary_mapping = mapping
                elif _compare_mapping(mapping, primary_mapping) < 0:
                    primary_mapping = mapping
        return primary_mapping

    def _get_codons (self, tid, chrom, tstart, cstart, cpos_start, cpos_end=None):
        if cpos_end is None:
            cpos_end = cpos_start
        [seq, ex] = self.mrnas[tid]
        cpos_start_codonstart = int((cpos_start - 1) / 3) * 3 + 1
        tpos_start_codonstart = tstart + (cpos_start_codonstart - cstart)
        tpos_start_codonend = tpos_start_codonstart + 2
        cpos_end_codonstart = int((cpos_end - 1) / 3) * 3 + 1
        tpos_end_codonstart = tstart + (cpos_end_codonstart - cstart)
        tpos_end_codonend = tpos_end_codonstart + 2
        codonnums = []
        for tpos_codonstart in range(tpos_start_codonstart, tpos_end_codonend, 3):
            codonnum = 0
            for i in range(3):
                tpos = tpos_codonstart + i
                if tpos in ex:
                    codonnum = codonnum | 0b10000000
                    break
                else:
                    try:
                        seqbyteno = int((tpos - 1) / 4)
                        seqbitno = ((tpos - 1) % 4) * 2
                        base_bits = ((seq[seqbyteno] >> (6 - seqbitno)) & 0b00000011) << ((2 - i) << 1)
                        codonnum = codonnum | base_bits
                    except IndexError:
                        base = self.hg38reader[chrom][tpos - 1].upper()
                        if base == NBASECHAR:
                            codonnum = codonnum | 0b10000000
                            break
                        else:
                            base_bits = base_to_basenum(base) << ((2 - i) << 1)
                            codonnum = codonnum | base_bits
            if codonnum & 0b10000000 > 0:
                aanum = UNA
            else:
                aanum = codonnum_to_aanum[codonnum]
            codonnums.append(codonnum)
        return codonnums

    def summarize_by_gene (self, hugo, input_data):
        out = {}
        sos = list(set(input_data['so']))
        out['so'] = most_severe_so(sos)
        out['num_noncoding_variants'] = len([c for c in input_data['coding'] if c != 'Y'])
        out['num_coding_variants'] = len([c for c in input_data['coding'] if c == 'Y'])
        so_counts = {}
        all_mappings_lines = input_data['all_mappings']
        for lineno in range(len(all_mappings_lines)):
            line = all_mappings_lines[lineno]
            all_mappings = json.loads(line)
            numsample = input_data['numsample'][lineno]
            if hugo in all_mappings:
                counts = {}
                for mapping in all_mappings[hugo]:
                    so = mapping[2]
                    if so in gene_level_so_exclude:
                        continue
                    if so not in counts:
                        counts[so] = True
                for so in counts:
                    if so not in so_counts:
                        so_counts[so] = 0
                    so_counts[so] += numsample
        so_count_keys = list(so_counts.keys())
        so_count_keys.sort()
        so_count_l = ['{}({})'.format(so, so_counts[so]) for so in so_count_keys]
        out['all_so'] = ','.join(so_count_l)
        return out

    def empty_map (self, crv_data):
        return

if __name__ == '__main__':
    crv_data_snv = {'uid':1, 'chrom':'chr1', 'pos':155208824, 'ref_base':'C', 'alt_base':'T'}
    crv_data_ini = {'uid':1, 'chrom':'chr1', 'pos':155208824, 'ref_base':'-', 'alt_base':'TTT'}
    crv_data_ind = {'uid':1, 'chrom':'chr1', 'pos':155208824, 'ref_base':'CCC', 'alt_base':'-'}
    crv_data_fsi = {'uid':1, 'chrom':'chr1', 'pos':155208824, 'ref_base':'-', 'alt_base':'T'}
    crv_data_fsd = {'uid':1, 'chrom':'chr1', 'pos':155208824, 'ref_base':'C', 'alt_base':'-'}
    crv_data_com = {'uid':1, 'chrom':'chr1', 'pos':155208824, 'ref_base':'CA', 'alt_base':'TAA'}
    m = Mapper('', None, live=True)
    m.setup()
    for i in range(10000):
        crx_data = m.map(crv_data_snv)
        crx_data = m.map(crv_data_ini)
        crx_data = m.map(crv_data_ind)
        crx_data = m.map(crv_data_fsi)
        crx_data = m.map(crv_data_fsd)
        crx_data = m.map(crv_data_com)
