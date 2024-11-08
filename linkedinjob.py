from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

def generar_excel(urls, vacancy_count):
    # Iniciamos el navegador (Chrome en este caso)
    driver = webdriver.Chrome()

    # Asegúrate de que las URLs son válidas
    valid_urls = []
    for url in urls:
        if isinstance(url, str) and url.startswith('http'):
            valid_urls.append(url)
        else:
            print(f"URL inválida: {url}")

    if not valid_urls:
        raise ValueError("No hay URLs válidas para procesar.")

    for url in valid_urls:
        driver.get(url)

        # Espera explícita para que la página cargue completamente
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'box_offer')))
        print("Página principal cargada.")

        # Cerrar el banner de cookies si está presente
        try:
            cookie_banner = wait.until(EC.presence_of_element_located((By.ID, 'cookie-banner')))
            close_button = cookie_banner.find_element(By.CSS_SELECTOR, 'button.cc-btn')
            close_button.click()
            print("Banner de cookies cerrado.")
        except Exception as e:
            print(f"No se pudo cerrar el banner de cookies: {e}")

        # Lista para almacenar los datos de cada trabajo
        jobs = []
        while len(jobs) < vacancy_count:
            job_offers = driver.find_elements(By.CLASS_NAME, 'box_offer')
            print(f"Encontradas {len(job_offers)} ofertas en esta página.")

            for offer in job_offers:
                try:
                    # Extraemos el nombre de la empresa y el título del trabajo
                    company = offer.find_element(By.CSS_SELECTOR, 'a.fc_base.t_ellipsis').text
                    job_title = offer.find_element(By.CSS_SELECTOR, 'h2.fs18.fwB a.js-o-link').text
                    job_link = offer.find_element(By.CSS_SELECTOR, 'h2.fs18.fwB a.js-o-link').get_attribute('href')

                    # Ir a la página de detalle del trabajo
                    offer.find_element(By.CSS_SELECTOR, 'h2.fs18.fwB a.js-o-link').click()

                    # Esperar que cargue la descripción completa en la página de detalle
                    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'box_detail')))
                    time.sleep(2)

                    # Capturar la descripción completa
                    description = driver.find_element(By.CSS_SELECTOR, 'div.fs16').text

                    # Guardar los datos en un diccionario
                    jobs.append({
                        'Company': company,
                        'Title': job_title,
                        'Description': description,
                        'Apply Link': job_link
                    })

                    print(f"Datos de la oferta capturados: {job_title} en {company}")

                    # Volver a la página de listado
                    driver.back()
                    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'box_offer')))
                    time.sleep(1)

                except Exception as e:
                    print(f"Error al procesar oferta: {e}")
                    continue

            # Intentar ir a la siguiente página si aún no tenemos suficientes trabajos
            try:
                next_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@title="Siguiente"]')))
                next_button.click()
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'box_offer')))
                print("Página siguiente cargada.")
            except Exception:
                print("No se encontró el botón 'Siguiente' o se produjo un error.")
                break

    # Convertir la lista de trabajos a un DataFrame de pandas
    final_df = pd.DataFrame(jobs)

    # Guardar el DataFrame en un archivo Excel para revisión posterior
    output_path = 'Computrabajo_Jobs.xlsx'
    final_df.to_excel(output_path, index=False)
    print(f"Datos guardados en {output_path} con éxito.")

    # Cerrar el navegador al finalizar
    driver.quit()

# Ejemplo de uso
# urls = ['https://www.computrabajo.com.co/']
# generar_excel(urls, 10)
