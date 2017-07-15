def get_current_company(user):
    return user.companies.first().company
