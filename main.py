
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

    #REQUESTS
    def Download(e):
        #Example: Year:2022, sessions:principale, Section:math, Matiere (Subject):math 
        #href="http://www.bacweb.tn/bac/2022/principale/math/math.pdf"
        print(section, matieres,aam_range)
        matiere=[]
        sessions=[]
        for mat in matieres:
            if mat.value:
                matiere.append(mat.label)
                print(opt,opt.value)
        if opt.value != None:
            matiere.append(opt.value)
        print(matiere)
        for s in SessionP,SessionC:
            if s.value != None:
                sessions.append(s.label)
        print(sessions)
        print(aam_range)

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
                    for sess in (sessions): #Loop through the sessions
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



    page.add(ft.Text("Section:"))
    def DownloadTest(e):
        print(section, matieres,aam_range)
        matiere=[]
        sessions=[]
        for mat in matieres:
            if mat.value:
                matiere.append(mat.label)
                print(opt,opt.value)
        if opt.value != None:
            matiere.append(opt.value)
        print(matiere)
        for s in SessionP,SessionC:
            if s.value != None:
                sessions.append(s.label)
        print(sessions)
        print(aam_range)

    
    download_button = ft.ElevatedButton("Download",icon="DOWNLOAD",on_click=Download,visible=False)
    page.add(download_button)




    #MATIERES DU SECTION
    def matieres_update(e):
        global matieres
        global section 
        section = dsc.value
        page.remove(download_button)
        if (matieres is not(None)):
            
            for matiere in matieres:
                page.remove(matiere)
                print("-" ,matiere.label," ", matiere)
                
            else:
                matieres = []
                for matiere in section_matieres[dsc.value]:
                    matiere = ft.Checkbox(label=matiere, value=True)
                    page.add(matiere)    
                    matieres.append(matiere)
                    print("+" ,matiere.label," ", matiere)
                page.add(download_button)
                download_button.visible = True

        page.update()

    dsc = ft.Dropdown(
        options=[ft.dropdown.Option(section) for section in section_matieres.keys()],on_change=matieres_update,
    )
    page.add(dsc)
    


    #sessions
    page.add(ft.Text("sessions:"))
    global SessionP,SessionC
    SessionP,SessionC = ft.Checkbox(label="Principale", value=True),ft.Checkbox(label="Controle", value=True)
    page.add(SessionP,SessionC)

    def slider_changed(e):
        t_ad.value = e.control.value
        aam_range[0]= int(t_af.value)
        page.update()

    t_ad = ft.Text()
    page.add(
        ft.Text("année de début:"),
        ft.Slider(min=1994, max=2030, divisions=(36), label="{value}", on_change=slider_changed), t_ad)

    def slider_changed(e):
        t_af.value = e.control.value
        aam_range[1]= int(t_af.value)
        page.update()

    t_af = ft.Text()
    page.add(
        ft.Text("dernière année:"),
        ft.Slider(min=1994, max=2030, divisions=(36), label="{value}", on_change=slider_changed), t_af)


    page.add(ft.Text("Option:"))

    global opt 
    opt = ft.Dropdown(
        options=[ft.dropdown.Option(opt) for opt in options])
    page.add(opt)


    #matieres





    page.add(ft.Text("Matieres:"))


ft.app(target=main)




