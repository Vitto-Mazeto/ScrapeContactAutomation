import re
import requests

# Função para limpar o número de telefone e garantir que o código DDI do Brasil (55) esteja presente
def format_phone_number(phone):
    # Remove qualquer máscara, mantendo apenas os dígitos
    phone = re.sub(r'\D', '', phone)
    
    # Adiciona o código DDI (55) se não estiver presente
    if not phone.startswith('55'):
        phone = '55' + phone
    
    return phone

# Função para enviar mensagem via Z-API
def send_whats_message(instance_id, token, phone, message):
    # Formata o número do telefone
    formatted_phone = format_phone_number(phone)
    
    # Monta a URL da API com a instância e token
    api_url = f"https://api.z-api.io/instances/{instance_id}/token/{token}/send-text"
    
    # Payload da requisição (dados a serem enviados)
    payload = {
        "phone": formatted_phone,
        "message": message
    }
    
    # Realiza a requisição POST para enviar a mensagem
    response = requests.post(api_url, json=payload)
    
    # Verifica o status da resposta
    if response.status_code == 200:
        print(f"Mensagem enviada com sucesso para {formatted_phone}")
    else:
        print(f"Falha ao enviar mensagem para {formatted_phone}. Erro: {response.status_code} - {response.text}")

    return response.status_code, response.text
