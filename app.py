import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

import requests
import pdfplumber
from _datetime import datetime
import json
from PIL import Image, ImageTk

HEIGHT = 200  # y
WIDTH = 300  # x

font = "Calibri 12"

config_file = open('config.json')
config = json.load(config_file)

base_url = config['base_url']


class LoginWindow:

    def __init__(self, master):

        self.master = master

        self.master.geometry("+%d+%d" % (400, 20))
        self.master.title("Prijava na sistem")

        self.canvasLogin = tk.Canvas(self.master, height=HEIGHT, width=WIDTH)
        self.canvasLogin.pack()

        self.frame = tk.Frame(self.master, bg="#cce5ff", bd=5)
        self.frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Login forma
        # Polja za username
        self.username_label = tk.Label(self.frame, text="Ime: ", bg="#cce5ff", font=font)
        self.username_label.place(height=30, width=30, x=50, y=40)

        self.username_entry = tk.Entry(self.frame, font=font)
        self.username_entry.place(height=30, width=120, x=90, y=40)

        # Polja za password
        self.password_label = tk.Label(self.frame, text="Šifra: ", bg="#cce5ff", font=font)
        self.password_label.place(height=30, width=40, x=50, y=90)

        self.password_entry = tk.Entry(self.frame, font=font, show="*")
        self.password_entry.place(height=30, width=120, x=90, y=90, )

        self.loginButton = tk.Button(self.frame, text="Prijavi se", padx=30, pady=5, fg="white", bg="#3333ff",
                                     font=font,
                                     command=lambda: self.validate_data())

        self.loginButton.place(height=40, width=100, x=100, y=140)

    def validate_data(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username:
            messagebox.showerror("Greška", "Morate unijeti ime!")
            return False

        if not password:
            messagebox.showerror("Greška", "Morate unijeti šifru !")
            return False

        json_to_send = {
            'username': username,
            'password': password
        }

        self.login(json_to_send)

    def login(self, json_to_send):
        try:

            self.password_entry.delete(0, tk.END)

            endpoint = base_url + "/api/login"
            print('endpoint: ' + endpoint)

            headers_for_request = {'Accept': 'application/json'}

            response = requests.post(endpoint, json=json_to_send, headers=headers_for_request)

            response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xxx

            print("Status code: ", response.status_code)

            data = response.json()
            token = data["token"]
            username = data["name"]
            print(token)
            print(username)

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            messagebox.showerror("Greška", "Konekcija sa serverom nije uspjela!")
        except requests.exceptions.HTTPError:
            messagebox.showerror("Greška", "Ime ili šifra su pogrešni.")
        else:
            messagebox.showinfo("Uspješna prijava", "Dobrodošli " + username)
            self.master.destroy()
            main_window = tk.Tk()
            # otvara klasu gdje se nalazi glavni prozor za dodavanje polisa
            InsuranceCard(main_window, token)


class InsuranceCard:

    def __init__(self, master, token):

        self.master = master
        self.token = token

        master.geometry("+%d+%d" % (500, 20))
        master.title("Polise")

        self.canvas = tk.Canvas(master, height=880, width=790)
        self.canvas.pack()

        self.frame = tk.Frame(master, bg="#cce5ff", bd=5)
        self.frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.openFileButton = tk.Button(self.frame, text="Učitaj polisu", padx=30, pady=5, fg="white", bg="#3333ff",
                                        font=font,
                                        command=lambda: self.load_insurance_card())
        self.openFileButton.place(height=40, width=100, x=10, y=820)

        self.sendToServerButton = tk.Button(self.frame, text="Dodaj u bazu", padx=30, pady=5, fg="white", bg="#3333ff",
                                            font=font,
                                            command=lambda: self.validate_fields())
        self.sendToServerButton.place(height=40, width=100, x=670, y=820)

        # # Creating a photoimage object to use png image
        # self.photo = Image.open("trashh.png")
        #
        # # Putting image on tkinter's object
        # self.photoimage = ImageTk.PhotoImage(self.photo)

        # add argument image=self.photoimage in button below to add icon to button

        self.emptyFields = tk.Button(self.frame, text="#", command=lambda: self.empty_all_fields())
        self.emptyFields.place(height=10, width=10, x=10, y=10)

        # Polja za broj polise
        self.polisa_broj_entry = tk.Entry(self.frame, font=font)
        self.polisa_broj_entry.place(height=25, width=120, x=650, y=10)

        self.polisa_broj_label = tk.Label(self.frame, text="Polisa broj: ", bg="#cce5ff", font=font)
        self.polisa_broj_label.place(height=25, width=100, x=550, y=10)

        # Polja za zamjena
        self.zamjena_entry = tk.Entry(self.frame, font=font)
        self.zamjena_entry.place(height=25, width=120, x=650, y=45)

        self.zamjena_label = tk.Label(self.frame, text="Zamjena: ", bg="#cce5ff", font=font)
        self.zamjena_label.place(height=25, width=100, x=550, y=45)

        # Polja za is.br. polisa
        self.is_br_polise_entry = tk.Entry(self.frame, font=font)
        self.is_br_polise_entry.place(height=25, width=120, x=650, y=80)

        self.is_br_polise_label = tk.Label(self.frame, text="IS br. polisa: ", bg="#cce5ff", font=font)
        self.is_br_polise_label.place(height=25, width=100, x=550, y=80)

        # divider reg oznaka vozila
        divider_reg_oznaka_vozila = tk.Canvas(self.frame, bg="#cce5ff", bd=5, highlightbackground="#3333ff").place(
            height=70,
            width=230,
            x=540,
            y=110)

        # Polja za reg. oznaku vozila
        self.reg_oznaka_vozila_entry = tk.Entry(self.frame, font=font + " bold", justify="center")
        self.reg_oznaka_vozila_entry.place(height=25, width=200, x=555, y=140)

        self.reg_oznaka_vozila_label = tk.Label(self.frame, text="Registarska oznaka vozila: ", bg="#cce5ff", font=font)
        self.reg_oznaka_vozila_label.place(height=20, width=200, x=550, y=115)

        # divider ugovornik
        self.divider_ugovornik = tk.Canvas(self.frame, bg="#cce5ff", bd=5, highlightbackground="white").place(
            height=110,
            width=760, x=10,
            y=185)

        # Label podaci o ugovorniku osiguranja
        self.ugovornik_podaci_label = tk.Label(self.frame, text="Podaci o ugovorniku osiguranja  ", bg="#cce5ff",
                                               font=font + " bold",
                                               anchor="w")
        self.ugovornik_podaci_label.place(height=25, width=250, x=30, y=190)

        # Polja za ugovornika prvi red

        self.ugovornik_ime_naziv_label = tk.Label(self.frame, text="Ime i prezime/naziv", bg="#cce5ff", font=font,
                                                  anchor="w")
        self.ugovornik_ime_naziv_label.place(height=25, width=130, x=30, y=220)

        self.ugovornik_ime_naziv_entry = tk.Entry(self.frame, font=font)
        self.ugovornik_ime_naziv_entry.place(height=25, width=250, x=170, y=220)

        self.ugovornik_jmbg_pib_label = tk.Label(self.frame, text="JMBG/PIB", bg="#cce5ff", font=font, anchor="e")
        self.ugovornik_jmbg_pib_label.place(height=25, width=70, x=460, y=220)

        self.ugovornik_jmbg_pib_entry = tk.Entry(self.frame, font=font)
        self.ugovornik_jmbg_pib_entry.place(height=25, width=210, x=540, y=220)

        # Polja za ugovornika drugi red
        self.ugovornik_grad_label = tk.Label(self.frame, text="Grad", bg="#cce5ff", font=font, anchor="w")
        self.ugovornik_grad_label.place(height=25, width=40, x=30, y=260)

        self.ugovornik_grad_entry = tk.Entry(self.frame, font=font)
        self.ugovornik_grad_entry.place(height=25, width=140, x=75, y=260)

        self.ugovornik_ulica_broj_label = tk.Label(self.frame, text="Ulica i broj", bg="#cce5ff", font=font, anchor="e")
        self.ugovornik_ulica_broj_label.place(height=25, width=80, x=225, y=260)

        self.ugovornik_ulica_broj_entry = tk.Entry(self.frame, font=font)
        self.ugovornik_ulica_broj_entry.place(height=25, width=240, x=310, y=260)

        self.ugovornik_br_tel_label = tk.Label(self.frame, text="Br. tel", bg="#cce5ff", font=font, anchor="e")
        self.ugovornik_br_tel_label.place(height=25, width=50, x=565, y=260)

        self.ugovornik_br_tel_entry = tk.Entry(self.frame, font=font)
        self.ugovornik_br_tel_entry.place(height=25, width=130, x=620, y=260)

        # divider osiguranik
        self.divider_osiguranik = tk.Canvas(self.frame, bg="#cce5ff", bd=5, highlightbackground="white").place(
            height=110,
            width=760,
            x=10, y=300)

        # Label podaci o osiguraniku
        self.osiguranik_podaci_label = tk.Label(self.frame, text="Podaci o osiguraniku  ", bg="#cce5ff",
                                                font=font + " bold",
                                                anchor="w")
        self.osiguranik_podaci_label.place(height=25, width=250, x=30, y=305)

        # Polja za osiguranika prvi red

        self.osiguranik_ime_naziv_label = tk.Label(self.frame, text="Ime i prezime/naziv", bg="#cce5ff", font=font,
                                                   anchor="w")
        self.osiguranik_ime_naziv_label.place(height=25, width=130, x=30, y=330)

        self.osiguranik_ime_naziv_entry = tk.Entry(self.frame, font=font)
        self.osiguranik_ime_naziv_entry.place(height=25, width=250, x=170, y=330)

        self.osiguranik_jmbg_pib_label = tk.Label(self.frame, text="JMBG/PIB", bg="#cce5ff", font=font, anchor="e")
        self.osiguranik_jmbg_pib_label.place(height=25, width=70, x=460, y=330)

        self.osiguranik_jmbg_pib_entry = tk.Entry(self.frame, font=font)
        self.osiguranik_jmbg_pib_entry.place(height=25, width=210, x=540, y=330)

        # Polja za osiguranika drugi red
        self.osiguranik_grad_label = tk.Label(self.frame, text="Grad", bg="#cce5ff", font=font, anchor="w")
        self.osiguranik_grad_label.place(height=25, width=40, x=30, y=370)

        self.osiguranik_grad_entry = tk.Entry(self.frame, font=font)
        self.osiguranik_grad_entry.place(height=25, width=140, x=75, y=370)

        self.osiguranik_ulica_broj_label = tk.Label(self.frame, text="Ulica i broj", bg="#cce5ff", font=font,
                                                    anchor="e")
        self.osiguranik_ulica_broj_label.place(height=25, width=80, x=225, y=370)

        self.osiguranik_ulica_broj_entry = tk.Entry(self.frame, font=font)
        self.osiguranik_ulica_broj_entry.place(height=25, width=240, x=310, y=370)

        self.osiguranik_br_tel_label = tk.Label(self.frame, text="Br. tel", bg="#cce5ff", font=font, anchor="e")
        self.osiguranik_br_tel_label.place(height=25, width=50, x=565, y=370)

        self.osiguranik_br_tel_entry = tk.Entry(self.frame, font=font)
        self.osiguranik_br_tel_entry.place(height=25, width=130, x=620, y=370)

        # divider vozilo
        self.divider_vozilo = tk.Canvas(self.frame, bg="#cce5ff", bd=5, highlightbackground="white").place(height=225,
                                                                                                           width=760,
                                                                                                           x=10,
                                                                                                           y=420)

        # Label podaci o vozilu
        self.vozilo_podaci_label = tk.Label(self.frame, text="Podaci o vozilu ", bg="#cce5ff", font=font + " bold",
                                            anchor="w")
        self.vozilo_podaci_label.place(height=25, width=250, x=30, y=425)

        # polja za vozilo prvi red
        # vrsta
        self.vrsta_label = tk.Label(self.frame, text="Vrsta", bg="#cce5ff", font=font, anchor="w")
        self.vrsta_label.place(height=25, width=40, x=30, y=450)

        self.vrsta_entry = tk.Entry(self.frame, font=font, justify="center")
        self.vrsta_entry.place(height=25, width=330, x=150, y=450)

        # godina proizvodnje
        self.godina_proizvodnje_label = tk.Label(self.frame, text="Godina proizvodnje", bg="#cce5ff", font=font,
                                                 anchor="e")
        self.godina_proizvodnje_label.place(height=25, width=130, x=500, y=450)

        self.godina_proizvodnje_entry = tk.Entry(self.frame, font=font, justify="center")
        self.godina_proizvodnje_entry.place(height=25, width=110, x=640, y=450)

        # polja za vozilo drugi red
        # marka i tip
        self.marka_tip_label = tk.Label(self.frame, text="Marka i tip", bg="#cce5ff", font=font, anchor="w")
        self.marka_tip_label.place(height=25, width=75, x=30, y=490)

        self.marka_tip_entry = tk.Entry(self.frame, font=font, justify="center")
        self.marka_tip_entry.place(height=25, width=330, x=150, y=490)

        # snaga kw
        self.snaga_kw_label = tk.Label(self.frame, text="Snaga KW", bg="#cce5ff", font=font, anchor="e")
        self.snaga_kw_label.place(height=25, width=130, x=500, y=490)

        self.snaga_kw_entry = tk.Entry(self.frame, font=font, justify="center")
        self.snaga_kw_entry.place(height=25, width=110, x=640, y=490)

        # polja za vozilo treci red
        # broj sasije
        self.broj_sasije_label = tk.Label(self.frame, text="Broj šasije", bg="#cce5ff", font=font, anchor="w")
        self.broj_sasije_label.place(height=25, width=80, x=30, y=530)

        self.broj_sasije_entry = tk.Entry(self.frame, font=font, justify="center")
        self.broj_sasije_entry.place(height=25, width=330, x=150, y=530)

        # zapremina ccm
        self.zapremina_ccm_label = tk.Label(self.frame, text="Zapremina ccm", bg="#cce5ff", font=font, anchor="e")
        self.zapremina_ccm_label.place(height=25, width=130, x=500, y=530)

        self.zapremina_ccm_entry = tk.Entry(self.frame, font=font, justify="center")
        self.zapremina_ccm_entry.place(height=25, width=110, x=640, y=530)

        # polja za vozilo cetvrti red
        # broj motora
        self.broj_motora_label = tk.Label(self.frame, text="Broj motora", bg="#cce5ff", font=font, anchor="w")
        self.broj_motora_label.place(height=25, width=80, x=30, y=570)

        self.broj_motora_entry = tk.Entry(self.frame, font=font, justify="center")
        self.broj_motora_entry.place(height=25, width=330, x=150, y=570)

        # broj mjesta
        self.broj_mjesta_label = tk.Label(self.frame, text="Broj mjesta", bg="#cce5ff", font=font, anchor="e")
        self.broj_mjesta_label.place(height=25, width=130, x=500, y=570)

        self.broj_mjesta_entry = tk.Entry(self.frame, font=font, justify="center")
        self.broj_mjesta_entry.place(height=25, width=110, x=640, y=570)

        # polja za vozilo peti red
        # namjena
        self.namjena_label = tk.Label(self.frame, text="Namjena", bg="#cce5ff", font=font, anchor="w")
        self.namjena_label.place(height=25, width=80, x=30, y=610)

        self.namjena_entry = tk.Entry(self.frame, font=font, justify="center")
        self.namjena_entry.place(height=25, width=330, x=150, y=610)

        # nosivost kg
        self.nosivost_kg_label = tk.Label(self.frame, text="Nosivost kg", bg="#cce5ff", font=font, anchor="e")
        self.nosivost_kg_label.place(height=25, width=130, x=500, y=610)

        self.nosivost_kg_entry = tk.Entry(self.frame, font=font, justify="center")
        self.nosivost_kg_entry.place(height=25, width=110, x=640, y=610)

        # divider trajanje
        self.divider_trajanje = tk.Canvas(self.frame, bg="#cce5ff", bd=5, highlightbackground="white").place(height=70,
                                                                                                             width=760,
                                                                                                             x=10,
                                                                                                             y=655)
        # trajanje osiguranja
        self.trajanje_osiguranja_label = tk.Label(self.frame, text="Trajanje osiguranja ", bg="#cce5ff",
                                                  font=font + " bold",
                                                  anchor="w")
        self.trajanje_osiguranja_label.place(height=25, width=150, x=30, y=660)

        # datum od
        self.datum_od_label = tk.Label(self.frame, text="Osiguranje počinje", bg="#cce5ff", font=font, anchor="w")
        self.datum_od_label.place(height=25, width=130, x=30, y=685)

        self.datum_od_entry = tk.Entry(self.frame, font=font, justify="center")
        self.datum_od_entry.place(height=25, width=85, x=160, y=685)

        # vrijeme od
        self.vrijeme_od_label = tk.Label(self.frame, text="godine u", bg="#cce5ff", font=font, anchor="w")
        self.vrijeme_od_label.place(height=25, width=60, x=250, y=685)

        self.vrijeme_od_entry = tk.Entry(self.frame, font=font, justify="center")
        self.vrijeme_od_entry.place(height=25, width=60, x=315, y=685)

        # datum do
        self.datum_do_label = tk.Label(self.frame, text="časova i traje do", bg="#cce5ff", font=font, anchor="w")
        self.datum_do_label.place(height=25, width=120, x=375, y=685)

        self.datum_do_entry = tk.Entry(self.frame, font=font, justify="center")
        self.datum_do_entry.place(height=25, width=100, x=490, y=685)

        # vrijeme od
        self.vrijeme_do_label = tk.Label(self.frame, text="godine u", bg="#cce5ff", font=font, anchor="w")
        self.vrijeme_do_label.place(height=25, width=60, x=590, y=685)

        self.vrijeme_do_entry = tk.Entry(self.frame, font=font, justify="center")
        self.vrijeme_do_entry.place(height=25, width=60, x=655, y=685)

        # casova
        self.vrijeme_do_label = tk.Label(self.frame, text="časova", bg="#cce5ff", font=font, anchor="w")
        self.vrijeme_do_label.place(height=25, width=50, x=710, y=685)

        # divider trajanje
        self.divider_dodatne_informacije = tk.Canvas(self.frame, bg="#cce5ff", bd=5, highlightbackground="white").place(
            height=70,
            width=760,
            x=10,
            y=730)

        # dodatne infomacije
        self.dodatne_informacije_label = tk.Label(self.frame, text="Dodatne informacije ", bg="#cce5ff",
                                                  font=font + " bold",
                                                  anchor="w")
        self.dodatne_informacije_label.place(height=25, width=150, x=30, y=735)

        self.porez_label = tk.Label(self.frame, text="Porez =>", bg="#cce5ff", font=font, anchor="w")
        self.porez_label.place(height=25, width=60, x=30, y=765)

        self.porez_entry = tk.Entry(self.frame, font=font, justify="center")
        self.porez_entry.place(height=25, width=70, x=90, y=765)

        self.za_naplatu_label = tk.Label(self.frame, text="Za naplatu =>", bg="#cce5ff", font=font, anchor="w")
        self.za_naplatu_label.place(height=25, width=100, x=170, y=765)

        self.za_naplatu_entry = tk.Entry(self.frame, font=font, justify="center")
        self.za_naplatu_entry.place(height=25, width=70, x=270, y=765)

        self.sklopljeno_u_label = tk.Label(self.frame, text="Sklopljeno u =>", bg="#cce5ff", font=font, anchor="w")
        self.sklopljeno_u_label.place(height=25, width=105, x=350, y=765)

        self.sklopljeno_u_entry = tk.Entry(self.frame, font=font, justify="center")
        self.sklopljeno_u_entry.place(height=25, width=70, x=460, y=765)

        self.sklopljeno_dana_label = tk.Label(self.frame, text="Sklopljeno dana =>", bg="#cce5ff", font=font,
                                              anchor="w")
        self.sklopljeno_dana_label.place(height=25, width=125, x=540, y=765)

        self.sklopljeno_dana_entry = tk.Entry(self.frame, font=font, justify="center")
        self.sklopljeno_dana_entry.place(height=25, width=80, x=670, y=765)

        master.mainloop()

    def parse_pdf(self, path_to_file):
        pdf = pdfplumber.open(path_to_file)
        page = pdf.pages[0]
        rows = page.extract_words()

        zamjena = ""
        is_br_polisa = ""
        reg_oznaka_vozila = ""

        ugovornik_prvi_red = ""
        ugovornik_drugi_red = ""

        ime_naziv_ugovornik = ""
        jmbg_pib_ugovornik = ""
        grad_ugovornik = ""
        ulica_broj_ugovornik = ""
        br_tel_ugovornik = ""

        osiguranik_prvi_red = ""
        osiguranik_drugi_red = ""

        ime_naziv_osiguranik = ""
        jmbg_pib_osiguranik = ""
        grad_osiguranik = ""
        ulica_broj_osiguranik = ""
        br_tel_osiguranik = ""

        vrsta = ""
        marka_tip = ""
        broj_sasije = ""
        broj_motora = ""
        namjena = ""
        godina_proizvodnje = 0
        snaga_kw = ""
        zapremina_ccm = ""
        broj_mjesta = ""
        nosivost_kg = ""

        datum_i_vrijeme = ""
        datum_od = ""
        datum_do = ""
        vrijeme_od = ""
        vrijeme_do = ""

        porez = ""
        za_naplatu = ""

        sklopljeno_u = ""
        sklopljeno_dana = ""

        for row in rows:

            print(row)

            text = row['text']
            text_str = text
            # if 'cid' in text_str.lower():
            #     text_str = text_str.strip('(')
            #     text_str = text_str.strip(')')
            #     ascii_num = text_str.split(':')[-1]
            #     ascii_num = int(ascii_num)
            #     text = chr(ascii_num)  # 66 = 'B' in ascii

            if 'cid' in text_str.lower():
                text = 'N/A'

            # x0 - lijeva pozicija teksta u PDF-u
            x0 = float(row['x0'])

            # x1 - lijeva pozicija teksta u PDF-u
            x1 = float(row['x1'])

            # top -  gornja pozicija teksta u PDF-u
            top = float(row['top'])

            if 33 < top < 37 and x1 > 450:
                print("zamjena: " + text)
                zamjena = text

            if 53 < top < 56 and x1 > 450:
                print("is_br_polisa: " + text)
                is_br_polisa = text

            if 94 < top < 97:
                print("reg_oznaka_vozila: " + text)
                reg_oznaka_vozila = text

            if 137.544 < top < 140.415:
                ugovornik_prvi_red += text + ' '

            if 157 < top < 162:
                ugovornik_drugi_red += text + ' '

            if 191.02 < top < 194:
                osiguranik_prvi_red += text + ' '

            if 210 < top < 215:
                osiguranik_drugi_red += text + ' '

            if 244 < top < 248 and x1 < 450:
                vrsta += text + ' '

            if 247 < top < 249 and x1 > 450:
                godina_proizvodnje = text

            if 266 < top < 268 and x1 < 450:
                marka_tip += text + ' '

            if 266 < top < 268 and x1 > 450:
                snaga_kw = text

            if 285 < top < 288 and x1 < 450:
                broj_sasije = text

            if 285 < top < 288 and x1 > 450:
                zapremina_ccm = text

            if 303 < top < 306 and x1 < 450:
                broj_motora = text

            if 303 < top < 306 and x1 > 450:
                broj_mjesta = text

            if 321 < top < 324 and x1 < 450:
                namjena += text + ' '

            if 321 < top < 324 and x1 > 450:
                nosivost_kg = text

            if 354 < top < 358:
                datum_i_vrijeme += text + ' '

            if 584 < top < 590 and x1 < 450:
                porez = text

            if 584 < top < 590 and x1 > 450:
                za_naplatu = text

            if 755 < top < 760 and x1 < 300:
                sklopljeno_u = text

            if 755 < top < 760 and x1 < 300:
                sklopljeno_u = text

            if 755 < top < 760 and x1 > 300:
                sklopljeno_dana = text

        pdf.close()

        if not reg_oznaka_vozila:
            messagebox.showerror("Greska", "Došlo je do greške!\nDatoteka koju ste izabrali nije polisa!")

        # parse za ugovornika
        ugovornik_prvi_red_podaci = ugovornik_prvi_red.split(' ')

        duzina_liste = len(ugovornik_prvi_red_podaci)

        jmbg_pib_ugovornik = ugovornik_prvi_red_podaci[duzina_liste - 2]

        i = 0
        for podatak in ugovornik_prvi_red_podaci:
            if i < duzina_liste - 2:
                ime_naziv_ugovornik += podatak + " "
            i += 1

        print("ime_naziv_ugovornik: " + ime_naziv_ugovornik)
        print("jmbg_pib_ugovornik: " + jmbg_pib_ugovornik)

        ugovornik_drugi_red_podaci = ugovornik_drugi_red.split(' ')
        duzina_liste = len(ugovornik_drugi_red_podaci)

        if ugovornik_drugi_red.__contains__('067') or ugovornik_drugi_red.__contains__(
                '068') or ugovornik_drugi_red.__contains__('069'):
            # ima broj telefona

            i = 0
            for podatak in ugovornik_drugi_red_podaci:
                if i == 0:
                    grad_ugovornik = podatak
                elif 0 < i < duzina_liste - 2:
                    ulica_broj_ugovornik += podatak + " "
                else:
                    br_tel_ugovornik += podatak
                i += 1
        else:
            # nema broj telefona
            i = 0
            for podatak in ugovornik_drugi_red_podaci:
                if i == 0:
                    grad_ugovornik = podatak
                else:
                    ulica_broj_ugovornik += podatak + " "
                i += 1

        print("grad_ugovornik: " + grad_ugovornik)
        print("ulica_broj_ugovornik: " + ulica_broj_ugovornik)
        print("br_tel_ugovornik: " + br_tel_ugovornik)

        ##################################################

        # parse za osiguranika

        osiguranik_prvi_red_podaci = osiguranik_prvi_red.split(' ')

        duzina_liste = len(osiguranik_prvi_red_podaci)

        jmbg_pib_osiguranik = osiguranik_prvi_red_podaci[duzina_liste - 2]

        i = 0
        for podatak in osiguranik_prvi_red_podaci:
            if i < duzina_liste - 2:
                ime_naziv_osiguranik += podatak + " "
            i += 1

        print("ime_naziv_osiguranik: " + ime_naziv_osiguranik)
        print("jmbg_pib_osiguranik: " + jmbg_pib_osiguranik)

        osiguranik_drugi_red_podaci = osiguranik_drugi_red.split(' ')
        duzina_liste = len(osiguranik_drugi_red_podaci)

        if osiguranik_drugi_red.__contains__('067') or osiguranik_drugi_red.__contains__(
                '068') or osiguranik_drugi_red.__contains__('069'):
            # ima broj telefona

            i = 0
            for podatak in osiguranik_drugi_red_podaci:
                if i == 0:
                    grad_osiguranik = podatak
                elif 0 < i < duzina_liste - 2:
                    ulica_broj_osiguranik += podatak + " "
                else:
                    br_tel_osiguranik += podatak
                i += 1
        else:
            # nema broj telefona
            i = 0
            for podatak in osiguranik_drugi_red_podaci:
                if i == 0:
                    grad_osiguranik = podatak
                else:
                    ulica_broj_osiguranik += podatak + " "
                i += 1

        print("grad_osiguranik: " + grad_osiguranik)
        print("ulica_broj_osiguranik: " + ulica_broj_osiguranik)
        print("br_tel_osiguranik: " + br_tel_osiguranik)

        ##################################################

        # podaci o vozilu

        print("vrsta:" + vrsta)
        print("marka_tip:" + marka_tip)
        print("godina_proizvodnje: " + godina_proizvodnje)
        print("snaga_kw: " + snaga_kw)
        print("broj_sasije: " + broj_sasije)
        print("zapremina_ccm: " + zapremina_ccm)
        print("broj_motora: " + broj_motora)
        print("broj_mjesta: " + broj_mjesta)
        print("namjena: " + namjena)
        print("nosivost_kg: " + nosivost_kg)

        # datum i vrijeme
        dv = datum_i_vrijeme.rstrip()
        datum_i_vrijeme_niz = dv.split(" ")

        datum_od = datum_i_vrijeme_niz[0]
        vrijeme_od = datum_i_vrijeme_niz[1]
        datum_do = datum_i_vrijeme_niz[2]
        vrijeme_do = datum_i_vrijeme_niz[3]

        date_object_datum_od = datetime.strptime(datum_od, '%d.%m.%Y')
        datum_od = date_object_datum_od.strftime('%Y-%m-%d')

        date_object_datum_do = datetime.strptime(datum_do, '%d.%m.%Y')
        datum_do = date_object_datum_do.strftime('%Y-%m-%d')

        date_object_sklopljeno_dana = datetime.strptime(sklopljeno_dana, '%d.%m.%Y')
        sklopljeno_dana = date_object_sklopljeno_dana.strftime('%Y-%m-%d')

        print("datum_od: " + datum_od)
        print("vrijeme_od: " + vrijeme_od)
        print("datum_do: " + datum_do)
        print("vrijeme_do: " + vrijeme_do)
        print("porez: " + porez)
        print("za_naplatu: " + za_naplatu)
        print("sklopljeno_u: " + sklopljeno_u)
        print("sklopljeno_dana: " + sklopljeno_dana)

        # print("vrsta:" + vrsta.rstrip()) rstrip mice zadnji space iz string-a

        # polisa_broj = input('Unesite broj polise!')

        self.empty_all_fields()

        self.zamjena_entry.insert(0, zamjena)
        self.is_br_polise_entry.insert(0, is_br_polisa)
        self.reg_oznaka_vozila_entry.insert(0, reg_oznaka_vozila)

        self.ugovornik_ime_naziv_entry.insert(0, ime_naziv_ugovornik)
        self.ugovornik_jmbg_pib_entry.insert(0, jmbg_pib_ugovornik)
        self.ugovornik_grad_entry.insert(0, grad_ugovornik)
        self.ugovornik_ulica_broj_entry.insert(0, ulica_broj_ugovornik)
        self.ugovornik_br_tel_entry.insert(0, br_tel_ugovornik)

        self.osiguranik_ime_naziv_entry.insert(0, ime_naziv_osiguranik)
        self.osiguranik_jmbg_pib_entry.insert(0, jmbg_pib_osiguranik)
        self.osiguranik_grad_entry.insert(0, grad_osiguranik)
        self.osiguranik_ulica_broj_entry.insert(0, ulica_broj_osiguranik)
        self.osiguranik_br_tel_entry.insert(0, br_tel_osiguranik)

        self.vrsta_entry.insert(0, vrsta)
        self.marka_tip_entry.insert(0, marka_tip)
        self.broj_sasije_entry.insert(0, broj_sasije)
        self.broj_motora_entry.insert(0, broj_motora)
        self.namjena_entry.insert(0, namjena)
        self.godina_proizvodnje_entry.insert(0, godina_proizvodnje)
        self.snaga_kw_entry.insert(0, snaga_kw)
        self.zapremina_ccm_entry.insert(0, zapremina_ccm)
        self.broj_mjesta_entry.insert(0, broj_mjesta)
        self.nosivost_kg_entry.insert(0, nosivost_kg)

        self.datum_od_entry.insert(0, datum_od)
        self.datum_do_entry.insert(0, datum_do)
        self.vrijeme_od_entry.insert(0, vrijeme_od)
        self.vrijeme_do_entry.insert(0, vrijeme_do)

        self.porez_entry.insert(0, porez)
        self.za_naplatu_entry.insert(0, za_naplatu)
        self.sklopljeno_u_entry.insert(0, sklopljeno_u)
        self.sklopljeno_dana_entry.insert(0, sklopljeno_dana)

    def empty_all_fields(self):

        self.polisa_broj_entry.delete(0, tk.END)
        self.zamjena_entry.delete(0, tk.END)
        self.is_br_polise_entry.delete(0, tk.END)
        self.reg_oznaka_vozila_entry.delete(0, tk.END)

        self.ugovornik_ime_naziv_entry.delete(0, tk.END)
        self.ugovornik_jmbg_pib_entry.delete(0, tk.END)
        self.ugovornik_grad_entry.delete(0, tk.END)
        self.ugovornik_ulica_broj_entry.delete(0, tk.END)
        self.ugovornik_br_tel_entry.delete(0, tk.END)

        self.osiguranik_ime_naziv_entry.delete(0, tk.END)
        self.osiguranik_jmbg_pib_entry.delete(0, tk.END)
        self.osiguranik_grad_entry.delete(0, tk.END)
        self.osiguranik_ulica_broj_entry.delete(0, tk.END)
        self.osiguranik_br_tel_entry.delete(0, tk.END)

        self.vrsta_entry.delete(0, tk.END)
        self.marka_tip_entry.delete(0, tk.END)
        self.broj_sasije_entry.delete(0, tk.END)
        self.broj_motora_entry.delete(0, tk.END)
        self.namjena_entry.delete(0, tk.END)
        self.godina_proizvodnje_entry.delete(0, tk.END)
        self.snaga_kw_entry.delete(0, tk.END)
        self.zapremina_ccm_entry.delete(0, tk.END)
        self.broj_mjesta_entry.delete(0, tk.END)
        self.nosivost_kg_entry.delete(0, tk.END)

        self.datum_od_entry.delete(0, tk.END)
        self.datum_do_entry.delete(0, tk.END)
        self.vrijeme_od_entry.delete(0, tk.END)
        self.vrijeme_do_entry.delete(0, tk.END)

        self.porez_entry.delete(0, tk.END)
        self.za_naplatu_entry.delete(0, tk.END)
        self.sklopljeno_u_entry.delete(0, tk.END)
        self.sklopljeno_dana_entry.delete(0, tk.END)

    def load_insurance_card(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Odaberi polisu za unos",
                                              filetypes=(("pdf fajlovi", "*.pdf"), ("svi fajlovi", "*.*")))
        path = filename

        # ako nije odabran fajl pada exception pa ova provjera to sprecava
        if not path:
            messagebox.showwarning("Upozorenje", "Nista odabrali ni jedan pdf fajl za dodavanje!")
        else:
            self.parse_pdf(path)

    def send_to_server(self, json_to_send):

        try:

            endpoint = base_url + "/api/insuranceCards"

            token = self.token

            headers_for_request = {'Accept': 'application/json', 'Authorization': 'Bearer ' + token}

            response = requests.post(endpoint, json=json_to_send, headers=headers_for_request)

            response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xxx

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            messagebox.showerror("Greška", "Konekcija sa serverom nije uspjela!")
        except requests.exceptions.HTTPError:
            messagebox.showerror("Greška", "Polisa sa ovim brojem već postoji")
        else:
            messagebox.showinfo("Uspješno dodavanje", "Uspješno ste dodali polisu sa brojem " + json_to_send[
                'polisa_broj'] + " \nRegistarska oznaka vozila: " + json_to_send[
                                    'reg_oznaka_vozila'] + "\nOsiguranik: " + json_to_send['ime_naziv_osiguranik'])
            self.empty_all_fields()

    def validate_fields(self):

        polisa_broj = self.polisa_broj_entry.get()

        zamjena = self.zamjena_entry.get()
        is_br_polisa = self.is_br_polise_entry.get()
        reg_oznaka_vozila = self.reg_oznaka_vozila_entry.get()

        ime_naziv_ugovornik = self.ugovornik_ime_naziv_entry.get()
        jmbg_pib_ugovornik = self.ugovornik_jmbg_pib_entry.get()
        grad_ugovornik = self.ugovornik_grad_entry.get()
        ulica_broj_ugovornik = self.ugovornik_ulica_broj_entry.get()
        br_tel_ugovornik = self.ugovornik_br_tel_entry.get()

        ime_naziv_osiguranik = self.osiguranik_ime_naziv_entry.get()
        jmbg_pib_osiguranik = self.osiguranik_jmbg_pib_entry.get()
        grad_osiguranik = self.osiguranik_grad_entry.get()
        ulica_broj_osiguranik = self.osiguranik_ulica_broj_entry.get()
        br_tel_osiguranik = self.osiguranik_br_tel_entry.get()

        vrsta = self.vrsta_entry.get()
        marka_tip = self.marka_tip_entry.get()
        broj_sasije = self.broj_sasije_entry.get()
        broj_motora = self.broj_motora_entry.get()
        namjena = self.namjena_entry.get()
        godina_proizvodnje = self.godina_proizvodnje_entry.get()
        snaga_kw = self.snaga_kw_entry.get()
        zapremina_ccm = self.zapremina_ccm_entry.get()
        broj_mjesta = self.broj_mjesta_entry.get()
        nosivost_kg = self.nosivost_kg_entry.get()

        datum_od = self.datum_od_entry.get()
        datum_do = self.datum_do_entry.get()
        vrijeme_od = self.vrijeme_od_entry.get()
        vrijeme_do = self.vrijeme_do_entry.get()

        porez = self.porez_entry.get()
        za_naplatu = self.za_naplatu_entry.get()
        sklopljeno_u = self.sklopljeno_u_entry.get()
        sklopljeno_dana = self.sklopljeno_dana_entry.get()

        if not polisa_broj:
            messagebox.showerror("Greška", "Morate unijeti broj polise!")
            return False

        if not reg_oznaka_vozila:
            messagebox.showerror("Greška", "Morate unijeti registarsku oznaku vozila!")
            return False

        if not ime_naziv_ugovornik:
            messagebox.showerror("Greška", "Morate unijeti ime/naziv ugovornika!")
            return False

        if not ime_naziv_osiguranik:
            messagebox.showerror("Greška", "Morate unijeti ime/naziv osiguranika!")
            return False

        if not marka_tip:
            messagebox.showerror("Greška", "Morate unijeti marku i tip automobila!")
            return False

        if not broj_sasije:
            messagebox.showerror("Greška", "Morate unijeti broj šasije!")
            return False

        if not datum_od:
            messagebox.showerror("Greška", "Morate unijeti datum početka osiguranja!")
            return False

        if not datum_do:
            messagebox.showerror("Greška", "Morate unijeti datum završetka osiguranja!")
            return False

        if not porez:
            messagebox.showerror("Greška", "Morate unijeti prikupljeni porez!")
            return False

        if not za_naplatu:
            messagebox.showerror("Greška", "Morate unijeti polje Za naplatu !")
            return False

        json_to_send = {
            'polisa_broj': polisa_broj,
            "zamjena": zamjena,
            "is_br_polisa": is_br_polisa,
            "reg_oznaka_vozila": reg_oznaka_vozila,
            "ime_naziv_ugovornik": ime_naziv_ugovornik,
            "jmbg_pib_ugovornik": jmbg_pib_ugovornik,
            "grad_ugovornik": grad_ugovornik,
            "ulica_broj_ugovornik": ulica_broj_ugovornik,
            "br_tel_ugovornik": br_tel_ugovornik,
            "ime_naziv_osiguranik": ime_naziv_osiguranik,
            "jmbg_pib_osiguranik": jmbg_pib_osiguranik,
            "grad_osiguranik": grad_osiguranik,
            "ulica_broj_osiguranik": ulica_broj_osiguranik,
            "br_tel_osiguranik": br_tel_osiguranik,
            "vrsta": vrsta,
            "marka_tip": marka_tip,
            "broj_sasije": broj_sasije,
            "broj_motora": broj_motora,
            "namjena": namjena,
            "godina_proizvodnje": godina_proizvodnje,
            "snaga_kw": snaga_kw,
            "zapremina_ccm": zapremina_ccm,
            "broj_mjesta": broj_mjesta,
            "nosivost_kg": nosivost_kg,
            "datum_od": datum_od,
            "datum_do": datum_do,
            "vrijeme_od": vrijeme_od,
            "vrijeme_do": vrijeme_do,
            "porez": porez,
            "za_naplatu": za_naplatu,
            "sklopljeno_u": sklopljeno_u,
            "sklopljeno_dana": sklopljeno_dana,
        }

        self.send_to_server(json_to_send)


root = tk.Tk()
login_window = LoginWindow(root)
root.mainloop()
