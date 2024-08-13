from core.utils.RestHandler import RestHandler

rest = RestHandler()


async def fetch_users(company_id: int, role: str = "manager") -> list[str]:
    users_dict: list[dict] = await rest.post(f"service/users_find/", {
        "company_id": company_id,
        "role": role
    })
    return [user.get("telegram_id") for user in users_dict]
