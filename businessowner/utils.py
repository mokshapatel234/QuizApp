import jwt
from datetime import datetime, timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=1)  
    }

    jwt_token_bytes = jwt.encode(payload, 'secret', algorithm='HS256')
    jwt_token_str = jwt_token_bytes.decode('utf-8')  # Convert bytes to string

    return jwt_token_str

def paginate_data(request,data):
    page = request.GET.get('page', 1)
    items_per_page = request.GET.get('per_page', 5)
    paginator = Paginator(data, items_per_page)
    try:
        paginated_data = paginator.page(page)
    except PageNotAnInteger:
        paginated_data = paginator.page(1)
    except EmptyPage:
        paginated_data = paginator.page(paginator.num_pages)
    
    return paginated_data,items_per_page