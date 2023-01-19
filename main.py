
import requests, os
#Example: Year:2022, Session:principale, Section:math, Matiere (Subject):math 
#href="http://www.bacweb.tn/bac/2022/principale/math/math.pdf"

aam_range = 2020,2023 #Year Range
session = 'principale','controle'
section = 'technique','math'
matiere = 'physique','math'

def sawwr(t): #Prints State
    print(f'{sect} {mat} {aam} {sess}{t}'.upper())

#Create a Folder named MSABB
dir_path = os.path.join(os.getcwd(), 'MSABB')
if not os.path.exists(dir_path):
    os.mkdir(dir_path, 0o666)


for sect in section: #Create a Folder of the Section
    dir_path = os.path.join(os.getcwd(), f'MSABB\\BAC {sect}')
    if not os.path.exists(dir_path):
        os.mkdir(dir_path, 0o666)

    for mat in matiere: #Create a Folder of the "Matiere" inside the Section
        dir_path = os.path.join(os.getcwd(), f'MSABB\\BAC {sect}\\{mat}')
        if not os.path.exists(dir_path):
            os.mkdir(dir_path, 0o666)

        for aam in range(*aam_range): #Loop through the years (aam).
            for sess in (session): #Loop through the sessions
                sawwr(' Yetsabb..') #Prints about being Downloaded..
                s=False
                url = f'http://www.bacweb.tn/bac/{str(aam)}/{sess}/{sect}/{mat}.pdf'
                response = requests.get(url)
                if response.status_code == 200: #Success
                    sawwr(' Tsabb.\n') #Prints about geting Downloaded.
                    s=True
                    with open(os.path.join(dir_path, f'{mat.upper()}-{aam}-{sess[0].upper()}.pdf'), 'wb') as pdf: #Create the pdf.
                        for block in response.iter_content(chunk_size=1024):
                            pdf.write(block)

                if not(s): #Fail
                    sawwr(' Matsabbech.') #Prints about not getting downloaded.