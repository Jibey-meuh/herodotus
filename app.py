import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Projet Hérodote", page_icon="🏛️", layout="centered")

st.title("🏛️ Projet Hérodote")
st.subheader("Le Conseil Perse : L'analyse croisée Ivre / Sobre")
st.write("Soumettez une problématique. Le système s'occupe de tout gratuitement via Groq !")

# Récupération de la clé Groq cachée dans les Secrets
api_key = st.secrets.get("GROQ_API_KEY", "")

problematique = st.text_area("Quelle problématique voulez-vous soumettre au Conseil ?", 
                             value="Comment relancer le commerce de centre-ville face aux géants du e-commerce ?")

if st.button("Déclencher le Conseil"):
    if not api_key:
        st.error("Erreur : La clé API GROQ_API_KEY n'est pas configurée dans les Secrets de Streamlit.")
    elif not problematique:
        st.error("Veuillez écrire une problématique.")
    else:
        with st.spinner("Le vin coule, les esprits s'échauffent... Délibération en cours..."):
            try:
                # Connexion aux serveurs de Groq
                client = OpenAI(
                    base_url="https://api.groq.com/openai/v1",
                    api_key=api_key
                )
                
                # Modèle ultra-rapide et gratuit de Groq
                modele_groq = "llama3-8b-8192"
                
                # ÉTAPE 1 : IVRE
                prompt_creative = f"Tu es le conseiller 'Ivre'. Propose 3 idées ultra-créatives, audacieuses et sans aucun filtre pour résoudre : '{problematique}'."
                reponse_creative = client.chat.completions.create(
                    model=modele_groq, messages=[{"role": "user", "content": prompt_creative}], temperature=1.3
                )
                idees_brutes = reponse_creative.choices[0].message.content
                st.markdown("### 🍷 [1] Les propositions du Conseiller 'Ivre'")
                st.info(idees_brutes)
                
                # ÉTAPE 2 : SOBRE
                prompt_analytique = f"Tu es le conseiller 'Sobre'. Évalue froidement ces propositions pour '{problematique}'. Ne retiens et ne reformule que ce qui est logiquement et concrètement applicable :\n\n{idees_brutes}"
                reponse_analytique = client.chat.completions.create(
                    model=modele_groq, messages=[{"role": "user", "content": prompt_analytique}], temperature=0.1
                )
                decision_finale = reponse_analytique.choices[0].message.content
                st.markdown("### ⚖️ [2] La décision finale du Conseiller 'Sobre'")
                st.success(decision_finale)
                
            except Exception as e:
                st.error(f"Erreur technique : {e}")
