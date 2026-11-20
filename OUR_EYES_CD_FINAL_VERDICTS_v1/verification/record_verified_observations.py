#!/usr/bin/env python3
"""Normalize observed connector listings, then reconcile against fixed identities.
These are manually transcribed observations, NOT raw API captures. IDs below
were copied from successful post-filing list_files responses in this execution.
No Drive request or mutation is performed here.
"""
from pathlib import Path
import json,collections,hashlib,shutil
from PIL import Image
BASE=Path(__file__).resolve().parents[1]
REPO=BASE.parent
SCOPE=json.loads((BASE/'verification/SOURCE_SCOPE_193.json').read_text())
F=json.loads((BASE/'verification/DESTINATION_FOLDERS.json').read_text())
CORR=json.loads((BASE/'correction_evidence/CORRECTION_ATTEMPTS.json').read_text())
COPY=json.loads((BASE/'verification/copy_plan.json').read_text())
META={r['source_id']:{'name':r['name'],'kind':'original','code':r['code']} for r in SCOPE}
META.update({r['new_drive_id']:{'name':r['output_name'],'kind':'new_derivative','code':r['source_code']+'_DERIVATIVE'} for r in CORR})
META.update({F[k]['id']:{'name':F[k]['path'].split('/')[-1],'kind':'preserved_container','code':k} for k in ['original_container','assistant_container']})
RAW={
'visual_release':('02f0c091-50e0-4719-bcf4-125e70f46151','''1CKaEzdNb-Xom9W0DprYxMtPspIphuFqi 1bs7I2_iPaWQMANPkCLu8YA3x_24FiS9n 1SR7CRZC9MZjTBsEi84_N3b4sesAmDsiq 1OwSkuBRB1VMKdI7iPE4sYw3xypr-EyZD 1GTFnMdZMqesUXdWeLhFApVdiRsownwb0 1lnMePbbXNHmDZTnbmcJW47RGbMtIfjo4'''),
'rejected':('f461ade1-e3b4-48ec-bd57-a5dc22540bc4','''1VTA7bi3rAcf8o_oTXmmqQS3AjIkrt63H 1CFCPrQct-qvsw662-wOZAngxiXAOMfw3 1TdWrO3lkNCTHPqlrAgjFKkBfeth9wowP 1C--Ojw2kN2G_-VmHbac4lMXEDRLJslyb 17uomx2sn8Jp8p7GZQFqzJz7zlBNOThg7 1FodM5tkMCetTrp3e1ln4T-_Fb9rKGuv3 1y4efClikpBy8l_MgzOJjvSnq7ASYbR1_ 145CTWxRCA0LQtYj3QNTGqFGNVmPLwSgg 1oMCsvO-dsL01rMpli_e1mwJs5wty-A57 1w0sSsFVxbPKPScXVHAZvj7wBHK7DnYCu 1uUV4ZaZekbL3MfyTfCZDBdLXuj2NFP3s'''),
'superseded':('440c600d-f70d-4461-9964-b89b372b2b29','''1IhgfuIFZ5wOj4Wb0KpTrYQcyj57nT9Pz 1sixVQ4I9wsgJbEOSfssCVsXRcrIG3x7R 1cKZa4flUbjidGKo5dHZECfJF9hf75RdW 1YF2yq80Bxzz9wGOn7C4GzkzaFgApJqe- 1KyoNo4wBHp6GG_2Ad2MdYew-cKLYHpaz 1r5SIMNFxa1CRTgFnA-4yugnvykBBch4F 1YJqo7pZRuq1hOHpfsiBp9Amiv8SHGJQp 1xSJ6QJBwA2eQsatcYgM_hHBrhEAvz_5d 1SLxYu-Fez5qGeo1gpZbILWXy_Y_9WHco 1OmXsyhC7HZJrZuLjFqBKNkpAq4lqUWf2 16yJsFYZRa3iE1VAtAqhBTAI3JLuUdCmT 1JWX8z0UcLpqUXouXMJzSyWvMsVxTjxPI 1MA20ws6ujgQazDb66BgDOHIjrNgfT29x 1nYt7Tvoyn7Q5179ITrgJhCjY5gb4MmyY 1nNFdXOcJYpojq1PYmRsOuZTn5wBRBIq8 1rYwLsX0S-MlqK-UArMF3MHUu1qc0QhwN 1Wj41WxKZ_kqLWRqJz2PQFr1EYWSqj9vR 1QtJIm1YcL8orW7pNBRZDyLCdPG-RtCGo 1P-PjtOw4TrIjmN3uZsrFZF0NDjzgfHSv 1DtT7wfMJt63S_oGN-cIKuzR__7oDAqRG 1RcEkIjAlMqO6cvKhwALy9gveVL07gOCK 10Apn34FkRedH1E5NXGCa9KSZ1Dh42SJK 1xxQFlOkqg045hnmWm-wJY428u0xSV3-K 18RHdPeQM-WUSA9N0dvliTi4WWqsfcFVX'''),
'aids':('b71e67ee-c609-4bb8-afe0-b060c26ebb97','''1X-eO-Svbzo46ozPXbsE-JpT4SEfWMgOw 1j03tjjtHXt6s5iHJfgJS3M_j17aNmiMg 1Rxo6My76m13XUAEVS00M3-bVzMVIxQgb 1OOnKZsctqMp19dzMhTrDqFLTTzRoRMf1 1s28ocisLsI-BOpGMY65MMT-yU9hbHDOY 1a4dO7GjSe89mDr1xQXWf2iszj8wAblgh 1pijFOgm8JQJNn_2xe4rk3wK4dOYjeYw0 11MmHTZ-CawZrvknG21bsgqqKXJ-7x2nP 14uOMGJYXucAHpfCByFi8TW_i1ZxriKMy 1566AiHfIYW0b03yU_R8dHZg_zoGDWsDb 17PXQi9TGyQvMcNynmmnYzOsJFKLQczTX 1JCpUGC37IkeiokNd77cP6I75k5l7tET4 1CZbSP1PY9LBeoA65WMgmhBZhqFVlH9f6 1LMwXIN3whaxctH9BQ9xJS9tEVIT6-mtj 1kto-RyzxZFt_QgxAK_-UKFpeykFsin7H 1cWfqzGqDckOzKsZtrDCnxajdM5jkygq3 1CWfG8a7YxBXRdC_2RB8bWwgUqwprAZ1M 16nRB4iN6OAco8K5XN4OKfCqNAOAnNz1E 1lXvNjgnJpWxAlGsRzozDYvVUrd_6gums 1Hl40ep9LfPsb2JqQCFjq6TCtTVrwtKnT 1gDpiCSJVuhSFUgRpuN9t_dBR4_n3oegj 1T9Eziwd_5UcVfBXgxdi_-7Cvr1XYkT3J 1A10-FlflAwN3yuI_OVpgRSPS_nl0eCk0 1FSpdjZBhXqzaRXBDt8WzB_HFxdAVjnJk 1NQCWe-zXx7D88p4GnCWqv42IAsQHva1s 1aENkNhoAZJewZD6GR1cniUtRnqR_0ctf 1Vyt8yjZAcy8uqMUSZEWDludc5k74rAix 1uHEH6I8SKhwpeA1C38tsarzLNBACDWny 1IljvE5kdAQKj-GXJbpTFCTcu2KKXK_4a 12v0y9sOdgbn7ZBFBMdUDPOh64EtpyW02 1gcB6yB2ERgfTn1mzWBF43_k-k51uR0TM 1HWiL2cB_DYiDG2Kfi3NpeOA_RwdYrPeG 118DT3OivKh789heYdQRUuXlIc7NcK7mG 1v_Sls4vJNSVZHF5XV-RHEM-PQ2c9ImmV 1oGedLDNFIWEa2rQybWpIdY0NuEtKQ7pX'''),
'studies':('af5b0df1-fcdb-4fb2-9124-8f05539db094','''10f6Xgh0PSv3fkDYADSz1sGKFIC6kd3np 1b2vTn10kpAsmmMaN53yzQ8G4pJZc1wR0 1hQqFawUsv8oM_aX_4JJNqqkBmVoiTmvd 1p1erIKGaOy4UX3MWCFgJTnIAcX1XSz0e 1gAun9ET_l0Ro8-oD2yIeKILp9jBx0rjJ 1_Lw07vpd0aOo0XnI7-xrbWZTWhypg7vU 1TBXHgJlUmmbMWcMhG9PQn0eS07bdbum9 1npYn0kJB2FFjTxPyGdACAsCqKk8ZbDPq 1Ji0NUXNJfos4Qvodp8ZNWIzlxAcUWOTk 1oGMObicz17rFr3O-HRXjjvRIbS2W3QQJ 1N9evqu7rf1BspncPBVZZVAs_HKv-ZCkA 1ffC9c575D2fzrH_aahnokHg8GXpd5_63 1iR48S7upDhIp-zQ_cVqHTcS8V66xH2Gl 1xtum5Ln3jiXSwtXQJVLr1jw55EnfvmJw 1OnmKtOuDB2CaYb71HfzxznLCcLF7un5t 1hldnXwv2_grB2Q6YWvQFRPdcIs3dR_h3 1keM066YH3olFbX5b1xhxbKqIITSeTJrG 136GaYOi8QJFC60xb9hfmtr3bp_Rdn2vp 1hTmInOVfZ_EIHzv4RWIM_BzGru-r4uOp 1xDJaz1ip1sU4mNFkUpjjPFcCkOGu1d-N 1MuhupyLWP2fqLn0mhfAzXXTjy0q6sqa0'''),
'corrections':('2627b1ca-4a1e-41e2-97cd-1b2be6c0a5a8','''1Slo9WE8ezx6yDe-zS-moGTItO-f1dQ_t 1lrjAnGZRQ7srJxZMTg7Gs7wxZUlDEm_H 1Zjbufzzg6J4eL-OEKVZgBgNV8hMw1lig 16E4umob2MQdXGMRt1M9upT5yYOJ8-3UV'''),
'external':('eed0a913-e084-4f07-93c9-17a7f4cc5a59','''1s2nj3g1sIoeG_GSOZx80h4gWPAOCii1B 1rWjKHHTvwL7oxaqVs8W1oGO2Vqyvm5Ff 1Ra_Aqb6OIzStdjRhT4lldGlatTuH6sef 1nIDlHOGiJbm7MEJ9xt3MJjsC7hAVz_60 1e98rcp-QG7u5z9ihXmbabgGDXe94XTEa 13Dc48FnSA9nvCUzL2zBq6zNv6axFLtIG 1OB-WeC6Z6hrOt3oQquEYoOZ-ICrpbRW2 1lPnwpnYUXtsVdPAqmVPK0Wu-54vu58dt 1C_jk77ERIws4CsKIyHD1txrfBWwAaiSp 1_vJFw7KNJRn435OijQHdjDhds0G-gF6n'''),
'documents':('8f145352-4f17-4aaf-9013-283b95345c4a','''1CSiUHZDyE4NsKxIYEcUYSPFepYQBpOyp 1YUCfczTDGsdcMGz3favvphMabMR9q9PJ 16p2TYXn16u9UNdMlJzjTK873YK_Fk7Ab'''),
'original_container':('ce83e98b-5a3a-465e-900d-e49ad98caddc','''1GbksU93uvNp26nSVs2sx0msW0CNW-acn 1imiOKufYUwaj-hcc6ojlbQTwKnmUjGON 1mRYoJ71IRUz3HS1G19luJMFCJxjv3-th 14JDeODzhfPwOuCgXPezYYMlyjMGGdC-N 1ei3sAwJ6AQ3CU3fCAZ8FqR2JldJWRc8y 1y2nF2o_KEALA29pJyfjU7oF-aQaXm1Y- 1B0qMXM87r7vP5kBahTCckDRXdz70JLmm 1OE2u-yuZz2IfyF0iVPzUzfkC-YUAzldj 1qbi6WbMMAWgCuWycafd9oJJTTJiaInaG 1VB5s6b3_tuiC475Aq7Z86XaBdPACu1db 1G6aHuFTCfTR5HkxirpnAf4tn9LuEG-SX 1meBZkmzfDX8HY38DbqIdhVDwc7F2WfyE 19Ct7vvsF0xa-ClBi621JVkpxGrzgJQlf 1dZ2ufTteb_IOV6SR3B5z5zqTkYGFjq25 1xI5v1ZfeXyxE-laueJRmWsymvlFkJGgl 18Ehnq1cIcE6eu8fE7Wzidk9aDfNm9aTI 1k2_5AUOonHKDyxCHpgY_o3IYTAdzEjX8 1gN2UYAAP0liFmCgQMJjJhskj2D0BAmQW 1m32I8rIheLcbUG8NAWF1b1DbUSHE4b7H'''),
'assistant_container':('eb756e50-afc9-4816-b60f-b3b381748deb','''12Lkat1YdzLdBKPkMHMJUIjTSFzuEQAHB 1gCIEHoYYFlPzvQ6gzEqKoGACu_xR4Lsz 1_2wlaIkVKLdDBSHJYnH5pmcJWhoKJz2F 19L_kdq4w5q0jZiCZfHc5j07Tx_oTrOdI 1hkFxPg1TwJN4tZDevMuk-2coi6XoGmV8 1NXUmIb5B4yIXKETU5q3CtsqBW7CC67GC 15vfEEcf1zelEbQ0aAKUD18sWvOjC75FO 1l1tDDWtklqknUP7k7JkzHeVMmJLYocF3 1KvQ8UTXo9dRexWJpgI-6FduOKRRdan8d 14t17-fgr9WExEx202HSQxCeoU9gMVLL- 17Z0oh9v3a9M7Ct2iLu2O0aAs3oEwxEUw 1WDUWvm66odU4igHjVazyV5JAzAQ6Qx05 1tJ4K-u_vlnw3QC6HmIt3sxoz2KucRhBl 1Cyu8qfaPdbu3lzWq_PaiD7UrFDIDc_jz 1iaev_4IWhgU95v--1S75_NP32dJaTEeJ 1i1gv_CHPnUj-xpr7Gvx06JLxp_BEHk6l 1hY4f3JNYFDBvCA7nGoBfCWexJIYUymUR 1ko3w_HJjtpcIWRPNMVlbu9R3XWMTOGrY 12PYjx-mGY86qFkpobliG46-DFklLzdga 1ivS14J-IkNs9BkyXqfh0Sy5K0gDJusK8 1lyjvnekcrBHdU03Ya5cNCwFaVjSnD45a 1CQkT3YpHES7krjjGB93bZqERKwe0zv0j 1fQJ3dMve_bbUF53IhulvpLmOqIh9kL0b 1Q6RvgWZegMMO5md0N8HQvP7gTIRu5EwE 1qvIe2S7rmJA0G9eiGsCMvg4HckXAUYSu 1w5eDzRwcqRTUwDaifnlwK-i4f56wFRGa 13aJGxM20F9FCorGDq-2g4DbnDdpTDUlZ 11hnYj5qH7LRCD90XUq0M8H3kaBHpLdCN 1vA4D8DM3ihztefYbeywPXOAUZjLx18ri 13AXeI5-Cy7mvuvor4V86Y0Plv2midqqx 1Ay5cP6XKdVc6YWptNgmK0x4liB-PT-wn 1-QexQjgdEF8B6qdy3nRWX2GwH6LH7YeJ 1kyG28U9QT6meBdGpDxN0JDpYt20AdOYZ 1XTPF-QmHfQ16e8oOVTGNOHT0ojuJ11Wu 1sQLIp0vR0a7A1NRslMatte-aMnSdcKz_ 1obe3Ry3B8TJosyB4bVyVRUWih-eCNS2l 1QUoYd7yCFGsD9pPrSm7tRSPccHs-R0So 1lAESDSpwgtLNr4rjc2RKDEJ4WDU4--lU 1dh3CH91t-C6wUV8XHEMREX_w883AReMG 12gTdtxR76qB_5916pRV_R1p1xK0cl9w3 1epIa9TkphMfiZgNLnySH5vDwkpJXJ-bs 1hoh64TdMya1jCslKC_xGARuvsDfHlPOo 1h_s2Zaw5lCgn1ewptkbze4LJsoalrm-4 1WLiqPhYiU6DVsFZaFvOge-0DH89uh-Mr 12D8gVf8cqfSQQzghzJtr026lenc38iI9 1huW7ymhmxkwA2u3hQ-5ijRO33Mv3RLjj 1tshnIBY20TF2dhveqYjDy0oDC29wTmfz 14reSojyyOr-qbvuFwJP-sOqCcNSvq95e 1uvSrH46ihg7ZNYwBKFNDYQiVUJtalN1H 1aa3rlVl9mm7S-YYq80eu3mQAQhiYFPwx 1QFFfLHwn1GmfGGi9oqhdzLyy8QsAqJQc 1I9BzFKPkSpJ8BQa8KVnb79DU26YAsJ00 1RO7-agpxO92Vp7ifjB34WEjXCJ5MXobA 1fNCoel_Z7KnlrMzMBUutBiJEDJ2X9nj0 1Wwsibgrlr8bJevMjkRclaQ-iJ-SFgbE_ 1sRagEJxToeZFTWy7Anx60dVonXRNvDSR 1mODNxtojxzg8UHjSBuRiXMsKRfYAQofw 1fEhvp7x5KK4j8XxxkGmbXk-KTNXSQU3e 12WJLRjnQ6IJoMsYigJMQYN7Boy_wEuSo 1vqo8RMnVh1UQZNREGwBPFPcIHX88OmDl 1u_ey_gPxdTM5862Bw_3cfhm3NMcETMxL 1xDhCmsNgh1xGweNfqldm70AbCTw7CwuL 1WlPZ0g2zcQPvdGXna-xGfm6XTSf9MbCB 1QFJ_9JSjmgNIiRhncDWfObk_cJsfi5SU 1DbUGmu9tmbdKoTmmBBIJ0PgIelRY_icd 1LVTcBLlt5eWhbOdX3uqJ3EPIc-_Fv4u5 1xPD33CTWybukTy10WP5TLN9k6XK3fkFy 1U4xF6NUFrVnSEW3ljz5_FBUWOYMOsZYD'''),
'pending':('b2996140-82b7-4306-b254-4b1afc33e920','')}
expected_counts={'visual_release':6,'rejected':11,'superseded':24,'aids':35,'studies':21,'corrections':4,'external':10,'documents':3,'original_container':19,'assistant_container':68,'pending':0}
master=json.loads((BASE/'A_MASTER_FINAL_VERDICT_REGISTER.json').read_text())
expected_parent={r['source_id']:r['final_parent_id'] for r in master}
expected_parent.update({r['new_drive_id']:F['studies' if r['source_code'] in ['D03','D06','E46','E50'] else 'corrections']['id'] for r in CORR})
expected_parent.update({F[k]['id']:F['documents']['id'] for k in ['original_container','assistant_container']})
observations=[];seen={}
for key,(request,ids) in RAW.items():
 ids=ids.split();assert len(ids)==expected_counts[key],(key,len(ids))
 assert len(ids)==len(set(ids));names=[];files=[]
 for ident in ids:
  assert ident in META,(key,ident,'unknown');assert ident not in seen,(ident,'duplicate location');assert expected_parent[ident]==F[key]['id'],(key,ident,'wrong parent')
  seen[ident]=F[key]['id'];m=META[ident];names.append(m['name']);files.append({'id':ident,'name_joined_to_fixed_identity':m['name'],'code':m['code'],'kind':m['kind']})
 assert len(names)==len(set(names)),(key,'name collision')
 observations.append({'destination_key':key,'folder_id':F[key]['id'],'query':f"'{F[key]['id']}' in parents and trashed = false",'connector_response_request_id':request,'observed_total':len(ids),'next_page_token':None,'incomplete_search':False,'observed_ids':ids,'files':files,'observed_names_and_parents_checked_against_fixed_identity':True,'basis':'Manually transcribed complete successful post-filing connector listing, not a raw API capture. Names are canonical joins after manual equality check of named listing/download. Assistant IDs were re-enumerated lean; named listing and separate F45 get_file confirm names/parents.'})
assert len(seen)==201
assert all(r['source_id'] in seen for r in master)
p=BASE/'verification/destination_payload_checks.json';checks=json.loads(p.read_text());assert len(checks)==193
for r in checks:
 assert seen[r['source_id']]==r['expected_final_parent_id'];assert r['source_sha256_match'] and r['open_check']['open_success']
 r['destination_listing_verified']=True;r['observed_final_parent_id']=seen[r['source_id']];r['complete_destination_verified']=True
p.write_text(json.dumps(checks,indent=2)+'\n')
(BASE/'verification/destination_listing_observations.json').write_text(json.dumps(observations,indent=2)+'\n')
p=BASE/'verification/move_ledger.json';moves=json.loads(p.read_text());assert len(moves)==106
for r in moves:r['post_move_download_verified']=True;r['destination_listing_verified']=True
p.write_text(json.dumps(moves,indent=2)+'\n')
# Separately observed package-copy locations.
PF=json.loads((BASE/'verification/package36_folders.json').read_text())
PC={
'release':('708e77dd-ea19-4d53-bf12-f173df649677','''1ltlaigJOtaNs-sJjr0jwApZiWhT3PyMG 1uCO473-hYNmWcsHU16imkARfF6h79gzp 1Clz61vqjKFcV7mSX5EMyjb1qnFg8rAjM 1EuBi0RNpYkqsy9KW65rX8q6NPGl0P4q9 1vFG-hpej16w4ikMaAxZ1bfmJVscw7skp 1X5tsb3_KSYPlAzMZEzCqNa6l5bMA-r3M 10ukVC-rOfhe9txoqIzosArcreKzprcmZ 1VTtkDNbnxdepMGqLWLDoELD4sDLKJ3fX 1krucyyjoC1ZGwCeu2XLSmR3LbXOHPOhf 1N4AnEYjJFjq70E4qQcytXo-jHUaxUSfm 1_evuFIDG6nFE6IuR3pe3v2h7oz0YE7gA 1u8_dLZNYXRK5k0cZHUq9Ds8jDPXW8Krq 1-_IdFS1-ySQ4X_BwGrceiSSsuqSq31yl 1OY1TO4QdVOKTeBvV-E0ih8heJZK-xuL6 1X7D9PNnS4q_s0f5ogvPw0LnKcnQzVnmE 1M1mnXP91wQOW0Wr87tPDAcxd9J0OF9BG 1FheMKP-cRN7pjqMNbVwpwK-4VVKQ7rZY'''),
'reference':('9414643d-ad30-41d7-8d9e-eeecfcc04341','''1Ggh6doQ6IPBqPz4Mvq2NaEj0J8dDI5Qj 1rsTokmziVOT_vs8lvo_0meFdjelaj-mL 1GcfptqCp9Qg4z7LA0SEejlwbYqiZozbu 1hgzdUHVEgeO5AUrW5hfwy0RTvaB0hP17 1ne1I9N4HyEmEpAKmD1UNVmpMvP6RHEL0 15Lu7Y6aoRUdyv6QfKXsIf5pJtGx9zi63 1xo0PkGFH_BjrKpKgqMMx2Cbf0WfTErNP 1OPxsdTwfNRJ7nCZGRnV-xqIngS7O5LkB'''),
'external':('5faaa6a9-3884-48ed-a54d-599a60c89adb','''184RRp01AWkqYGGFUVLAI7yrT2tfcDqsE 1Dk8uuVjAXVj1GOv1VXmiW-TfFaKYEU_w 1r63KEc8JczN-UMih1Zsb9hslX03zlxo4 1upDzPg-CMUNg6alk9VsZrvdlLHKYbAVI 1QVLe6dh5pA4jXQ_mYQhN5GAS3367dz3k 1N-o3NotlbzRrLwM1NpAtfk34vXT0lfo0 1aHbIZPm4H8JAimpdVA8ZPFjyu4m8-B2U'''),
'rejected':('4ddee291-d021-4ed3-b1ef-84189893c762','''1pUpVCU2jXcLpocm45Bmo7oLtDU_1h8Nb 1hPVGS7pL-fbND1MWJlRbbAWrpTVK7v3v'''),
'replacements':('4202403e-2094-4bd3-bcbf-432a271343c1','''1Ug908Xf-JSL18TAFWamzb1C_SkfZgYin 16tTxehEYQ86VwyivcqGtMiqHR-ci8_Dd 12GOMXfKY2hTenIGj8BwUVcJmjQ6WzwGx 1HP2m8e0z8Ug7_4_yeJal3zVvj18luRa6''')}
copyby={r['new_id']:r for r in COPY};assert len(copyby)==38
copyobs=[];copyseen=set()
for key,(request,ids) in PC.items():
 ids=ids.split();names=[]
 for ident in ids:
  assert ident in copyby and ident not in copyseen;copyseen.add(ident);r=copyby[ident];assert r['destination_id']==PF[key]
  names.append(r['name']);r['destination_listing_verified']=True
 assert len(names)==len(set(names))
 copyobs.append({'folder_key':key,'folder_id':PF[key],'connector_response_request_id':request,'observed_ids':ids,'observed_total':len(ids),'next_page_token':None,'incomplete_search':False,'basis':'Manually transcribed complete named listing; no raw API capture.'})
assert len(copyseen)==38 and not copyseen.intersection(seen)
# These exact 38 copy IDs were downloaded after the originals were independently
# snapshotted; they cannot be confused with the original-ID download evidence.
copychecks=[];snap=REPO/'_final_release_stage/verified_package_copies';snap.mkdir(exist_ok=True)
for r in COPY:
 p=REPO/'google_drive'/r['name'];data=p.read_bytes();md5=hashlib.md5(data).hexdigest();sha=hashlib.sha256(data).hexdigest()
 assert len(data)==r['source_size'] and md5==r['source_md5'] and sha==r['source_sha256'],r['code']
 with Image.open(p) as im:im.load();dimensions=list(im.size)
 r['download_verified']=True;r['open_verified']=True;r['complete_copy_verified']=True
 dest=snap/r['code']/r['name'];dest.parent.mkdir(exist_ok=True);shutil.copy2(p,dest)
 copychecks.append({'code':r['code'],'new_id':r['new_id'],'original_or_derivative_id':r['source_id'],'md5':md5,'sha256':sha,'bytes':len(data),'dimensions':dimensions,'full_decode_success':True,'download_by_copy_id_after_original_snapshot':True,'listed_in_expected_parent':True})
(BASE/'verification/copy_plan.json').write_text(json.dumps(COPY,indent=2)+'\n')
(BASE/'verification/copy_payload_checks.json').write_text(json.dumps(copychecks,indent=2)+'\n')
(BASE/'verification/copy_listing_observations.json').write_text(json.dumps(copyobs,indent=2)+'\n')
clearance={'status':'PENDING CLEARED','scope_originals':193,'initial_pending_original_files':193,'initial_submission_containers':2,'direct_file_moves':106,'originals_relocated_by_two_container_moves':87,'original_destinations_payload_and_parent_verified':193,'original_total_bytes':70416758,'original_hash_mismatches':0,'original_open_failures':0,'duplicate_destination_names_observed':0,'missing_originals':0,'pending_remaining_files':0,'pending_remaining_folders':0,'pending_scan_complete':True,'pending_next_page_token':None,'pending_incomplete_search':False,'pending_query':"'11DxQ0d_noAPbZCPrYQBkUonHFl_cFAWm' in parents and trashed = false",'pending_response_request_id':RAW['pending'][0],'new_derivatives':6,'selected_derivatives':4,'failed_derivatives_not_replacements':2,'intentional_held_original_copies_verified':36,'intentional_selected_derivative_copies_verified':2,'all_external_authority_cases_still_unapproved':10,'qualification':'Administrative physical clearance only, not universal creative/cultural/production approval. Observed connector results are manually normalized; hashes/open tests are independently computed. No claim that raw API responses were archived.'}
(BASE/'verification/PHYSICAL_CLEARANCE.json').write_text(json.dumps(clearance,indent=2)+'\n')
print(json.dumps(clearance,indent=2))
