import os
import time
import flet as ft
import requests

matieres_fix = "math", "philo", "francais", "arabe", "anglais"
section_matieres = {
    "math": ["info", "svt", "physique", *matieres_fix],
    "sciences_ex": ["info", "svt", "physique", *matieres_fix],
    "economie_gestion": ["economie", "gestion", "his_geo", "info", *matieres_fix],
    "technique": ["technique", "info", "physique", *matieres_fix],
    "lettre": ["pensee", "his_geo", "info", "svt", *matieres_fix],
    "sport": ["sport", "info", "svt", "physique", *matieres_fix],
    "informatique": ["bd", "algorithme", "physique", *matieres_fix],
}
matieres_in = []
options = (
    "theatre",
    "artistique",
    "musique",
    "italien",
    "portugais",
    "turque",
    "chinois",
    "russe",
    "espagnol",
    "allemand",
)
year_range = [2020, 2023]  # Year Range


def create_folder(*t):
    global dir_path
    dir_path = os.path.join(os.getcwd(), *t)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path, 0o777)


# GUI with FLET
def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.window_height = 700
    page.window_width = 500
    page.title = "Msabb l BAC"
    page.scroll = True

    # Download
    def Download(e):
        # Example: Year:2022, sessions:principale, Section:math, Matiere (Subject):math
        # http://www.bacweb.tn/bac/2022/principale/math/math.pdf

        # Matieres
        matieres = [
            mat.label if not correction_in.value else [
                mat.label, f"{mat.label}_c"]
            for mat in matieres_in
            if mat.value
        ]  # "matiere"; "matiere","matiere_c" if correction_in
        matieres = (
            [element for sublist in matieres for element in sublist]
            if correction_in.value
            else matieres
        )  # Unravel if correction_in
        # Option
        if option_in.value:
            matieres.append(option_in.value)

        # Sessions
        sessions = [
            (session_in.label).lower()
            for session_in in (session_princiaple_in, session_controle_in)
            if session_in.value
        ]

        # Create a Folder named MSABB
        create_folder("MSABB")
        progress_counter = 0
        ts = 0
        progress_bar_column.visible = True
        start_time = time.time()
        iter_number = (
            len(section)
            * len(matieres)
            * (year_range[1] - year_range[0])
            * len(sessions)
        )
        for sect in section:  # Create a Folder of the Section
            create_folder("MSABB",f"BAC {sect}")
            for mat in matieres:  # Create a Folder of the "Matiere" inside the Section
                create_folder("MSABB",f"BAC {sect}",f"{mat}")
                # Loop through the years (year).
                for year in range(*year_range):
                    for sess in sessions:  # Loop through the sessions
                        success = False
                        # matieres communs : sections communs, default: math
                        # philo,arabe: technique, math, science, eco, info.
                        # francais,anglais: math, science, eco, info.
                        # info: technique, math, science.
                        # option: all.
                        url = (
                            f"http://www.bacweb.tn/bac/{str(year)}/{sess}/math/{mat}.pdf"
                            if (
                                mat in ["philo", "arabe"]
                                and sect
                                in [
                                    "technique",
                                    "economie_gestion",
                                    "sciences_ex",
                                    "informatique",
                                ]
                            )
                            or (
                                mat in ["francais", "anglais"]
                                and sect
                                in ["economie_gestion", "sciences_ex", "informatique"]
                            )
                            or (mat == "info" and sect in ["technique", "sciences_ex"])
                            or (mat == option_in.value)
                            else f"http://www.bacweb.tn/bac/{str(year)}/{sess}/{sect}/{mat}.pdf"
                        )
                        progress_text.value = f"Downloading: {url}"
                        page.update()

                        response = requests.get(url)
                        if response.status_code == 200:  # Success
                            success = True
                            with open(
                                os.path.join(
                                    dir_path,
                                    f"{mat.upper()}-{year}-{sess[0].upper()}.pdf",
                                ),
                                "wb",
                            ) as pdf:  # Create the pdf.
                                for block in response.iter_content(chunk_size=1024):
                                    pdf.write(block)
                            progress_text.value = f"Downloaded: {url}"
                            ts += 1
                        if not (success):  # Fail
                            progress_text.value = f"Doesnt exist: {url}"

                        progress_counter += 1
                        progress_bar.value = progress_counter / iter_number
                        page.update()

        end_time = time.time()
        progress_text.value = (
            f"Downloaded {ts} files in {int(end_time-start_time)} seconds."
        )
        page.update()

    # Section
    page.add(ft.Text("Section:"))

    # Download Button
    download_button = ft.ElevatedButton(
        "Download", icon="DOWNLOAD", on_click=Download, visible=False
    )
    page.add(download_button)

    # Matieres du section
    def matieres_update(e):
        global matieres_in
        global section
        section = [section_in.value]
        page.remove(download_button)
        if matieres_in is not (None):
            for matiere_in in matieres_in:
                page.remove(matiere_in)
            else:
                matieres_in = []
                for matiere in section_matieres[section_in.value]:
                    matiere = ft.Checkbox(label=matiere, value=True)
                    page.add(matiere)
                    matieres_in.append(matiere)
                page.add(download_button)
                download_button.visible = True

        page.update()

    section_in = ft.Dropdown(
        options=[ft.dropdown.Option(section) for section in section_matieres],
        on_change=matieres_update,
    )
    page.add(section_in)

    # SESSIONS
    global session_princiaple_in, session_controle_in
    session_princiaple_in, session_controle_in = ft.Checkbox(
        label="Principale", value=True
    ), ft.Checkbox(label="Controle", value=True)
    page.add(ft.Text("Sessions:"), session_princiaple_in, session_controle_in)

    # CORRECTION
    global correction_in
    correction_in = ft.Switch(label="Correction", value=True)
    page.add(ft.Text("Correction:"), correction_in)

    # Year Range
    def slider_changedMin(e):
        year_min_in.value = e.control.value
        year_range[0] = int(year_min_in.value)
        page.update()

    year_min_in = ft.Text()
    page.add(
        ft.Text("De l'année:"),
        ft.Slider(
            min=2009,
            max=2030,
            divisions=(21),
            label="{value}",
            on_change=slider_changedMin,
        ),
        year_min_in,
    )

    def slider_changedMax(e):
        year_max_in.value = e.control.value
        year_range[1] = int(year_max_in.value) + 1
        page.update()

    year_max_in = ft.Text()
    page.add(
        ft.Text("A l'année:"),
        ft.Slider(
            min=2009,
            max=2030,
            divisions=(21),
            label="{value}",
            on_change=slider_changedMax,
        ),
        year_max_in,
    )

    # OPTION
    page.add(ft.Text("Option:"))
    global option_in
    option_in = ft.Dropdown(
        options=[ft.dropdown.Option(option) for option in options])
    page.add(option_in)

    # MATIERES
    page.add(ft.Text("Matieres:"))
    global progress_bar
    global progress_text
    progress_text = ft.Text()
    progress_bar = ft.ProgressBar()
    progress_bar_column = ft.Column(
        [progress_text, progress_bar], visible=False)
    page.add(progress_bar_column)


ft.app(target=main)
