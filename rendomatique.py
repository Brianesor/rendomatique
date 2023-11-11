from flask import Flask, request, render_template
from datetime import datetime
import re

app = Flask(__name__, static_folder='staticFiles')

def print_result(prix_achat, prix_total, pru, dividende_total, rendement_brut, taxe):
    resultat = '<div class="result">'
    resultat += '<table class="calculateur styled-table" cellspacing="0" id="rendementForm">'
    resultat += '<tbody>'
    resultat += '<tr>'
    resultat += '<td></td>'
    resultat += '</tr>'
    resultat += '<tr>'
    resultat += '<td class="lib" id="tdTopLeft">Prix de l\'action : </td>'
    resultat += f'<td class="inp" id="tdTopRight">{prix_achat:.2f} €</td>'
    resultat += '</tr>'
    resultat += '<tr>'
    resultat += '<td class="lib">Prix total : </td>'
    resultat += f'<td class="inp">{prix_total:.2f} €</td>'
    resultat += '</tr>'
    resultat += '<tr>'
    resultat += '<td class="lib">PRU (+ frais) : </td>'
    resultat += f'<td class="inp">{pru:.2f} €</td>'
    resultat += '</tr>'
    resultat += '<tr>'
    resultat += '<td class="lib">Dividende avant taxe : </td>'
    resultat += f'<td class="inp">{dividende_total:.2f} €</td>'
    resultat += '</td>'
    resultat += '</tr>'
    resultat += '<tr>'
    resultat += '<td class="lib">Rendement avant taxe : </td>'
    resultat += f'<td class="inp">{rendement_brut:.2f} %</td>'
    resultat += '</tr>'
    resultat += '<tr>'
    resultat += '<td class="lib">Dividende après taxe : </td>'
    resultat += f'<td class="inp">{taxe[0]:.2f} €</td>'
    resultat += '</tr>'
    resultat += '<tr>'
    resultat += '<td class="lib">Rendement après taxe : </td>'
    resultat += f'<td class="inp">{taxe[1]:.2f} %</td>'
    resultat += '</tr>'
    resultat += '<tr>'
    resultat += '<td class="lib">Remboursement du précompte mobilier : </td>'
    resultat += f'<td class="inp">{taxe[2]:.2f} €</td>'
    resultat += '</tr>'
    resultat += '<tr>'
    resultat += '<td class="lib" id="tdDownLeft">Rendement avec le remboursement du précompte mobilier : </td>'
    resultat += f'<td class="inp" id="tdDownRight">{taxe[3]:.2f} %</td>'
    resultat += '</tr>'
    resultat += '</tbody>'
    resultat += '</table>'
    resultat += '</div>'
    return resultat

def print_result_valeur(formatted_date, prix_achat, nbr_action, benefice, pourcentage_variation, prix_total_augmenter):
    resultat = '<div class="result">'
    resultat += '<table class="tg">\n'
    resultat += '<thead>\n'
    resultat += '<tr>\n'
    resultat += '<th class="tg-0lax">DATE D\'ACHAT</th>\n'
    resultat += '<th class="tg-0lax">DATE</th>\n'
    resultat += '<th class="tg-0lax"></th>\n'
    resultat += '<th class="tg-0lax">PRIX D\'ACHAT</th>\n'
    resultat += '<th class="tg-0lax">QUANTITÉ</th>\n'
    resultat += '<th class="tg-0lax"></th>\n'
    resultat += '<th class="tg-0lax">GAIN TOTAL</th>\n'
    resultat += '<th class="tg-0lax">VALEUR</th>\n'
    resultat += '</tr>\n'
    resultat += '</thead>\n'
    resultat += '<tbody>\n'
    resultat += '<tr>\n'
    resultat += f'<td class="tg-0lax">{formatted_date}</td>\n'
    resultat += f'<td class="tg-0lax"></td>\n'
    resultat += f'<td class="tg-0lax"></td>\n'
    resultat += f'<td class="tg-0lax">{prix_achat:.2f} €</td>\n'
    resultat += f'<td class="tg-0lax">{nbr_action}</td>\n'
    resultat += f'<td data-color="{benefice:.2f}" class="tg-0lax" >{benefice:.2f} €</td>\n'
    resultat += f'<td data-color="{pourcentage_variation:.2f}" class="tg-0lax">{pourcentage_variation:.2f} %</td>\n'
    resultat += f'<td class="tg-0lax">{prix_total_augmenter:.2f} €</td>\n'
    resultat += '</tr>\n'
    resultat += '</tbody>\n'
    resultat += '</table>\n'
    resultat += '<script src="/staticFiles/color_digit.js" type="text/javascript"></script>'
    resultat += "</div>"
    return resultat

def erreur_formulaire_invalide():
    return "Erreur : Données invalides. Assurez-vous de fournir des valeurs numériques valides dans le formulaire."

def erreur_date_invalide():
    return "Erreur : Données invalides. Assurez-vous de fournir des valeurs numériques valides dans le formulaire." #format date invalide

def calcule_taxe(frais, prix_total, dividende_total, rendement_brut):
    if frais == 3 :
        #taxe be
        dividende_after_tax_be = dividende_total - (dividende_total * 30 / 100) 
        
        dividende_net = dividende_after_tax_be

        rendement_net = dividende_after_tax_be / prix_total * 100

        precompte_moblilier = dividende_total * 30 / 100

        rendement_net_precompte_moblilier = rendement_brut

        return dividende_net, rendement_net, precompte_moblilier, rendement_net_precompte_moblilier
        
    elif frais == 6 :
        
        #taxe fr
        dividende_after_tax_fr = dividende_total - (dividende_total * 25 / 100)
        #taxe be
        dividende_after_tax_be = dividende_after_tax_fr - (dividende_after_tax_fr * 30 / 100)
        #taxe belfius
        dividende_after_tax_belfius = dividende_after_tax_be - 3.03 

        dividende_net = dividende_after_tax_belfius

        rendement_net = dividende_after_tax_belfius / prix_total * 100
        rendement_net_precompte_moblilier = rendement_net * 1.30
        
        precompte_moblilier = dividende_after_tax_fr * 30 / 100

        return dividende_net, rendement_net, precompte_moblilier, rendement_net_precompte_moblilier
        
    elif frais == 8 :
        #taxe nl
        dividende_after_tax_nl = dividende_total - (dividende_total * 15 / 100)
        #taxe be
        dividende_after_tax_be = dividende_after_tax_nl - (dividende_after_tax_nl * 30 / 100)
        #taxe belfius
        dividende_after_tax_belfius = dividende_after_tax_be - 3.03

        dividende_net = dividende_after_tax_belfius

        rendement_net = dividende_after_tax_belfius / prix_total * 100
        rendement_net_precompte_moblilier = rendement_net * 1.30
        
        precompte_moblilier = dividende_after_tax_nl * 30 / 100

        return dividende_net, rendement_net, precompte_moblilier, rendement_net_precompte_moblilier

    elif frais == 15 :
        #taxe us
        dividende_after_tax_us = dividende_total - (dividende_total * 15 / 100)
        #taxe be
        dividende_after_tax_be = dividende_after_tax_us - (dividende_after_tax_us * 30 / 100)
        #taxe belfius
        dividende_after_tax_belfius = dividende_after_tax_be - 3.03

        dividende_net = dividende_after_tax_belfius

        rendement_net = dividende_after_tax_belfius / prix_total * 100
        rendement_net_precompte_moblilier = rendement_net * 1.30
        
        precompte_moblilier = dividende_after_tax_us * 30 / 100

        return dividende_net, rendement_net, precompte_moblilier, rendement_net_precompte_moblilier


def calcule_prix(prix_achat, nbr_action, frais_reel):
    prix_total = prix_achat * nbr_action + frais_reel
    return prix_total

def calcule_pru(prix_total, nbr_action):
    pru = prix_total / nbr_action
    return pru

def calcule_dividende_total(dividende, nbr_action):
    dividende_total = dividende * nbr_action
    return dividende_total

def calcule_rendement_brut(dividende_total, prix_total):
    rendement_brut = dividende_total / prix_total * 100
    return rendement_brut

def calcule_prix_achat(prix_total, frais_reel, nbr_action):
    prix_total = (prix_total - frais_reel) / nbr_action
    return prix_total

def calcule_frais_reel(frais):
    if frais == 3 :
        return 3.60
    if frais == 6 :
        return 6.60
    if frais == 8 :
        return 6.60
    if frais == 15 :
        return 15

def date_valide(date):
    if re.match(r'^\d{4}-\d{2}-\d{2}$', date): 
        return True # Le format de date est valide
    else:
        return False # Le format de date n'est pas valide

def calcule_pourcentage_variation(prix_achat, prix_action):
    pourcentage_variation = 100 * (prix_action - prix_achat) / prix_achat
    return pourcentage_variation
def calcule_benefice(prix_total, pourcentage_variation):
    benefice = prix_total * pourcentage_variation / 100
    return benefice

def calcule_augmentation(prix_total, pourcentage_variation):
    prix_total_augmenter = prix_total * (1 + pourcentage_variation / 100)
    return prix_total_augmenter

def change_date_format(date_str, input_format, output_format):
    # Parse the input date string using the input format
    date_object = datetime.strptime(date_str, input_format)

    # Format the date object using the desired output format
    formatted_date = date_object.strftime(output_format)

    return formatted_date

@app.route('/')
def index():
    return render_template("calcule_action.html")

@app.route('/calcule_action')
def calcule_action():
    return render_template("calcule_action.html")

@app.route('/calcule_action_totale')
def calcule_total():
    return render_template("calcule_action_total.html")

@app.route('/calcule_valeur')
def calcule_valeur():
    return render_template("/calcule_valeur.html")

@app.route('/calcule_rendement', methods=['GET', 'POST'])
def reception_donner_action():
    if request.method == 'POST':
        try:  
            # Essayez de convertir les données en types souhaités
            prix_achat = float(request.form['prixAchat'])
            nbr_action = int(request.form['nombreActions'])
            dividende = float(request.form['dividendes'])
            frais = int(request.form['frais'])

            frais_reel = calcule_frais_reel(frais)

            prix_total = calcule_prix(prix_achat, nbr_action, frais_reel)

            pru = calcule_pru(prix_total, nbr_action)

            dividende_total = calcule_dividende_total(dividende, nbr_action)

            rendement_brut = calcule_rendement_brut(dividende_total, prix_total)

            taxe = calcule_taxe(frais, prix_total, dividende_total, rendement_brut)

            resultat = print_result(prix_achat, prix_total, pru, dividende_total, rendement_brut, taxe)
            return resultat
        except (ValueError, KeyError):
            # En cas d'erreur de conversion de type ou de clé manquante
            return erreur_formulaire_invalide()
    return render_template("calcule_action.html")

@app.route('/calcule_rendement_totale', methods=['GET', 'POST'])
def reception_donner_totale():
    if request.method == 'POST':
        try:
            # Récupérer les données du formulaire
            prix_total = float(request.form['prixTotal'])
            nbr_action = int(request.form['nombreActions'])
            dividende = float(request.form['dividendes'])
            frais = int(request.form['frais'])

            frais_reel = calcule_frais_reel(frais)

            prix_achat = calcule_prix_achat(prix_total, frais_reel, nbr_action)

            pru = calcule_pru(prix_total, nbr_action)

            dividende_total = calcule_dividende_total(dividende, nbr_action)

            rendement_brut = calcule_rendement_brut(dividende_total, prix_total)

            taxe = calcule_taxe(frais, prix_total, dividende_total, rendement_brut)

            resultat = print_result(prix_achat, prix_total, pru, dividende_total, rendement_brut, taxe)
            return resultat

        except (ValueError, KeyError):
            # En cas d'erreur de conversion de type ou de clé manquante
            return erreur_formulaire_invalide()
    return render_template("calcule_action_totale.html") 

@app.route('/calcule_valeur', methods=['GET', 'POST'])
def reception_donner_valeur():
    if request.method == 'POST':
        try:  
            # Essayez de convertir les données en types souhaités
            prix_achat = float(request.form['prixAchat'])
            nbr_action = int(request.form['nombreActions'])
            date = str(request.form['date'])
            prix_action = float(request.form['prixAction'])
            frais_reel = 0 # 0 car les frais sont deja ajouter dans le prix d'achat
            input_format = "%Y-%m-%d"
            output_format = "%d %B %Y"

            is_date_valide = date_valide(date)
            if is_date_valide == False :
                return erreur_date_invalide()

            pourcentage_variation = calcule_pourcentage_variation(prix_achat, prix_action)

            prix_total = calcule_prix(prix_achat, nbr_action, frais_reel)

            benefice = calcule_benefice(prix_total, pourcentage_variation)

            prix_total_augmenter = calcule_augmentation(prix_total, pourcentage_variation)

            formatted_date = change_date_format(date, input_format, output_format)

            resultat = print_result_valeur(formatted_date, prix_achat, nbr_action, benefice, pourcentage_variation, prix_total_augmenter)
            return resultat
        except (ValueError, KeyError):
            # En cas d'erreur de conversion de type ou de clé manquante
            return erreur_formulaire_invalide()
    return render_template("calcule_action.html") 

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)