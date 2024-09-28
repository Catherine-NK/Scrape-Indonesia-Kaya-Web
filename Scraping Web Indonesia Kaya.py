from bs4 import BeautifulSoup
import requests
import csv

base_url = "https://indonesiakaya.com/tokoh-indonesia-category/tokoh/page/{}/"
page_number = 1 

with open("Tokoh Indonesia.csv", "w", newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["NAMA TOKOH", "DESKRIPSI", "PROFESI", "TAGAR"])

    while True:
        current_page = base_url.format(page_number)
        print(f"Scraping halaman: {current_page}")
        page_to_scrape = requests.get(current_page)
        soup = BeautifulSoup(page_to_scrape.text, "html.parser")

        data_tokoh = soup.findAll("h4", attrs={"class": "font2"})
        data_profesi = soup.findAll("span", attrs={"class": "mt-3 d-block"})
 
        if not data_tokoh:
            print("Tidak ada data tokoh lagi, selesai.")
            break

        for tokoh, profesi in zip(data_tokoh, data_profesi):
            judul = tokoh.text.split(": ")

            if len(judul) == 2:
                nama_tokoh = judul[0].strip()
                deskripsi = judul[1].strip()
            else:
                nama_tokoh = judul[0].strip() if judul else "-"
                deskripsi = "-"

            profesi_tokoh = profesi.text.strip() if profesi else "-"

            #Scrape halaman detail_tokoh untuk tagar
            link_element = tokoh.find_parent("a", href=True)
            if link_element:
                link_detail_tokoh = link_element["href"]

                detail_page = requests.get(link_detail_tokoh)
                detail_soup = BeautifulSoup(detail_page.text, "html.parser")

                tagar_elemen = detail_soup.find("div", attrs={"style": "color: #277633  !important;"})
                
                if tagar_elemen:
                    tagar_tokoh = ", ".join([tag.text for tag in tagar_elemen.find_all("a")])
                else:
                    tagar_tokoh = "-"
            else:
                tagar_tokoh = "-"

            writer.writerow([nama_tokoh, deskripsi, profesi_tokoh, tagar_tokoh])

        page_number += 1