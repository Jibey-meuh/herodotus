import streamlit as st
from openai import OpenAI

# 1. Configuration esthétique de la page web
st.set_page_config(
    page_title="Projet Hérodote",
    page_icon="🏛️",
    layout="centered"
)

# Design de l'en-tête thématique
st.markdown("""
    <div style="text-align: center; padding: 10px; border-bottom: 2px solid #b58d3d; margin-bottom: 20px;">
        <h1 style="color: #b58d3d; font-family: 'Georgia', serif; margin-bottom: 5px;">🏛️ Projet Hérodote</h1>
        <h3 style="color: #3e3e3e; font-style: italic; font-weight: normal; margin-top: 0;">Le Conseil Antique : L'analyse croisée Ivre / Sobre</h3>
    </div>
""", unsafe_style=True)

st.write(
    "Soumettez une problématique. Le conseiller **Ivre** va explorer des pistes de réflexion "
    "sans aucun filtre social, puis le conseiller **Sobre** viendra y appliquer une logique "
    "froide et rationnelle pour en extraire des plans d'action applicables."
)

# 2. Configuration dans la barre latérale
st.sidebar.markdown("### ⚙️ Paramètres du Conseil")

# Récupération de la clé Groq cachée dans les Secrets
api_key = st.secrets.get("GROQ_API_KEY", "")

# Nouvelle fonctionnalité : Curseur d'absurdité (Température)
options_absurdite = {
    "🍷 Un verre (Créatif mais sage)": 0.8,
    "🍶 Quelques calices (Idées osées)": 1.1,
    "🍾 Grand Banquet (Franchement éméché)": 1.4,
    "🥴 Délire d'Hérodote (Absurdité totale)": 1.7,
    "🌀 Extase mystique (Chaos créatif)": 1.99
}

choix_absurdite = st.sidebar.select_slider(
    "Niveau d'absurdité du conseiller Ivre :",
    options=list(options_absurdite.keys()),
    value="🍾 Grand Banquet (Franchement éméché)"
)

# Conversion du choix en valeur numérique de température
temperature_drunk = options_absurdite[choix_absurdite]

st.sidebar.markdown("---")
st.sidebar.caption("Propulsé par Groq & Llama 3.1 8B ⚡")

# 3. Zone de saisie principale
problematique = st.text_area(
    "Quelle problématique voulez-vous soumettre aux deux états de conscience ?", 
    value="Comment relancer le commerce de centre-ville face aux géants du e-commerce ?"
)

if st.button("🔥 Déclencher le Conseil Antique"):
    if not api_key:
        st.error("Erreur : La clé API GROQ_API_KEY n'est pas configurée dans les Secrets de Streamlit.")
    elif not problematique:
        st.error("Veuillez formuler une problématique.")
    else:
        # Spinner d'attente immersif
        with st.spinner("Le vin coule, les esprits s'échauffent... Délibération en cours..."):
            try:
                # Connexion à l'API Groq (compatible format OpenAI)
                client = OpenAI(
                    base_url="https://api.groq.com/openai/v1",
                    api_key=api_key
                )
                
                # Modèle stable et rapide de Groq
                modele_groq = "llama-3.1-8b-instant"
                
                # ÉTAPE 1 : LE CONSEILLER IVRE (Température ajustable)
                prompt_creative = (
                    f"Tu es le conseiller 'Ivre' de l'Antiquité. Ton esprit est totalement "
                    f"désinhibé par le vin. Propose 3 idées extrêmement audacieuses, étranges, "
                    f"parfois absurdes, disruptives et sans aucun filtre pour résoudre : '{problematique}'."
                )
                
                reponse_creative = client.chat.completions.create(
                    model=modele_groq,
                    messages=[{"role": "user", "content": prompt_creative}],
                    temperature=temperature_drunk  # On applique la température choisie !
                )
                idees_brutes = reponse_creative.choices[0].message.content
                
                # Affichage des idées folles
                st.markdown("### 🍷 [1] Les propositions du Conseiller 'Ivre'")
                st.info(idees_brutes)
                
                # ÉTAPE 2 : LE CONSEILLER SOBRE (Température ultra-basse et logique)
                prompt_analytique = (
                    f"Tu es le conseiller 'Sobre' de l'Antiquité. Ton esprit est d'une logique "
                    f"froide, implacable et pragmatique. Voici des propositions formulées sous emprise "
                    f"de l'alcool pour résoudre : '{problematique}'.\n\n"
                    f"Idées proposées :\n{idees_brutes}\n\n"
                    f"Évalue rigoureusement ces pistes de manière pragmatique. Élimine ce qui est irréaliste, "
                    f"et ne retiens et ne reformule que ce qui survit à ton examen logique sous la forme "
                    f"d'un plan concret et applicable."
                )
                
                reponse_analytique = client.chat.completions.create(
                    model=modele_groq,
                    messages=[{"role": "user", "content": prompt_analytique}],
                    temperature=0.15  # Gardé très bas pour une logique pure
                )
                decision_finale = reponse_analytique.choices[0].message.content
                
                # Affichage de la synthèse logique
                st.markdown("### ⚖️ [2] La décision finale du Conseiller 'Sobre'")
                st.success(decision_finale)
                
            except Exception as e:
                st.error(f"Erreur technique de l'API : {e}")
