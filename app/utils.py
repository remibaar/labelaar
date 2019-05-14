
def get_dict_from_request(request, prefix):
    return {k.lstrip(prefix): v for k, v in request.POST.dict().items() if k.startswith(prefix)}
