
import requests, os
section = 'technique','math'
matiere = 'physique','math'
def sawwr(t):
    print(f'{sect.upper()[0]}{mat[0:2]}{str(aam)}{sess[0].upper()}{t}')
#href="bac/2017/principale/technique/math.pdf"

dir_path = os.path.join(os.getcwd(), 'MSABB')
if not os.path.exists(dir_path):
    os.mkdir(dir_path, 0o666)

for sect in section:
    dir_path = os.path.join(os.getcwd(), f'MSABB\\BAC {sect}')
    if not os.path.exists(dir_path):
        os.mkdir(dir_path, 0o666)
    for mat in matiere:
        dir_path = os.path.join(os.getcwd(), f'MSABB\\BAC {sect}\\{mat}')
        if not os.path.exists(dir_path):
            os.mkdir(dir_path, 0o666)
        for aam in range(2020,2023):

            for sess in ('principale','controle'):
                sawwr(' Yetsabb..')
                s=False
                url = f'http://www.bacweb.tn/bac/{str(aam)}/{sess}/{sect}/{mat}.pdf'
                print(url)
                response = requests.get(url)
                if response.status_code == 200:
                    sawwr(' Tsabb.')
                    s=True
                    with open(os.path.join(dir_path, f'{mat.upper()}-{aam}-{sess[0].upper()}.pdf'), 'wb') as pdf:
                        for block in response.iter_content(chunk_size=1024):
                            pdf.write(block)
                if not(s):
                    sawwr(' Matsabbech.')