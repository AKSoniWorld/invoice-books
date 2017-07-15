def get_current_company(user):
    user_company = user.companies.first()
    return user_company.company if user_company else None
