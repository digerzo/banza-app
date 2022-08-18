from unittest.mock import MagicMock
import pytest

from app.adapter import ClientDolarSi, CotizacionDolarBolsaNotFound

@pytest.fixture(name="response_payload")
def fixture_response():
    return [
        {"casa":{"compra":"136,44","venta":"142,44","agencia":"349","nombre":"Dolar Oficial","variacion":"0,02","ventaCero":"TRUE","decimales":"2"}}, \
        {"casa":{"compra":"288,00","venta":"292,00","agencia":"310","nombre":"Dolar Blue","variacion":"0,34","ventaCero":"TRUE","decimales":"2"}}, \
        {"casa":{"compra":"No Cotiza","venta":"0","agencia":"311","nombre":"Dolar Soja","variacion":"0","ventaCero":"TRUE","decimales":"3"}}, \
        {"casa":{"compra":"284,20","venta":"290,38","agencia":"312","nombre":"Dolar Contado con Liqui","variacion":"4,43","ventaCero":"TRUE","decimales":"2"}}, \
        {"casa":{"compra":"279,170","venta":"278,860","agencia":"313","nombre":"Dolar Bolsa","variacion":"0,900","ventaCero":"TRUE","decimales":"3"}}, \
        {"casa":{"compra":"9.852,070","venta":"0","agencia":"399","nombre":"Bitcoin","variacion":"-100,00","ventaCero":"TRUE","decimales":"3"}}, \
        {"casa":{"nombre":"Dolar turista","compra":"No Cotiza","venta":"249,27","agencia":"406","variacion":"0,02","ventaCero":"TRUE","decimales":"2"}}, \
        {"casa":{"compra":"133,18","venta":"142,93","agencia":"302","nombre":"Dolar","decimales":"3"}}, \
        {"casa":{"nombre":"Argentina","compra":"2.426,00","venta":"2,32","mejor_compra":"True","mejor_venta":"False","fecha":"05\/05\/15","recorrido":"16:30","afluencia":{},"agencia":"141","observaciones":{}}}
    ]

@pytest.fixture(name="response_missing")
def fixture_response_missing():
    return [
        {"casa":{"compra":"136,44","venta":"142,44","agencia":"349","nombre":"Dolar Oficial","variacion":"0,02","ventaCero":"TRUE","decimales":"2"}}, \
        {"casa":{"compra":"288,00","venta":"292,00","agencia":"310","nombre":"Dolar Blue","variacion":"0,34","ventaCero":"TRUE","decimales":"2"}}, \
        {"casa":{"compra":"No Cotiza","venta":"0","agencia":"311","nombre":"Dolar Soja","variacion":"0","ventaCero":"TRUE","decimales":"3"}}, \
        {"casa":{"compra":"284,20","venta":"290,38","agencia":"312","nombre":"Dolar Contado con Liqui","variacion":"4,43","ventaCero":"TRUE","decimales":"2"}}, \
        # {"casa":{"compra":"279,170","venta":"278,860","agencia":"313","nombre":"Dolar Bolsa","variacion":"0,900","ventaCero":"TRUE","decimales":"3"}}, \
        {"casa":{"compra":"9.852,070","venta":"0","agencia":"399","nombre":"Bitcoin","variacion":"-100,00","ventaCero":"TRUE","decimales":"3"}}, \
        {"casa":{"nombre":"Dolar turista","compra":"No Cotiza","venta":"249,27","agencia":"406","variacion":"0,02","ventaCero":"TRUE","decimales":"2"}}, \
        {"casa":{"compra":"133,18","venta":"142,93","agencia":"302","nombre":"Dolar","decimales":"3"}}, \
        {"casa":{"nombre":"Argentina","compra":"2.426,00","venta":"2,32","mejor_compra":"True","mejor_venta":"False","fecha":"05\/05\/15","recorrido":"16:30","afluencia":{},"agencia":"141","observaciones":{}}}
    ]



def test_client_get_cotizacion_dolar_bolsa(response_payload):
    """Test ClientDolarBolsaSi obtiene cotizacion correctamente"""
    api = MagicMock()
    response = MagicMock()
    response.json.return_value = response_payload
    api.get.return_value = response

    client = ClientDolarSi(api=api)
    cotizacion = client.get_cotizacion_dolar_bolsa()
    assert cotizacion == 278.86


def test_client_get_cotizacion_dolar_bolsa_raises_exception(response_missing):
    """Test ClientDolarBolsaSi obtiene cotizacion correctamente"""
    api = MagicMock()
    response = MagicMock()
    response.json.return_value = response_missing
    api.get.return_value = response

    client = ClientDolarSi(api=api)
    with pytest.raises(CotizacionDolarBolsaNotFound):
        _ = client.get_cotizacion_dolar_bolsa()
    