import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key = os.getenv('GEMINI_API_KEY'))

def getQueryResponse(message):
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(
        history=[]
    )
    
    query_message = (
        "anda adalah query solver dan anda sangat memahami database dengan struktur seperti ini\n"
        "No,No_Order,\nOutlet,\nShift,\nTanggal,\nStatus,\nPembayaran,\nPAX,\nOperator,\nSub_Total,"
        "\nDiscount_total,\nKet_Discount,\nVoucher,\nket_Voucher,\nPromo,\nket_Promo,\nTAX,"
        "\nServis,\nOrder_Type,\nGrand_Total\n"
        "misalnya diberi pertanyaan\n"
        'QUESTION: "apa no order dengan order type terbanyak"\n'
        "jawaban anda harus dalam bentuk query sql\n"
        "ingat untuk hanya mengeluarkan sebuah query untuk menjawab, ingat juga bahwa anda sekarang ini akan melakukan query pada table df, pastikan hanya ada satu query yang keluar, "
        "jika anda diminta untuk melakukan query pada tanggal, bulan atau tahun gunakna format WHERE strftime('%y/m/d', Tanggal) = value untuk mencari"
        "gunakan query untuk database sqlite, pastikan query tersebut dapat berjalan tanpa error di sqlite dan jangan gunakan formatting apapun, hanya kirimkan querynya, "
        "karena selanjutnya query tersebut akan dijalankan di python\n"
        f"berikut pertanyaannya\n{message}, pastikan untuk hanya mengeluarkan query saja."
    )
    response = chat_session.send_message(query_message)
    return response.text

def getConclusion(question, query, result):
    generation_config = {
    "temperature": 0.8,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
      model_name="gemini-1.5-flash",
      generation_config=generation_config,
    )

    chat_session = model.start_chat(
      history=[]
    )
    
    query_message = (
        "anda adalah seorang yang handal untuk menganalisis, berikut saya akan memberikan pertanyaan, beserta dengan query dan hasilnya, simpulkan hasil tersebut, dan cobalah buat kesimpulan dari jawaban itu untuk questionnya"
        f"question: {question}"
        f"query: {query}"
        f"result: {result}"
        "simpulkan dari hal tersebut, dan kemudian jawab pertanyaan user tersebut, saya ingin ketika menjawab jangan menyebut query atau kalimat seperti 'berdasarkan query atua result tersebut' hindari kata kata seperti itu"
        "ketika menjawab sampaikan seperti contoh: 'berdasarkan hasil analisis saya, saya menemukan bahwa ... adalaha ....' tambahkan juga hal lain jika menurut anda user harus tau dari hasil analisa anda"
    )
    response = chat_session.send_message(query_message)
    return response.text

