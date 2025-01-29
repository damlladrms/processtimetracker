import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Başlık
st.title("Process Time Tracker")

# Dosya yükleme
uploaded_file = st.file_uploader("Bir Excel veya CSV dosyası yükleyin", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".xlsx"):
            data = pd.read_excel(uploaded_file)
        else:
            data = pd.read_csv(uploaded_file)
        
        st.write("### Yüklenen Veriler:")
        st.dataframe(data)
        
        # Toplam süre hesaplama
        total_time = data.iloc[:, 1:].sum().sum()
        st.write(f"**Toplam işlem süresi:** {total_time} saniye")
        
        # Grafik çizme
        categories = data.iloc[:, 0]
        times = data.iloc[:, 1:].sum(axis=1)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(categories, times, color='blue')
        ax.set_xlabel("İşlem")
        ax.set_ylabel("Toplam Süre (sn)")
        ax.set_title("İşlem Süreleri")
        plt.xticks(rotation=45, ha="right")
        st.pyplot(fig)
        
        # Yeni veri ekleme
        st.write("### Yeni İşlem Ekle")
        new_category = st.text_input("İşlem adı:")
        new_time = st.number_input("İşlem süresi (sn):", min_value=0.0, step=1.0)
        if st.button("Ekle"):
            if new_category and new_time:
                new_row = pd.DataFrame([[new_category, new_time]], columns=data.columns)
                data = pd.concat([data, new_row], ignore_index=True)
                st.success("Yeni işlem eklendi!")
                st.dataframe(data)
            else:
                st.error("Lütfen işlem adı ve süresini girin.")
        
        # Güncellenmiş verileri kaydetme
        st.write("### Güncellenmiş Verileri Kaydet")
        if st.button("Verileri Kaydet"):
            csv = data.to_csv(index=False).encode('utf-8')
            st.download_button("Güncellenmiş Veriyi İndir", data=csv, file_name="updated_data.csv", mime='text/csv')
    except Exception as e:
        st.error(f"Dosya yüklenirken hata oluştu: {e}")
