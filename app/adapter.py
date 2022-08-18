"""Adapters"""
import requests


class CotizacionDolarBolsaNotFound(Exception):
    """La cotizacion Dolar Bolsa no pudo ser recuperada de dolarsi.com"""

class ApiAdapterException(Exception):
    """No se pudo contactar con la api dolarsi.com"""


class ApiAdapter:
    """Api adapter class para interactuar con entes externos"""

    def __init__(self, url: str, filtro: str):
        self.url = url
        self.filtro = filtro

    def get(self):
        """Metodo GET a la url definida"""
        response = requests.get(f"{self.url}?{self.filtro}")
        if response.status_code != 200:
            raise ApiAdapterException(f"Status: {response.status_code}, Body: {response.json()}")
        
        return response



class ClientDolarSi:
    """Cliente para interactuar con la API de dolarsi.com"""
 
    def __init__(self, api: ApiAdapter = None):
        if api:
            self.api = api
        else:
            self.api = ApiAdapter(url="https://www.dolarsi.com/api/api.php", filtro="type=valoresprincipales")

    def get_cotizacion_dolar_bolsa(self) -> float:
        """Devuelve la cotizacion venta del Dolar Bolsa en dolarsi.com"""
        response = self.api.get()
        lista_cotizacion = [e['casa']['venta'] for e in response.json() if e['casa']['nombre'] == "Dolar Bolsa"]
        
        if len(lista_cotizacion) != 1:
            raise CotizacionDolarBolsaNotFound

        return float(lista_cotizacion[0].replace(",","."))
