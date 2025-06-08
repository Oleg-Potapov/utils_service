import xml.etree.ElementTree as ET


# async def parse_rates(xml_content: str):
#     root = ET.fromstring(xml_content)
#     result = {}
#     for currency in root.findall('currency'):
#         code = currency.find('code').text
#         buy = currency.find('buy').text
#         sell = currency.find('sell').text
#         if code == 'USD':
#             result['usd_buy'] = float(buy)
#             result['usd_sell'] = float(sell)
#         elif code == 'EUR':
#             result['eur_buy'] = float(buy)
#             result['eur_sell'] = float(sell)
#     return result


def parse_rates(xml_content: str):
    root = ET.fromstring(xml_content)
    result = {}

    # Проходим по всем элементам <rates>
    for rates_elem in root.findall('.//rates'):
        from_currency = rates_elem.find('fromCurrency')
        to_currency = rates_elem.find('toCurrency')

        if from_currency is None or to_currency is None:
            continue

        from_code = from_currency.attrib.get('code')
        to_code = to_currency.attrib.get('code')

        # Ищем курсы EUR->RUB и USD->RUB
        if to_code == '643':  # Код RUB
            if from_code == '978':  # EUR
                buy = rates_elem.attrib.get('buy')
                sell = rates_elem.attrib.get('sell')
                if buy and sell:
                    result['eur_buy'] = float(buy)
                    result['eur_sell'] = float(sell)
            elif from_code == '840':  # USD
                buy = rates_elem.attrib.get('buy')
                sell = rates_elem.attrib.get('sell')
                if buy and sell:
                    result['usd_buy'] = float(buy)
                    result['usd_sell'] = float(sell)

    return result
