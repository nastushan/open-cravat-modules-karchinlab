import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):

    def annotate(self, input_data):
        out = {}
        chrom = input_data['chrom']
        pos = input_data['pos']
        ref = input_data['ref_base']
        alt = input_data['alt_base']
        
        q = '''select af,AFR_AF,AMR_AF,EAS_AF,EUR_AF,SAS_AF,
        	ACB_AF,ASW_AF,BEB_AF,CDX_AF,CEU_AF,CHB_AF,CHS_AF,CLM_AF,ESN_AF,FIN_AF,
        	GBR_AF,GIH_AF,GWD_AF,IBS_AF,ITU_AF,JPT_AF,KHV_AF,LWK_AF,MSL_AF,MXL_AF,
        	PEL_AF,PJL_AF,PUR_AF,STU_AF,TSI_AF,YRI_AF from thousandgenomes_%s where position=%s and refbase="%s" and altbase="%s";''' \
            %(chrom, pos, ref, alt)
        self.cursor.execute(q)
        self.logger.info(q)
        result = self.cursor.fetchone()
#        result = self.cursor.fetchall()
        if result:
            out['af'] = result[0] 
            out['afr_af'] = result[1] 
            out['amr_af'] = result[2] 
            out['eas_af'] = result[3] 
            out['eur_af'] = result[4] 
            out['sas_af'] = result[5] 
            out['acb_af'] = result[6] 
            out['asw_af'] = result[7] 
            out['beb_af'] = result[8] 
            out['cdx_af'] = result[9] 
            out['ceu_af'] = result[10] 
            out['chb_af'] = result[11] 
            out['chs_af'] = result[12] 
            out['clm_af'] = result[13] 
            out['esn_af'] = result[14] 
            out['fin_af'] = result[15] 
            out['gbr_af'] = result[16] 
            out['gih_af'] = result[17] 
            out['gwd_af'] = result[18] 
            out['ibs_af'] = result[19] 
            out['itu_af'] = result[20] 
            out['jpt_af'] = result[21] 
            out['khv_af'] = result[22] 
            out['lwk_af'] = result[23] 
            out['msl_af'] = result[24] 
            out['mxl_af'] = result[25] 
            out['pel_af'] = result[26] 
            out['pjl_af'] = result[27] 
            out['pur_af'] = result[28] 
            out['stu_af'] = result[29] 
            out['tsi_af'] = result[30] 
            out['yri_af'] = result[31] 
        return out
    def cleanup(self):
        pass

if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()