# app/utils/ad_utils.py

import streamlit as st

def create_prompt_for_ad(ad, selected_question):
    """
    Creates a prompt based on ad and question.
    
    :param ad: Adversarial data
    :param selected_question: Users question
    """
    category = ad.get("category_name", "Категория не указана")
    title = ad.get("title", "Название отсутствует")
    price = ad.get("price", "Цена не указана")
    description = ad.get("description", "Описание отсутствует")

    ad_content = (
        f"=== ОБЪЯВЛЕНИЕ ===\n"
        f"= Категория =\n{category}\n\n"
        f"= Название =\n{title}\n\n"
        f"= Цена =\n{price} рублей\n\n"
        f"= Описание =\n{description}\n\n"
    )

    system_message = {
        "role": "system",
        "content": (
            "Ты - помощник на площадке с объявлениями о продаже товаров и услуг."
            "Твоя задача - отвечать на вопросы клиентов на основе информации из объявлений."
            "Отвечай точно и кратко. Если информации для ответа недостаточно, отвечай: 'Пожалуйста, уточните у продавца.'"
            "В случае вопроса не по теме объявления, отвечай: 'Извините, это не мой предмет профессиональной деятельности.'"
        )
    }

    user_message = {
        "role": "user",
        "content": f"{ad_content}=== ВОПРОС ===\n{selected_question}\n\n"
    }

    return [system_message, user_message]