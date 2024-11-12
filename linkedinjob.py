from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

def generar_excel(urls, num_vacantes=10):
    jobs = []

    for url in urls:
        # Iniciamos el navegador (Chrome en este caso)
        driver = webdriver.Chrome()
        driver.get(url)

        # Espera explícita para que la página cargue completamente
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'box_offer')))
        print("Página principal cargada.")

        # Bucle de paginación hasta obtener el número deseado de trabajos
        while len(jobs) < num_vacantes:
            # Obtener todas las ofertas de trabajo en la página actual
            job_offers = driver.find_elements(By.CLASS_NAME, 'box_offer')
            print(f"Encontradas {len(job_offers)} ofertas en esta página.")

            for offer in job_offers:
                if len(jobs) >= num_vacantes:  # Si ya tenemos suficientes vacantes, salimos del ciclo
                    break
                try:
                    # Extraemos el nombre de la empresa y el título del trabajo
                    company = offer.find_element(By.CSS_SELECTOR, 'a.fc_base.t_ellipsis').text
                    job_title = offer.find_element(By.CSS_SELECTOR, 'h2.fs18.fwB a.js-o-link').text
                    job_link = offer.find_element(By.CSS_SELECTOR, 'h2.fs18.fwB a.js-o-link').get_attribute('href')

                    # Ir a la página de detalle del trabajo
                    offer.find_element(By.CSS_SELECTOR, 'h2.fs18.fwB a.js-o-link').click()

                    # Esperar que cargue la descripción completa en la página de detalle
                    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'box_detail')))
                    time.sleep(2)  # Pausa breve para asegurar que toda la información esté cargada

                    # Capturar la descripción completa
                    try:
                        description = driver.find_element(By.CSS_SELECTOR, 'div.fs16').text
                    except:
                        description = "Descripción no disponible"

                    # Capturar la sección de "Requerimientos"
                    try:
                        requirements = driver.find_element(By.CSS_SELECTOR, 'ul.fs16.disc').text
                        full_description = f"{description}\\n\\nRequerimientos:\\n{requirements}"
                    except:
                        full_description = description  # En caso de que no haya "Requerimientos"

                    # Guardar los datos en un diccionario
                    jobs.append({
                        'Company': company,
                        'Title': job_title,
                        'Description': full_description,
                        'Apply Link': job_link
                    })

                    print(f"Datos de la oferta capturados: {job_title} en {company}")

                    # Volver a la página de listado
                    driver.back()
                    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'box_offer')))
                    time.sleep(1)  # Pausa para que la página recargue los elementos

                except Exception as e:
                    print(f"Error al procesar oferta: {e}")
                    continue

            # Intentar ir a la siguiente página si aún no tenemos el número deseado de trabajos
            if len(jobs) < num_vacantes:
                try:
                    next_button = driver.find_element(By.XPATH, '//span[@title="Siguiente"]')
                    driver.execute_script("arguments[0].click();", next_button)
                    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'box_offer')))
                    print("Página siguiente cargada.")
                except Exception:
                    print("No se encontró el botón 'Siguiente' o se produjo un error.")
                    break

        # Cerrar el navegador al finalizar
        driver.quit()

    # Convertir la lista de trabajos a un DataFrame de pandas
    final_df = pd.DataFrame(jobs)

    # Guardar el DataFrame en un archivo Excel para revisión posterior
    output_path = 'Computrabajo_Jobs.xlsx'
    final_df.to_excel(output_path, index=False)
    print(f"Datos guardados en {output_path} con éxito.")
