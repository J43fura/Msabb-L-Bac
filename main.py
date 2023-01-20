
import requests, os
import flet as ft

aam_range = [2020,2023] #Year Range
sessions = 'principale','controle'
matieres_fix = 'physique','math','philo','francais','arabe','anglais'
section_matieres = {
    'math' : ['info','svt',*matieres_fix],
    'sciences_ex' : ['info','svt',*matieres_fix],
    'economie_gestion' : ['economie','gestion','his_geo','info',*matieres_fix],
    'technique' : ['technique','info',*matieres_fix],
    'lettre' : ['pensee','his_geo','info','svt',*matieres_fix],
    'sport' : ['sport','info','svt',*matieres_fix],
    'informatique' : ['bd','algorithme',*matieres_fix]
    }
matieres=[]

options = 'theatre','artistique','musique','italien','portugais','turque','chinois','russe','espagnol','allemand'



#FLUT
def main(page:ft.Page):
    page.theme_mode=ft.ThemeMode.DARK
    page.window_height=700
    page.window_width=500
    page.title="Msabb l BAC"
    page.scroll=True

    page.add(ft.Text("Section:"))

    def matieres_update(e):
        global matieres
        if (matieres is not(None)):
            for matiere in matieres:
                page.remove(matiere)
                print("-" ,matiere.label," ", matiere)
            else:
                matieres = []
                for matiere in section_matieres[dsc.value]:
                    matiere = ft.Checkbox(label=matiere, value=True)
                    matieres.append(matiere)
                    page.add(matiere)
                    print("+" ,matiere.label," ", matiere)
        page.update()

    dsc = ft.Dropdown(
        options=[ft.dropdown.Option(section) for section in section_matieres.keys()],on_change=matieres_update,
    )
    page.add(dsc)



    page.add(ft.Text("Session:"))
    dss = ft.Dropdown(
        options=[ft.dropdown.Option(session) for session in sessions],
    )
    page.add(dss)

    def slider_changed(e):
        t_ad.value = e.control.value
        aam_range[0]= t_af.value
        page.update()

    t_ad = ft.Text()
    page.add(
        ft.Text("année de début:"),
        ft.Slider(min=1994, max=2030, divisions=(36), label="{value}", on_change=slider_changed), t_ad)

    def slider_changed(e):
        t_af.value = e.control.value
        aam_range[1]= t_af.value
        page.update()

    t_af = ft.Text()
    page.add(
        ft.Text("dernière année:"),
        ft.Slider(min=1994, max=2030, divisions=(36), label="{value}", on_change=slider_changed), t_af)


    page.add(ft.Text("Option:"))
    opt = ft.Dropdown(
        options=[ft.dropdown.Option(opt) for opt in options],
    )
    page.add(opt)


    #matieres


    def DownloadTest():
        print("Click")

    page.add(ft.Text("Matieres:"))

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.DOWNLOAD, label="Download", on_click=DownloadTest),
        ]
    )

ft.app(target=main)




#REQUESTS
def Download():
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
