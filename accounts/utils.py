def get_username(request, credentials):
    username = credentials.get('username')
    return username


# def get_username(request, credentials):
#     data_username = None
#     if hasattr(request, 'data'):
#         data_username = request.data.get("username")
#     return data_username or request.POST.get("username")


