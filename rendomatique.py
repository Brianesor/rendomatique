from flask import Flask, request, render_template

app = Flask(__name__, static_folder='staticFiles')

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

@app.route('/')
def index():
    return render_template("calcule_action.html")

@app.route('/calcule_action')
def calcule_action():
    return render_template("calcule_action.html")

@app.route('/calcule_action_totale')
def calcule_total():
    return render_template("calcule_action_total.html")

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

            resultat = '<div class="result">'
            resultat += f"<p><p>Prix de l'action :  {prix_achat:.2f}€</p>\n"
            resultat += f"<p>Prix total : {prix_total:.2f}€</p>\n"
            resultat += f"<p>PRU (+ frais) : {pru:.2f}€</p>"
            resultat += f"<p>Dividende avant taxe : {dividende_total:.2f}€</p>\n"
            resultat += f"<p>Rendement avant taxe : {rendement_brut:.2f}%</p>\n"
            resultat += f"<p>Dividende après taxe : {taxe[0]:.2f}€</p>\n"
            resultat += f"<p>Rendement après taxe : {taxe[1]:.2f}%</p>\n"
            resultat += f"<p>Remboursement du précompte mobilier : {taxe[2]:.2f}€</p>\n"
            resultat += f"<p>Rendement avec le remboursement du précompte mobilier : {taxe[3]:.2f}%</p>\n"
            resultat += "</div>"
            return resultat
        except (ValueError, KeyError):
            # En cas d'erreur de conversion de type ou de clé manquante
            return "Erreur : Données invalides. Assurez-vous de fournir des valeurs numériques valides dans le formulaire."
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

            resultat = '<div class="result">'
            resultat += f"<p>Prix de l'action (estimation):  {prix_achat:.2f}€</p>\n"
            resultat += f"<p>Prix total : {prix_total:.2f}€</p>\n"
            resultat += f"<p>PRU (+ frais) : {pru:.2f}€</p>"
            resultat += f"<p>Dividende avant taxe : {dividende_total:.2f}€</p>\n"
            resultat += f"<p>Rendement avant taxe : {rendement_brut:.2f}%</p>\n"
            resultat += f"<p>Dividende après taxe : {taxe[0]:.2f}€</p>\n"
            resultat += f"<p>Rendement après taxe : {taxe[1]:.2f}%</p>\n"
            resultat += f"<p>Remboursement du précompte mobilier : {taxe[2]:.2f}€</p>\n"
            resultat += f"<p>Rendement avec le remboursement du précompte mobilier : {taxe[3]:.2f}%</p>\n"
            resultat += "</div>"
            return resultat

        except (ValueError, KeyError):
            # En cas d'erreur de conversion de type ou de clé manquante
            return "Erreur : Données invalides. Assurez-vous de fournir des valeurs numériques valides dans le formulaire."
    return render_template("calcule_action_totale.html")  

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)