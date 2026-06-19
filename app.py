import streamlit as st
from openai import OpenAI

# Configuration de la page
st.set_page_config(page_title="Projet Hérodote", page_icon="🏛️", layout="centered")

# En-tête personnalisé (Correction apportée ici)
st.markdown("""
    <div style="text-align: center; padding: 10px; border-bottom: 2px solid #b58d3d; margin-bottom: 20px;">
        <h1 style="color: #b58d3d; margin-bottom: 0;">🏛️ Projet Hérodote</h1>
        <p style="font-style: italic; color: #666;">Le Conseil Perse : L'analyse croisée Ivre / Sobre</p>
    </div>
""", unsafe_allow_html=True)

st.write("Soumettez une problématique. Réglez le niveau d'altération du conseiller Ivre, puis observez le filtre du conseiller Sobre.")

# Récupération de la clé Groq cachée dans les Secrets
api_key = st.secrets.get("GROQ_API_KEY", "")

# Nouvelle Option : Curseur de réglage de l'absurdité / créativité
st.sidebar.header("Réglages du Conseil")
niveau_ivresse = st.sidebar.select_slider(
    "Niveau d'altération du Conseiller Ivre :",
    options=["Sobre (0.2)", "Légère ivresse (0.7)", "Esprit joyeux (1.1)", "Complètement ivre (1.5)", "Extase mystique (2.0)"],
    value="Complètement ivre (1.5)"
)

# Correspondance entre le texte du curseur et la valeur numérique de la Température du LLM
dictionnaire_temperature = {
    "Sobre (0.2)": 0.2,
    "Légère ivresse (0.7)": 0.7,
    "Esprit joyeux (1.1)": 1.1,
    "Complètement ivre (1.5)": 1.5,
    "Extase mystique (2.0)": 1.95  # 2.0 est parfois instable sur certains LLM, 1.95 assure la folie sans planter
}
temperature_ivre = dictionnaire_temperature[niveau_ivresse]

# Zone d'écriture de la problématique
problematique = st.text_area("Quelle problématique voulez-vous soumettre au Conseil ?", 
                             value="Comment relancer le commerce de centre-ville face aux géants du e-commerce ?")

if st.button("Déclencher la délibération"):
    if not api_key:
        st.error("Erreur : La clé API GROQ_API_KEY n'est pas configurée dans les Secrets de Streamlit.")
    elif not problematique:
        st.error("Veuillez écrire une problématique.")
    else:
        with st.spinner("Le vin coule, les esprits s'échauffent... Délibération en cours..."):
            try:
                # Connexion à Groq
                client = OpenAI(
                    base_url="https://api.groq.com/openai/v1",
                    api_key=api_key
                )
                
                # Modèle stable et ultra-rapide sur Groq
                modele_groq = "llama-3.1-8b-instant"
                
                # ÉTAPE 1 : CONSEILLER IVRE (Température dynamique réglée par l'utilisateur)
                prompt_creative = (
                    f"Tu es le conseiller 'Ivre'. Ton niveau d'ébriété est calé sur la valeur {temperature_ivre}. "
                    f"Propose 3 idées ultra-créatives, spontanées, libres de tout filtre et potentiellement "
                    f"complètement folles ou disruptives pour résoudre : '{problematique}'."
                )
                
                reponse_creative = client.chat.completions.create(
                    model=modele_groq, 
                    messages=[{"role": "user", "content": prompt_creative}], 
                    temperature=temperature_ivre
                )
                idees_brutes = reponse_creative.choices[0].message.content
                
                st.markdown(f"### 🍷 [1] Propositions du Conseiller Ivre ({niveau_ivresse})")
                st.info(idees_brutes)
                
                # ÉTAPE 2 : CONSEILLER SOBRE (Température bloquée très basse pour la rigueur)
                prompt_analytique = (
                    f"Tu es le conseiller 'Sobre'. Évalue froidement et logiquement les propositions "
                    f"suivantes formulées pour résoudre '{problematique}'. Écarte ce qui est techniquement "
                    f"impossible, mais garde l'étincelle d'originalité s'il y en a une. "
                    f"Synthétise une décision finale réaliste et applicable :\n\n{idees_brutes}"
                )
                
                reponse_analytique = client.chat.completions.create(
                    model=modele_groq, 
                    messages=[{"role": "user", "content": prompt_analytique}], 
                    temperature=0.1
                )
                decision_finale = reponse_analytique.choices[0].message.content
                
                st.markdown("### ⚖️ [2] Décision finale du Conseiller Sobre")
                st.success(decision_finale)
                
            except Exception as e:
                st.error(f"Erreur technique : {e}")
