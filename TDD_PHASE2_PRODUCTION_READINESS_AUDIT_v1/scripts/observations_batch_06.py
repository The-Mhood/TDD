#!/usr/bin/env python3
from record_listing import record,V
from pathlib import Path
import json
# Repair a local transcription omission, not a source change. The full first page
# was re-read (40 reported/40 compared) under e29aa923; original had 39 transcribed.
p=V/'listings/1D21SsmJ-y6omtWYF3krKRKHr6QehLgGO_p001.json'; old=json.loads(p.read_text())
es=old['entries']; missing={'id':'16EThfNteUovrmLIhB4a3zjudOyJ8Iiy7','name':'env_ch8x_mothers_b_gen3_v5.jpg','bytes':438654,'md5':'95c4ba3c5de55fd2d1d13923e0451676','drive_version':'3'}
if not any(x['id']==missing['id'] for x in es):es.insert(26,missing)
assert len(es)==40
rows='\n'.join('|'.join(map(str,[x['id'],x['name'],x['bytes'],x['md5'],x['drive_version']])) for x in es)
record('1D21SsmJ-y6omtWYF3krKRKHr6QehLgGO','e29aa923-67d3-4da5-a73d-42981abe397b',rows,next_token='~!!~AAfjczeHaX4iHpwiw_Q2fnOru_tWfbV4q16qSL-tjo7yt9AjJtBOEdDxqxx0lfkzczKQDSslJ4SUluT6vgPW-djUrohmAe5Tp1mvZiPa2AReHgga4Y_TPJzbDV447dpnbdAsJbPAuXzGCAklu-8qDn5V14ClaCzinz0vlcntqjqxnZaye5H6j2mnSSA5PytqqsLszhKe1T7Ef1-n001McVoWjxJQRsDx4vTh5mX1djCOoD4gnE8cE01v5ZMnX1Mu5h_OjAEJvXxdSh63_bKrihHSbnozywj5eJD20GXClIMsXMrfMcQjF0A8MYtYxJMIBEdjjgVUbWXyz7YnfZaMftpBW72KKX-1igTKG1g8Z7MRdSorCOiBr_SHjE-x-G7Mru4YTpy8jx9TkiyjGBSgKc3I26OCO6sLzJjJqSVV9A3bz3aerOeMnHkRNXNYh_4rRhf_aS4G1V4dnPueJhtVSDfU4IrtWKPDx8z2XXDT-__0hEKi32StOGI=',complete=False)
record('1D21SsmJ-y6omtWYF3krKRKHr6QehLgGO','84a311f9-f4e4-45a1-bb3b-001e2b633b77','''1M--UAmYdpSggQQI9Vn5IfEDvDFK83c5Y|idemili_master.jpg|321878|6d7061a03d89dbfaee845feb860b1c9d|3
1z5wmalCm8-F4lA4CXUo7GfQ1X8IDo99m|idemili_turnaround.jpg|516578|d7616a7e0fb03ceb2c9bc2e879caba26|3
1jNQ2H1r0SyyeMRVQ8p6j_tBqCbUeeT2j|master_keyart.jpg|362426|d5f6ff7ecde83435aef56c9c19161f52|3
1VqTfylcCmISGlRd8hYIE46kXCcsIBddM|master_keyart_v002.jpg|617661|9b1d319ec046e45d66100d11bd83da75|3
1xPOsRDVORLcD4kYPEZsVSfQivIYiIJ-W|master_keyart_v003.jpg|338560|98611fbf376a0c14c1a1f4b5647f832b|3
1fWEjQSm5Ipg0Aw3TxhLQqHh8AY9kI_UG|material_language.jpg|752966|c3f268d410492b5dcb67f6590d23e69a|3
10Z3-o4vJpVp3J9awcrxQSgx8k7Dp0mj-|nneka_living_memory.jpg|262354|9163883726b964f29d3342e8e9453c7a|3
1-_bsPUuQEmST71O5bNIIJc-Jr6pOCRgq|nneka_living_memory_v002.jpg|252043|01010cb8f139f70104fbf7c8d2c63e5e|3
1kMjOUdExy8MzlY_tpruutLDKSGCW0CPA|nneka_master_portrait.jpg|282155|6b967882afd5fb44702f41724aef6f19|3
1GDVbTJxel_6nHVbKiEf_4djyRVqxFKen|nneka_turnaround.jpg|202488|e735a7172fe87b764ab83ede2f1ddb04|3
1ubfF_KTbw43_CtF4L3Q8xQ7DfrY1IJL4|nneka_turnaround_v002.jpg|194428|2c3b20ae4df0601b87eb487e8e265d43|3
1HA-I4d5HK3-zoNik_Rzutp650EIiN_UJ|okwu_feature_exploration.jpg|341725|983f044b36f617ed44705b949ef7a4fb|3
1AYOwOHgLG7xc7EjOH6cZkVdOwETmHsgq|okwu_master_portrait.jpg|481498|0775cfb786b1fccff075a184787b55b3|3
1vtLRaiVHbFq6CC_tR7UqTFmFwiQuiJIv|okwu_turnaround.jpg|336090|f96c1e20731db8d8633b53eae2599d1b|3
18eBAeeAU9dg1_C2NNj12-ymNFZI0Mzvp|ref_env_hall_of_posts_approved.jpg|649361|525b9d5afdfdb19a310d8b034a4b12ca|3
1Q5rqEBrJs2fQbU3P3wEFQjh-2Qinj6Ef|ref_env_nnekas_house_approved.jpg|513982|6c654498c9596ea52487a8e7f60eb9b4|3
1RcXqsOHonRBc41jcVtaawT4XyXMpBSvh|ref_env_nnekas_interior_approved.jpg|625160|a46bd074b3fc32e49459c1ad3d2189cf|3
16Ri68cFZ-Hvw3z9RNn283gSzGJzDQQR9|ref_env_sealed_quarter_approved.jpg|680244|1478358ab514e12b39b47ee768ca1c7b|3
1ov7wnSEQddYd1comm5MPztotTgycuLBC|y_backrooms_v002.jpg|250775|e821d6308a4a52adbb586760bed7ad2c|3
1JCwNvYgjrLU1MCk1BaP31-hXjwlfr06g|y_court_v003.jpg|222297|95eac30503d1901acc4ab09729e9d995|3
14wwanqUnMnzUSd-rsG3z9Cs0N4xMpIMA|y_court_v003b.jpg|354212|947af88df837f985b24d4b51eea45df1|3
13x9wvglN7sga4akc83a_xujYCFRf-qdN|y_gathering_v003.jpg|277769|858357e97be0897ee42524469d9d1801|3
1Eax4Y_30Qvsqk9raNJgeNjgd0wd9gU_L|y_guard_v002.jpg|208381|4b5e7281ca94873cbefec1e509a885a2|3
1YUVKvFFMmFbwrqYU3WOoONSc2f3HzKZM|y_hall_v003.jpg|183361|20aa8b74ac822ecf9f570c114b1a2a20|3
1XgDL8UbwhPIVAkWXt2_pnKYb8ERn0WlB|y_interior_v003.jpg|183162|06c29a94d69650d1fec380303941b9a7|3
1ZtnVxYDEmwF0zGpLBxLFrHPsnH4w3XKi|y_seal_v005.jpg|185023|a84ff7d06a6f34dcd4244440565077b3|3
1Ehdol1tQpugFGggaS__o8O1O2ra0dp0e|y_washing_v002.jpg|256840|48ed195f98b9c9d4170b09d783266a1b|3''',page=2)
record('1oEzqRhlmwKPlvkXvxjNSBp8_y98WHkEu','e6004f23-5ed4-4f5b-8090-f59824df97d8','1CMW978LfSYtR0SRAgnqKZkk0gNY_rpqF|REF_ADANNA_MASTER_PORTRAIT_APPROVED_V001.jpg|387742|827d464b159059a201def413957d9c4d|3')
record('1r3I96R5lJvHBotYzf0Ek8Jfno3lC4bKy','151db8a3-e92e-4bcf-80f9-b0b24ab20119','''1YU_5PoER-i6MxLiUno6G2Qh7-sD6ayiQ|REF_ORIGINAL_MOODBOARD_GAME_ART_BIBLE_V001.jpg|684359|9c735b2c636c50d19d59df15e198044e|3
1clpz22ZWm8hizXn6pOgPhuok-Qdlvku3|REF_ORIGINAL_MOODBOARD_WORLD_BIBLE_V001.jpg|659444|eb708538497a475a1af056699b891a93|3
1AghCYjiJ6B-pV-JbtHIEPSKoDy1Mi13e|REF_ORIGINAL_MOODBOARD_WORLDBUILDING_V001.jpg|588787|74ed7fe4b2cf83032ebd41bda55c0928|3''')
record('1rkIaRwJMxA_7rJLstzRTlk1v0jowexLQ','4285fc25-2525-4832-a87e-c7997d058f0e')
