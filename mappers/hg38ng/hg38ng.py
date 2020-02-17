from supersqlite import sqlite3
import cravat
import pickle
from collections import OrderedDict
import time
import os
import json
from cravat.util import most_severe_so
from cravat.constants import gene_level_so_exclude
import importlib

# strands
PLUSSTRAND = 1
MINUSSTRAND = -1
# bases
ADENINE = 0
THYMINE = 1
GUANINE = 2
CYTOSINE = 3
base_dict = {ADENINE: 'A', THYMINE: 'T', GUANINE: 'G', CYTOSINE: 'C'}
base_to_basenum = {'A': ADENINE, 'T': THYMINE, 'G': GUANINE, 'C': CYTOSINE}
rev_bases = {'A':'T', 'T':'A', 'G':'C', 'C':'G', '-':'-'}
# frag kind
UP2K = -10
UTR5 = -5
CDS = 1
NCRNA = 2
INTRON = 0
UTR3 = 5
DN2K = 10
# variant kind
SNV = 1
INS = 2
DEL = 3
COM = 4
# sequence ontology
NSO = 0
D2K = 1
U2K = 2
UT3 = 3
UT5 = 4
INT = 5
UNK = 6
SYN = 7
MIS = 8
CSS = 9
IND = 10
INI = 11
STL = 12
SPL = 13
STG = 14
FSD = 15
FSI = 16
# csn: coding, splice, noncoding (legacy from old hg38)
CODING = -1
SPLICE = -2
NONCODING = -3
sonum_to_so = {
    D2K: '2KD',
    U2K: '2KU',
    UT3: 'UT3',
    UT5: 'UT5',
    INT: 'INT',
    UNK: 'UNK',
    SYN: 'SYN',
    MIS: 'MIS',
    CSS: 'CSS',
    IND: 'IND',
    INI: 'INI',
    STL: 'STL',
    SPL: 'SPL',
    STG: 'STG',
    FSD: 'FSD',
    FSI: 'FSI',
    NSO: '',
}
# aa
NDA = -10
NOA = -2
UNA = -1
STP = 0
ALA = 1
CYS = 2
ASP = 3
GLU = 4
PHE = 5
GLY = 6
HIS = 7
ILE = 8
LYS = 9
LEU = 10
MET = 11
ASN = 12
PRO = 13
GLN = 14
ARG = 15
SER = 16
THR = 17
VAL = 18
TRP = 19
TYR = 20
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
    for i in range(len(codon)):
        codonnum = codonnum | base_to_basenum[codon[i]] << ((2 - i) << 1)
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

class Mapping:
    def __init__ (self, uniprot=None, achange=None, so=NSO, tr=None, cchange=None, aalen=-1, genename=None, coding=None, csn=NONCODING):
        self.uniprot = uniprot
        self.achange = achange
        self.so = so
        self.tr = tr
        self.cchange = cchange
        self.aalen = aalen
        self.genename = genename
        self.coding = coding
        self.csn = csn

    def better_than (self, mapping):
        better_csn = self.csn > mapping.csn
        same_csn = self.csn == mapping.csn
        acceptable_uniprot = self.uniprot is not None or mapping.uniprot is None
        #same_uniprot = ((self.uniprot is None) and (mapping.uniprot is None)) or ((self.uniprot is not None) and (mapping.uniprot is not None))
        higher_so = self.so > mapping.so
        same_so = self.so == mapping.so
        longer_aa = self.aalen > mapping.aalen
        same_aalen = self.aalen == mapping.aalen
        #self_is_better = (self.uniprot is not None or mapping.uniprot is None) and (higher_so or (same_so and longer_aa))
        #self_is_better = (better_csn) or ((same_csn and acceptable_uniprot) and (higher_so or (same_so and longer_aa)))
        self_is_better = (better_csn) or ((same_csn) and (higher_so or (same_so and longer_aa)))
        # TODO: revert below back to correct logic.
        #if better_uniprot or (same_uniprot and higher_so) or (same_uniprot and same_so and longer_aa):
        if self_is_better:
            return True
        else:
            return False

    def __repr__ (self):
        return str([self.genename, self.uniprot, self.achange, self.so, self.tr, self.cchange, self.coding])

    def _get_crx_data (self):
        return [self.uniprot, self.achange, sonum_to_so[self.so], self.tr, self.cchange]

class Mapper (cravat.BaseMapper):
    def setup (self):
        self.module_dir = os.path.dirname(__file__)
        data_dir = os.path.join(self.module_dir, 'data')
        db_path = os.path.join(data_dir, 'gene_24_10000_old.sqlite')
        db = self._get_db(db_path)
        self.c = db.cursor()
        self.c2 = db.cursor()
        q = 'select v from info where k="binsize"'
        self.c.execute(q)
        self.binsize = int(self.c.fetchone()[0])
        q = 'select v from info where k="gencode_ver"'
        self.c.execute(q)
        self.ver = self.c.fetchone()[0]
        mrnas_path = os.path.join(data_dir, 'mrnas_24_old')
        f = open(mrnas_path, 'rb')
        self.mrnas = pickle.load(f)
        f.close()
        self.logger.info(f'mapper database: {db_path}')
        self._make_refseqs()

    def _make_refseqs (self):
        t = time.time()
        q = f'select t.tid, t.name, t.strand, t.refseq, t.uniprot, t.aalen, g.desc from transcript as t, genenames as g where t.genename=g.genename'
        self.c.execute(q)
        self.tr_info = {}
        for r in self.c.fetchall():
            (tid, name, strand, refseq, uniprot, aalen, genename) = r
            refseqs = refseq.split(',')
            self.tr_info[tid] = [name, strand, refseqs, uniprot, aalen, genename]
        print(f'@ tr_info made in {time.time() - t:.2f}s')

    def _get_db (self, db_path):
        t = time.time()
        db = sqlite3.Connection(':memory:')
        diskdb = sqlite3.Connection(db_path)
        diskdb.backup(db)
        '''
        if importlib.util.find_spec('apsw') is not None:
            import apsw
            self.logger.info(f'using in-memory db')
            db = apsw.Connection(':memory:')
            diskdb = apsw.Connection(db_path)
            db.backup('main', diskdb, 'main').step()
        else:
            self.logger.info(f'using disk db')
            db = sqlite3.connect(db_path)
        '''
        return db

    def get_addl_tr_info (self, tid):
        q = f'select t.name, t.strand, t.uniprot, t.aalen, t.refseq, g.desc from transcript as t, genenames as g where t.tid={tid} and t.genename=g.genename'
        self.c2.execute(q)
        row = self.c2.fetchone()
        return row

    def _get_snv_map_data (self, tid, cpos, cstart, tpos, tstart, tr_ref_base, tr_alt_base, strand, kind, apos, gpos, start, end, chrom, fragno):
        if kind == CDS:
            so, ref_aanum, alt_aanum = self._get_svn_cds_so(tid, cpos, cstart, tpos, tstart, tr_alt_base, strand)
            ref_aas = [aanum_to_aa[ref_aanum]]
            alt_aas = [aanum_to_aa[alt_aanum]]
            achange = f'{"".join(ref_aas)}{apos}{"".join(alt_aas)}'
            cchange = f'{tr_ref_base}{cpos}{tr_alt_base}'
            coding = 'Y'
            csn = CODING
        elif kind == UTR5:
            so = UT5
            achange = None
            cchange = None
            ref_aas = [aanum_to_aa[NDA]]
            alt_aas = [aanum_to_aa[NDA]]
            coding = ''
            csn = NONCODING
        elif kind == UTR3:
            so = UT3
            achange = None
            cchange = None
            ref_aas = [aanum_to_aa[NDA]]
            alt_aas = [aanum_to_aa[NDA]]
            coding = ''
            csn = NONCODING
        elif kind == INTRON:
            achange = None
            cchange = None
            coding = ''
            if gpos == start or gpos == start + 1:
                so = SPL
                csn = SPLICE
                ref_aas = [aanum_to_aa[NOA]]
                alt_aas = [aanum_to_aa[NOA]]
                apos = self._get_splice_apos_plusstrand(tid, fragno, chrom)
                achange = f'{"".join(ref_aas)}{apos}{"".join(alt_aas)}'
            elif gpos == end or gpos == end - 1:
                so = SPL
                csn = SPLICE
                ref_aas = [aanum_to_aa[NOA]]
                alt_aas = [aanum_to_aa[NOA]]
                apos, so, csn = self._get_splice_apos_minusstrand(tid, fragno, chrom)
                achange = f'{"".join(ref_aas)}{apos}{"".join(alt_aas)}'
            else:
                so = INT
                csn = NONCODING
                ref_aas = [aanum_to_aa[NDA]]
                alt_aas = [aanum_to_aa[NDA]]
        elif kind == NCRNA:
            so = UNK
            achange = None
            cchange = None
            ref_aas = [aanum_to_aa[NDA]]
            alt_aas = [aanum_to_aa[NDA]]
            coding = ''
            csn = NONCODING
        elif kind == UP2K:
            so = U2K
            achange = None
            cchange = None
            ref_aas = [aanum_to_aa[NDA]]
            alt_aas = [aanum_to_aa[NDA]]
            coding = ''
            csn = NONCODING
        elif kind == DN2K:
            so = D2K
            achange = None
            cchange = None
            ref_aas = [aanum_to_aa[NDA]]
            alt_aas = [aanum_to_aa[NDA]]
            coding = ''
            csn = NONCODING
        return so, ref_aas, alt_aas, achange, cchange, coding, csn

    def _get_ins_map_data (self, tid, cpos, cstart, tpos, tstart, tr_ref_base, tr_alt_base, strand, kind, apos, gpos, start, end, chrom, alt_base, fragno):
        if kind == CDS:
            so, ref_aas, alt_aas = self._get_ins_cds_so(tid, cpos, cstart, tpos, tstart, alt_base, chrom, strand)
            achange = f'{"".join(ref_aas)}{apos}{"".join(alt_aas)}'
            cchange = f'{tr_ref_base}{cpos}{tr_alt_base}'
            coding = 'Y'
            csn = CODING
        elif kind == UTR5:
            so = UT5
            achange = None
            cchange = None
            ref_aas = [aanum_to_aa[NDA]]
            alt_aas = [aanum_to_aa[NDA]]
            coding = ''
            csn = NONCODING
        elif kind == UTR3:
            so = UTR3
            achange = None
            cchange = None
            ref_aas = [aanum_to_aa[NDA]]
            alt_aas = [aanum_to_aa[NDA]]
            coding = ''
            csn = NONCODING
        elif kind == INTRON:
            achange = None
            cchange = None
            coding = ''
            if gpos == start or gpos == start + 1:
                so = SPL
                csn = SPLICE
                ref_aas = [aanum_to_aa[NOA]]
                alt_aas = [aanum_to_aa[NOA]]
                apos = self._get_splice_apos_plusstrand(tid, fragno, chrom)
                achange = f'{"".join(ref_aas)}{apos}{"".join(alt_aas)}'
            elif gpos == end or gpos == end - 1:
                so = SPL
                csn = SPLICE
                ref_aas = [aanum_to_aa[NOA]]
                alt_aas = [aanum_to_aa[NOA]]
                apos, so, csn = self._get_splice_apos_minusstrand(tid, fragno, chrom)
                achange = f'{"".join(ref_aas)}{apos}{"".join(alt_aas)}'
            else:
                so = INT
                csn = NONCODING
                ref_aas = [aanum_to_aa[NDA]]
                alt_aas = [aanum_to_aa[NDA]]
        elif kind == NCRNA:
            so = UNK
            achange = None
            cchange = None
            ref_aas = [aanum_to_aa[NDA]]
            alt_aas = [aanum_to_aa[NDA]]
            coding = ''
            csn = NONCODING
        elif kind == UP2K:
            so = U2K
            achange = None
            cchange = None
            ref_aas = [aanum_to_aa[NDA]]
            alt_aas = [aanum_to_aa[NDA]]
            coding = ''
            csn = NONCODING
        elif kind == DN2K:
            so = D2K
            achange = None
            cchange = None
            ref_aas = [aanum_to_aa[NDA]]
            alt_aas = [aanum_to_aa[NDA]]
            coding = ''
            csn = NONCODING
        return so, ref_aas, alt_aas, achange, cchange, coding, csn

    def _get_del_map_data (self, tid, cpos, cstart, tpos, tstart, tr_ref_base, tr_alt_base, strand, kind, apos, gpos, start, end, chrom, gposendbin, gposend, lenref, fragno):
        q = f'select kind from transcript_frags_{chrom} where tid={tid} and binno={gposendbin} and start<={gposend} and end>={gposend}'
        self.c2.execute(q)
        gposend_kind = self.c2.fetchone()
        if gposend_kind is not None:
            gposend_kind = gposend_kind[0]
        if kind != gposend_kind:
            so = UNK
            coding = ''
            achange = None
            cchange = None
            csn = NONCODING
            ref_aas = [aanum_to_aa[NDA]]
            alt_aas = [aanum_to_aa[NDA]]
        else:
            if kind == CDS:
                ref_aas = [aanum_to_aa[NOA]]
                alt_aas = [aanum_to_aa[NOA]]
                lenref_3 = lenref % 3
                if lenref_3 == 0:
                    so = IND
                else:
                    so = FSD
                achange = f'{"".join(ref_aas)}{apos}{"".join(alt_aas)}'
                cchange = f'{tr_ref_base}{cpos}{tr_alt_base}'
                coding = 'Y'
                csn = CODING
            elif kind == UTR5:
                so = UT5
                achange = None
                cchange = None
                ref_aas = [aanum_to_aa[NDA]]
                alt_aas = [aanum_to_aa[NDA]]
                coding = ''
                csn = NONCODING
            elif kind == UTR3:
                so = UT3
                achange = None
                cchange = None
                ref_aas = [aanum_to_aa[NDA]]
                alt_aas = [aanum_to_aa[NDA]]
                coding = ''
                csn = NONCODING
            elif kind == INTRON:
                achange = None
                cchange = None
                coding = ''
                if gpos == start or gpos == start + 1:
                    so = SPL
                    csn = SPLICE
                    ref_aas = [aanum_to_aa[NOA]]
                    alt_aas = [aanum_to_aa[NOA]]
                    apos = self._get_splice_apos_plusstrand(tid, fragno, chrom)
                    achange = f'{"".join(ref_aas)}{apos}{"".join(alt_aas)}'
                elif gpos == end or gpos == end - 1:
                    so = SPL
                    csn = SPLICE
                    ref_aas = [aanum_to_aa[NOA]]
                    alt_aas = [aanum_to_aa[NOA]]
                    apos = self._get_splice_apos_plusstrand(tid, fragno, chrom)
                    achange = f'{"".join(ref_aas)}{apos}{"".join(alt_aas)}'
                else:
                    so = INT
                    csn = NONCODING
                    ref_aas = [aanum_to_aa[NDA]]
                    alt_aas = [aanum_to_aa[NDA]]
            elif kind == NCRNA:
                so = UNK
                achange = None
                cchange = None
                ref_aas = [aanum_to_aa[NDA]]
                alt_aas = [aanum_to_aa[NDA]]
                coding = ''
                csn = NONCODING
            elif kind == UP2K:
                so = U2K
                achange = None
                cchange = None
                ref_aas = [aanum_to_aa[NDA]]
                alt_aas = [aanum_to_aa[NDA]]
                coding = ''
                csn = NONCODING
            elif kind == DN2K:
                so = D2K
                achange = None
                cchange = None
                ref_aas = [aanum_to_aa[NDA]]
                alt_aas = [aanum_to_aa[NDA]]
                coding = ''
                csn = NONCODING
        return so, ref_aas, alt_aas, achange, cchange, coding, csn

    def _get_com_map_data (self, tid, cpos, cstart, tpos, tstart, tr_ref_base, tr_alt_base, strand, kind, apos, gpos, start, end, chrom, gposendbin, gposend, lenref):
        if lenref > 1:
            q = f'select kind from transcript_frags_{chrom} where binno={gposendbin} and start<={gposend} and end>={gposend} and tid={tid}'
            self.c2.execute(q)
            gposend_kind = self.c2.fetchone()
            if gposend_kind is not None:
                gposend_kind = gposend_kind[0]
        else:
            gposend_kind = kind
        if kind != gposend_kind:
            so = UNK
            coding = ''
            achange = None
            cchange = None
            csn = NONCODING
        else:
            if kind == CDS:
                so = CSS
                achange = None
                cchange = None
                ref_aas = [aanum_to_aa[NOA]]
                alt_aas = [aanum_to_aa[NOA]]
                achange = f'{"".join(ref_aas)}{apos}{"".join(alt_aas)}'
                cchange = f'{tr_ref_base}{cpos}{tr_alt_base}'
                coding = 'Y'
                csn = CODING
            elif kind == UTR5:
                so = UT5
                achange = None
                cchange = None
                ref_aas = [aanum_to_aa[NDA]]
                alt_aas = [aanum_to_aa[NDA]]
                coding = ''
                csn = NONCODING
            elif kind == UTR3:
                so = UTR3
                achange = None
                cchange = None
                ref_aas = [aanum_to_aa[NDA]]
                alt_aas = [aanum_to_aa[NDA]]
                coding = ''
                csn = NONCODING
            elif kind == INTRON:
                achange = None
                cchange = None
                coding = ''
                if gpos == start or gpos == start + 1:
                    so = SPL
                    csn = SPLICE
                    ref_aas = [aanum_to_aa[NOA]]
                    alt_aas = [aanum_to_aa[NOA]]
                    apos = self._get_splice_apos_plusstrand(tid, fragno, chrom)
                    achange = f'{"".join(ref_aas)}{apos}{"".join(alt_aas)}'
                elif gpos == end or gpos == end - 1:
                    so = SPL
                    csn = SPLICE
                    ref_aas = [aanum_to_aa[NOA]]
                    alt_aas = [aanum_to_aa[NOA]]
                    apos, so, csn = self._get_splice_apos_minusstrand(tid, fragno, chrom)
                    achange = f'{"".join(ref_aas)}{apos}{"".join(alt_aas)}'
                else:
                    so = INT
                    csn = NONCODING
                    ref_aas = [aanum_to_aa[NDA]]
                    alt_aas = [aanum_to_aa[NDA]]
            elif kind == NCRNA:
                so = UNK
                achange = None
                cchange = None
                ref_aas = [aanum_to_aa[NDA]]
                alt_aas = [aanum_to_aa[NDA]]
                coding = ''
                csn = NONCODING
            elif kind == UP2K:
                so = U2K
                achange = None
                cchange = None
                ref_aas = [aanum_to_aa[NDA]]
                alt_aas = [aanum_to_aa[NDA]]
                coding = ''
                csn = NONCODING
            elif kind == DN2K:
                so = D2K
                achange = None
                cchange = None
                ref_aas = [aanum_to_aa[NDA]]
                alt_aas = [aanum_to_aa[NDA]]
                coding = ''
                csn = NONCODING
        return so, ref_aas, alt_aas, achange, cchange, coding, csn

    def _get_tr_map_data (self, chrom, gpos):
        gposbin = int(gpos / self.binsize)
        q = f'select * from transcript_frags_{chrom} where binno={gposbin} and start<={gpos} and end>={gpos}'
        self.c.execute(q)
        ret = self.c.fetchall()
        '''
        q = f'select f.*, t.strand, t.name, g.desc, t.uniprot, t.aalen from transcript_frags_{chrom} as f, transcript as t, genenames as g where f.binno={gposbin} and f.start<={gpos} and f.end>={gpos} and t.tid=f.tid and t.genename=g.genename'
        self.c.execute(q)
        ret = self.c.fetchall()
        '''
        return ret

    #@profile
    def map (self, crv_data):
        lentr_ref_base = -1
        tpos = -1
        uid = crv_data['uid']
        chrom = crv_data['chrom']
        gpos = crv_data['pos']
        ref_base = crv_data['ref_base']
        alt_base = crv_data['alt_base']
        lenref = len(ref_base)
        lenalt = len(alt_base)
        if ref_base == '-' and alt_base != '-' and lenalt >= 1:
            var_type = INS
        elif alt_base == '-' and ref_base != '-' and lenref >= 1:
            var_type = DEL
        elif ref_base != '-' and alt_base != '-' and lenref == 1 and lenalt == 1:
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
            #[tid, fragno, start, end, kind, exonno, tstart, cstart, binno, strand, tr, genename, uniprot, aalen] = r
            [tid, fragno, start, end, kind, exonno, tstart, cstart, binno] = r
            [tr, strand, refseqs, uniprot, aalen, genename] = self.tr_info[tid]
            #strand = int(strand)
            if tr not in alt_transcripts:
                alt_transcripts[tr] = []
            for refseq in refseqs:
                if refseq not in alt_transcripts[tr]:
                    alt_transcripts[tr].append(refseq)
            if strand == PLUSSTRAND:
                tpos = gpos - start + tstart 
                tr_ref_base = ref_base
                tr_alt_base = alt_base
            elif strand == MINUSSTRAND:
                tpos = end - gpos + tstart
                tr_ref_base = ''.join([rev_bases[b] for b in ref_base])
                tr_alt_base = ''.join([rev_bases[b] for b in alt_base])
                tr_ref_base = tr_ref_base[::-1]
                tr_alt_base = tr_alt_base[::-1]
            lentr_ref_base = len(tr_ref_base)
            # cpos, apos
            if kind == CDS:
                if strand == PLUSSTRAND:
                    cpos = gpos - start + cstart
                else:
                    cpos = end - gpos + cstart
                    if var_type == DEL or var_type == COM:
                        cpos = cpos - len(tr_ref_base) + 1
                    elif var_type == INS:
                        cpos += 1
                apos = int((cpos - 1) / 3) + 1
            else:
                cpos = -1
                apos = -1
            # so, refaa, altaa
            ref_aanums = []
            alt_aanums = []
            ref_codonnum = -1
            alt_codonnum = -1
            if var_type == SNV:
                so, ref_aas, alt_aas, achange, cchange, coding, csn = self._get_snv_map_data(tid, cpos, cstart, tpos, tstart, tr_ref_base, tr_alt_base, strand, kind, apos, gpos, start, end, chrom, fragno)
            if var_type == INS:
                so, ref_aas, alt_aas, achange, cchange, coding, csn = self._get_ins_map_data(tid, cpos, cstart, tpos, tstart, tr_ref_base, tr_alt_base, strand, kind, apos, gpos, start, end, chrom, alt_base, fragno)
            if var_type == DEL:
                so, ref_aas, alt_aas, achange, cchange, coding, csn = self._get_del_map_data(tid, cpos, cstart, tpos, tstart, tr_ref_base, tr_alt_base, strand, kind, apos, gpos, start, end, chrom, gposendbin, gposend, lenref, fragno)
            if var_type == COM:
                so, ref_aas, alt_aas, achange, cchange, coding, csn = self._get_com_map_data(tid, cpos, cstart, tpos, tstart, tr_ref_base, tr_alt_base, strand, kind, apos, gpos, start, end, chrom, gposendbin, gposend, lenref)
            mapping = Mapping(uniprot, achange, so, tr, cchange, aalen, genename, coding, csn)
            if genename not in all_mappings:
                all_mappings[genename] = []
            all_mappings[genename].append(mapping)
        primary_mapping = self._get_primary_mapping(all_mappings)
        crx_data = {x['name']:'' for x in cravat.constants.crx_def}
        crx_data.update(crv_data)
        crx_data['hugo'] = primary_mapping.genename
        crx_data['coding'] = primary_mapping.coding
        crx_data['transcript'] = primary_mapping.tr
        crx_data['so'] = sonum_to_so[primary_mapping.so]
        crx_data['achange'] = primary_mapping.achange
        amd = {}
        for genename in sorted(all_mappings.keys()):
            if genename not in amd:
                amd[genename] = []
            for mapping in sorted(all_mappings[genename], key=lambda mapping: mapping.tr):
                amd[genename].append(mapping._get_crx_data())
        #crx_data['all_mappings'] = json.dumps(amd, separators=(',', ':'))
        crx_data['all_mappings'] = amd
        return crx_data, alt_transcripts

    def _get_splice_apos_plusstrand (self, tid, fragno, chrom):
        apos = None
        so = None
        csn = None
        for search_frag_no in range(fragno - 1, -1, -1):
            q = f'select kind, start, end, cpos from transcript_frags_{chrom} where tid={tid} and fragno={search_frag_no}'
            self.c2.execute(q)
            [kind, prev_frag_start, prev_frag_end, prev_frag_cpos] = self.c2.fetchone()
            if kind == CDS:
                prev_last_cpos = prev_frag_cpos + (prev_frag_end - prev_frag_start)
                apos = int((prev_last_cpos - 1) / 3) + 1
                so = SPL
                csn = SPLICE
                break
            elif kind == UTR3 or kind == UTR5 or kind == UP2K or kind == DN2K:
                apos = -1
                so = INT
                csn = SPLICE
                break
        if apos is None:
            raise
        return apos, so, csn

    def _get_splice_apos_minusstrand (self, tid, fragno, chrom):
        apos = None
        so = None
        csn = None
        q = f'select max(fragno) from transcript_frags_{chrom} where tid={tid}'
        self.c2.execute(q)
        max_fragno = self.c2.fetchone()[0]
        for search_frag_no in range(fragno + 1, max_fragno + 1, 1):
            q = f'select kind, start, end, cpos from transcript_frags_{chrom} where tid={tid} and fragno={search_frag_no}'
            self.c2.execute(q)
            [kind, next_frag_start, next_frag_end, next_frag_cpos] = self.c2.fetchone()
            if kind == CDS:
                next_first_cpos = next_frag_cpos
                apos = int((next_first_cpos - 1) / 3) + 1
                so = SPL
                csn = SPLICE
                break
            elif kind == UTR3 or kind == UTR5 or kind == UP2K or kind == DN2K:
                apos = -1
                so = INT
                csn = SPLICE
                break
        if apos is None:
            raise
        return apos, so, csn

    def _get_ins_cds_so (self, tid, cpos, cstart, tpos, tstart, alt_base, chrom, strand):
        if len(alt_base) % 3 == 0:
            so = INI
        else:
            so = FSI
        ref_aas = ['_']
        alt_aas = ['_']
        '''
        ref_codonnum = self._get_codons(tid, chrom, tstart, cstart, cpos, cpos)[0]
        ref_aanum = codonnum_to_aanum[ref_codonnum]
        ref_aas = [aanum_to_aa[ref_aanum]]
        ref_codonpos = (cpos - 1) % 3
        ref_codon = codonnum_to_codon[ref_codonnum]
        new_bases = ref_codon[:ref_codonpos] + alt_base + ref_codon[ref_codonpos:]
        lennew = len(new_bases)
        lennew_3 = lennew % 3
        alt_aas = ''
        if lennew_3 == 0:
            so = INI
            for i in range(0, len(new_bases), 3):
                alt_aas += codon_to_aa[new_bases[i:i+3]]
        else:
            so = FSI
            stp_found = False
            ll = lennew - lennew_3
            for i in range(0, ll, 3):
                new_aanum = codon_to_aanum[new_bases[i:i+3]]
                alt_aas += aanum_to_aa[new_aanum]
                if new_aanum == STP:
                    stp_found = True
                    break
            if stp_found == False:
                rem_bases = new_bases[ll:]
                len_rembases = len(rem_bases)
                len_rembases_rem = len_rembases % 3
                for i in range(0, len_rembases - len_rembases_rem, 3):
                    alt_aas += codon_to_aa[rem_bases[i:i+3]]
                    new_aanum = codon_to_aanum[rem_bases[i:i+3]]
                    if new_aanum == STP:
                        stp_found = True
                        break
                if stp_found == False:
                    rem_bases_rem = rem_bases[-len_rembases_rem:]
                    q = f'select start, end from transcript_frags_{chrom} where tid={tid} and kind={DN2K}'
                    self.c2.execute(q)
                    rs = self.c2.fetchall()
                    if strand == PLUSSTRAND:
                        r = rs[-1]
                        gpos_post_tr = r[0]
                        if len_rembases_rem > 0:
                            tmp_bases = self.hg38reader[chrom][gpos_post_tr - 1:gpos_post_tr + (3 - len_rembases_rem) - 1].upper()
                            codon = rem_bases_rem + tmp_bases
                            aanum = codon_to_aanum[codon]
                            aa = codon_to_aa[codon]
                            alt_aas += aa
                            if aanum == STP:
                                stp_found = True
                        if stp_found == False:
                            gpos_search_start = gpos_post_tr + (3 - len_rembases_rem)
                            for gpos_search in range(gpos_search_start, gpos_search_start + 300, 3):
                                codon = self.hg38reader[chrom][gpos_search:gpos_search + 3].upper()
                                aa = codon_to_aa[codon]
                                aanum = codon_to_aanum[codon]
                                alt_aas += aa
                                if aanum == STP:
                                    stp_found = True
                                    break
                            if stp_found == False:
                                alt_aas += '?'
                    elif strand == MINUSSTRAND:
                        r = rs[0]
                        gpos_post_tr = r[1]
                        if len_rembases_rem > 0:
                            tmp_bases = self.hg38reader[chrom][gpos_post_tr - (3 - len_rembases_rem):gpos_post_tr].upper()
                            codon = rem_bases_rem + tmp_bases
                            aanum = codon_to_aanum[codon]
                            aa = codon_to_aa[codon]
                            alt_aas += aa
                            if aanum == STP:
                                stp_found = True
                        if stp_found == False:
                            gpos_search_start = gpos_post_tr - len_rembases_rem
                            for gpos_search in range(gpos_search_start, gpos_search_start + 300, 3):
                                codon = self.hg38reader[chrom][gpos_search:gpos_search + 3].upper()
                                aa = codon_to_aa[codon]
                                aanum = codon_to_aanum[codon]
                                alt_aas += aa
                                if aanum == STP:
                                    stp_found = True
                                    break
                            if stp_found == False:
                                alt_aas += '?'
                ref_codonnum = self._get_codons(tid, chrom, tstart, cstart, cpos, cpos)[0]
        '''
        return so, ref_aas, alt_aas

    def _get_svn_cds_so (self, tid, cpos, cstart, tpos, tstart, alt_base, strand):
        [seq, ex] = self.mrnas[tid]
        cpos_codonstart = int((cpos - 1) / 3) * 3 + 1
        ref_codonnum = 0
        alt_codonnum = 0
        tpos_codonstart = tstart + (cpos_codonstart - cstart)
        alt_basebits = base_to_basenum[alt_base]
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
                    so = MIS
                else:
                    so = SYN
            else:
                so = STG
        else:
            if alt_aanum != STP:
                so = STL
            else:
                so = SYN
        return so, ref_aanum, alt_aanum

    def _get_primary_mapping (self, all_mappings):
        primary_mapping = Mapping()
        for genename, mappings in all_mappings.items():
            for mapping in mappings:
                if primary_mapping is None or mapping.better_than(primary_mapping):
                    primary_mapping = mapping
        return primary_mapping

    '''
    def _get_codon (self, tid, tstart, cstart, cpos, altbase=None):
        [seq, ex] = self.mrnas[tid]
        cpos_codonstart = int((cpos - 1) / 3) * 3 + 1
        tpos_codonstart = tstart + (cpos_codonstart - cstart)
        tpos = tstart + (cpos - cstart)
        ref_codonnum = 0
        alt_codonnum = 0
        for i in range(3):
            tpos_codon = tpos_codonstart + i
            if tpos_codon in ex:
                ref_codonnum = 0b10000000
                alt_codonnum = 0b10000000
                break
            else:
                seqbyteno = int((tpos_codon - 1) / 4)
                seqbitno = ((tpos_codon - 1) % 4) * 2
                base_bits = (seq[seqbyteno] >> (6 - seqbitno)) & 0b00000011
            num_shift = (2 - i) << 1
            ref_codonnum += base_bits << num_shift
            if altbase:
                if tpos_codon == tpos:
                    alt_codonnum += base_to_basenum[alt_base] << num_shift
                else:
                    alt_codonnum += base_bits << num_shift
        ref_aanum = codonnum_to_aanum[ref_codonnum]
        alt_aanum = codonnum_to_aanum[alt_codonnum]
        return ref_codonnum, ref_aanum, alt_codonnum, alt_aanum
    '''

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
                        if base == 'N':
                            codonnum = codonnum | 0b10000000
                            break
                        else:
                            base_bits = base_to_basenum[base] << ((2 - i) << 1)
                            codonnum = codonnum | base_bits
            if codonnum & 0b10000000 > 0:
                aanum = UNA
            else:
                aanum = codonnum_to_aanum[codonnum]
            codonnums.append(codonnum)
        return codonnums

    '''
    def _get_cdna_bases_until_end (self, tid, cpos_start, cstart, tstart):
        [seq, ex] = self.mrnas[tid]
        tpos_start = tstart + (cpos_start - cstart)
        codonnums = []
        for tpos in range(tpos_start_codonstart, tpos_end_codonend, 3):
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
                        base = self.hg38reader[chrom][tpos - 1]
                        if base == 'N':
                            codonnum = codonnum | 0b10000000
                            break
                        else:
                            base_bits = base_to_basenum[base] << ((2 - i) << 1)
                            codonnum = codonnum | base_bits
            if codonnum & 0b10000000 > 0:
                aanum = UNA
            else:
                aanum = codonnum_to_aanum[codonnum]
            codonnums.append(codonnum)
        return codonnums
    '''

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
