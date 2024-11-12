import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def procesar_excel(candidato_filepath):
    # Cargar el archivo de trabajos y el archivo de candidatos proporcionado
    computrabajo_df = pd.read_excel('Computrabajo_Jobs.xlsx')
    talento_df = pd.read_excel(candidato_filepath)

    # Imprimir las columnas disponibles para diagnóstico
    print(talento_df.columns)

    # Convertir los niveles de inglés en una escala numérica
    nivel_ingles = {'A1': 1, 'A2': 2, 'B1': 3, 'B2': 4, 'C1': 5, 'C2': 6}

    # Asegúrate de que 'Nivel de Inglés' esté presente
    if 'Nivel de Inglés' in talento_df.columns:
        talento_df['Nivel de Inglés'] = talento_df['Nivel de Inglés'].map(nivel_ingles)
    else:
        raise ValueError("La columna 'Nivel de Inglés' no se encuentra en el archivo proporcionado.")

    # Función para detectar si el empleo requiere nivel avanzado de inglés
    def requiere_nivel_avanzado(desc):
        desc = desc.lower()
        return bool(re.search(r'\b(advanced|fluency|fluent|avanzado)\b', desc))

    # Preprocesar los datos
    job_descriptions = computrabajo_df['Description'].fillna('')
    candidate_skills = talento_df['Skills'].fillna('')

    # Crear un vectorizador TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english')
    corpus = list(job_descriptions) + list(candidate_skills)
    tfidf_matrix = vectorizer.fit_transform(corpus)

    # Dividir la matriz TF-IDF
    job_matrix = tfidf_matrix[:len(job_descriptions)]
    candidate_matrix = tfidf_matrix[len(job_descriptions):]

    # Calcular la similitud de coseno
    similarity_matrix = cosine_similarity(candidate_matrix, job_matrix)

    # Obtener la mejor coincidencia
    best_matches = []
    for idx, similarities in enumerate(similarity_matrix):
        candidato_nivel_ingles = talento_df.iloc[idx]['Nivel de Inglés']
        candidato_correo = talento_df.iloc[idx]['Correo de Contacto']
        adjusted_similarities = []
        for j, score in enumerate(similarities):
            if requiere_nivel_avanzado(job_descriptions[j]) and candidato_nivel_ingles < 5:
                adjusted_score = score * 0.5  # Penalización
            else:
                adjusted_score = score
            adjusted_similarities.append(adjusted_score)

        best_match_idx = max(range(len(adjusted_similarities)), key=lambda x: adjusted_similarities[x])
        best_match_score = adjusted_similarities[best_match_idx]
        best_matches.append({
            'Candidate': f"{talento_df.iloc[idx]['Nombre(s)']} {talento_df.iloc[idx]['Apellidos']}",
            'Profile': talento_df.iloc[idx]['Perfil'],
            'Best Matched Job Title': computrabajo_df.iloc[best_match_idx]['Title'],
            'Match Score': best_match_score,
            'Job Description': computrabajo_df.iloc[best_match_idx]['Description'],
            'Apply Link': computrabajo_df.iloc[best_match_idx]['Apply Link'],
            'Candidate Email': candidato_correo
        })

    # Guardar el resultado
    best_matches_df = pd.DataFrame(best_matches)
    best_matches_df.to_excel('Mejores_Coincidencias_Ingles_Ajustado.xlsx', index=False)
    print("Proceso completado. Resultados guardados en 'Mejores_Coincidencias_Ingles_Ajustado.xlsx'.")