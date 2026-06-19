import streamlit as st
from openai import OpenAI

# 1. Configuration visuelle de la page web
st.set_page_config(page_title="Projet Hérodote", page_icon="🏛️", layout="centered")

st.title("🏛️ Projet Hérodote")
st.subheader("Le Conseil Perse : L'analyse croisée Ivre / Sobre")
st.write("Soumettez une idée. L'IA 'Ivre' (créative) va l'explorer sans limites, puis l'IA 'Sobre' (logique) va la filtrer.")

# 2. Zone de configuration dans la page
st.sidebar.header("Configuration")
# L'utilisateur pourra coller sa clé gratuite OpenRouter ici
api_key = st.sidebar.text_input("Clé API OpenRouter :", type="password", help="Obtenez-la gratuitement sur openrouter.ai")

# 3. Formulaire principal
problematique = st.text_area("Quelle problématique voulez-vous soumettre au Conseil ?", 
                             value="Comment relancer le commerce de centre-ville face aux géants du e-commerce ?")

if st.button("Déclencher le Conseil"):
    if not api_key:
        st.error("Veuillez entrer votre clé API OpenRouter dans la barre latérale.")
    elif not problematique:
        st.error("Veuillez écrire une problématique.")
    else:
        with st.spinner("Le vin coule, les esprits s'échauffent... Délibération en cours..."):
            try:
                # Connexion à OpenRouter (compatible avec le format OpenAI)
                client = OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=api_key
                )
                
                # Choix d'un excellent modèle 100% gratuit sur OpenRouter
                modele_gratuit = "meta-llama/llama-3-8b-instruct:free"
                
                # ÉTAPE 1 : LE CONSEILLER IVRE (Température haute)
                prompt_creative = f"Tu es le conseiller 'Ivre'. Propose 3 idées ultra-créatives, audacieuses et sans aucun filtre pour résoudre : '{problematique}'."
                reponse_creative = client.chat.completions.create(
                    model=modele_gratuit,
                    messages=[{"role": "user", "content": prompt_creative}],
                    temperature=1.3
                )
                idees_brutes = reponse_creative.choices[0].message.content
                
                st.markdown("### 🍷 [1] Les propositions du Conseiller 'Ivre'")
                st.info(idees_brutes)
                
                # ÉTAPE 2 : LE CONSEILLER SOBRE (Température basse)
                prompt_analytique = f"Tu es le conseiller 'Sobre'. Évalue froidement ces propositions pour '{problematique}'. Ne retiens et ne reformule que ce qui est logiquement et concrètement applicable :\n\n{idees_brutes}"
                reponse_analytique = client.chat.completions.create(
                    model=modele_gratuit,
                    messages=[{"role": "user", "content": prompt_analytique}],
                    temperature=0.1
                )
                decision_finale = reponse_analytique.choices[0].message.content
                
                st.markdown("### ⚖️ [2] La décision finale du Conseiller 'Sobre'")
                st.success(decision_finale)
                
            except Exception as e:
                st.error(f"Erreur technique : {e}")
