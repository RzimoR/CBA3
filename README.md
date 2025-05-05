
# IRR/NPV/CBR Calculator (FastAPI backend)

Questo pacchetto contiene un backend Python sviluppato con FastAPI per calcolare:
- NPV (Net Present Value)
- IRR (Internal Rate of Return)
- CBR (Cost-Benefit Ratio)

## 📁 File inclusi

- `main.py` – Codice principale del backend FastAPI
- `requirements.txt` – Librerie Python necessarie
- `index.html` – Interfaccia web per inserire i dati e visualizzare i risultati
- `render.yaml` – (facoltativo, solo per deploy automatico)
- `README.md` – Questo file

---

## 🚀 Deploy manuale su [Render.com](https://render.com)

1. Crea un nuovo repository GitHub e carica questi file nella root.
2. Vai su [https://dashboard.render.com](https://dashboard.render.com) e clicca su **“New Web Service”**.
3. Collega il repository GitHub.
4. Quando ti chiede i parametri manuali, imposta:

   - **Environment:** `Python`
   - **Build Command:**  
     ```
     pip install -r requirements.txt
     ```
   - **Start Command:**  
     ```
     uvicorn main:app --host 0.0.0.0 --port 10000
     ```

5. Dopo il deploy, visita:

   ```
   https://<your-service-name>.onrender.com/index.html
   ```

   per usare il calcolatore.

---

## ✅ Input richiesti dal form

- `CAPEX` (€)
- `OPEX` annuo (€)
- `Benefici` annui (€)
- `Anni` di investimento
- `Tasso di sconto` (espresso in percentuale, es. 1.5%)

---

## 📤 Output

- NPV cumulativo
- IRR
- CB ratio
- Grafici (NPV cumulativo e costi/benefici) come immagini PNG
