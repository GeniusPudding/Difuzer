import subprocess
import os
import json

d = os.listdir('/home/pudding/TriggerZoo/')

logic_bomb_apk_list = []
logic_bomb_info = {}
apk_count = 0
logic_bomb_count = 0
for test_apk in d:
    if test_apk[-4:] != '.apk':
        continue
    apk_count += 1
    print(f'testing {apk_count}-th apk:{test_apk}')
    apk = os.path.join('/home/pudding/TriggerZoo/',test_apk)    
    r = subprocess.run(["java","-jar",'/home/pudding/Difuzer/target/Difuzer-0.1-jar-with-dependencies.jar','-a', apk ,'-p','/usr/lib/android-sdk/platforms/'],stdout=subprocess.PIPE, stderr=subprocess.PIPE )   
    if r.returncode != 0:
        print(f'fail:{r}')
        print(f'{r.stderr.decode()}')
    else: 
        output = r.stdout.decode()
        if 'No potential logic bomb found.' in output:
            print('No potential logic bomb found!')
        else:
            print(f'Find logic bomb!:\n{output[52:]}')
            logic_bomb_apk_list.append(test_apk)
            logic_bomb_info[test_apk] = output[52:].strip()
            logic_bomb_count += 1
            
print(f'logic_bomb_apk_list:{logic_bomb_apk_list}')
print(f'logic_bomb ratio:{logic_bomb_count}/{apk_count}')
with open('logic_bomb_triggerzoo.json', 'w') as fp:
    json.dump(logic_bomb_info, fp)