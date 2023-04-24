
from fastapi import FastAPI, Body

app = FastAPI()

user_data_schema = {
    'properties': {
        'name': {'description': 'Имя пользователя'},
        'last_name':  {'description': 'Фамилия пользователя'},
        'email': {'description': 'Электронная почта пользователя'},
        'phone_number': {'description': 'Номер телефона пользователя'},
        'purchases': {
            'type': 'array',
            'items': {
                'properties': {
                    'date': {'description': 'Дата покупки'},
                    'item': {'description': 'Проданная позиция'}
                }
            }
        }
    }
}

@app.post("/user")
async def create_user(
    user_data: dict = Body(..., embed=user_data_schema)
):
    """Создание пользователя"""

    if not user_data or not 'name' in user_data or not 'last_name' in user_data or not 'email' in user_data or not 'phone_number' in user_data or not 'purchases' in user_data:
        return 400, "Invalid request data provided"

    name = user_data['name']
    last_name = user_data['last_name']
    email = user_data['email']
    phone_number = user_data['phone_number']

    purchases = []
    for purchase in user_data['purchases']:
        if not purchase['date'] or not purchase['item']:
            return 400, "Invalid purchase data provided"
        purchases.append({
            'date': purchase['date'],
            'item': purchase['item']
        })

    return 200, f"User {name} {last_name} created"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
