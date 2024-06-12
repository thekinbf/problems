def lookup(symbol):
    symbol = symbol.upper()
    if (symbol == "AAAA"):
        return {"price": 28.00, "symbol": "AAAA"}
    elif (symbol == "BBBB"):
        return {"price": 14.00, "symbol": "BBBB"}
    elif (symbol == "CCCC"):
        return {"price": 2000.00, "symbol": "CCCC"}
    else:
        return None
