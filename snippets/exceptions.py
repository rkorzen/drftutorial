from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db.utils import IntegrityError
from rest_framework.exceptions import ValidationError as DRFValidationError

def custom_exception_handler(exc, context):
    # Najpierw wywołujemy domyślny handler DRF
    response = exception_handler(exc, context)
    
    # Jeśli response jest None, oznacza to że DRF nie obsłużył tego wyjątku
    if response is None:
        if isinstance(exc, DjangoValidationError):
            response = Response(
                {'error': exc.messages},
                status=status.HTTP_400_BAD_REQUEST
            )
        elif isinstance(exc, IntegrityError):
            response = Response(
                {'error': 'Błąd integralności danych'},
                status=status.HTTP_400_BAD_REQUEST
            )
        elif isinstance(exc, UnicodeDecodeError):
            response = Response(
                {'error': 'Nieprawidłowe kodowanie pliku'},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            # Dla nieobsłużonych wyjątków
            response = Response(
                {'error': str(exc)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    else:
        # Formatujemy odpowiedź z DRF do spójnego formatu
        data = response.data
        if isinstance(data, list):
            response.data = {'error': data}
        elif isinstance(exc, DRFValidationError):
            if isinstance(data, dict):
                if 'detail' in data:
                    response.data = {'error': data['detail']}
                else:
                    response.data = {'error': data}

    return response