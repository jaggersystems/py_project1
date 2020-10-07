def is_bull_candle(f_open, f_close):
    if f_close > f_open:
        return 1 # Bull
    else:
        return 0 # Bear


def calculate_range(f_high, f_low):
    f_true_range = (f_high - f_low)
    # c_pips = int(c_true_range * 10000)  # TODO: Return pips
    return f_true_range


def calculate_high(f_open, f_high, f_low, f_close):
    nrange = calculate_range(f_high, f_low)
    if nrange == 0:
        return 0

    if is_bull_candle(f_open, f_close):
        # print("bull")
        f_high_percent = ((f_high - f_close) / nrange) * 100
    else:
        # print("bear")
        f_high_percent = ((f_high - f_open) / nrange) * 100
    return round_number(f_high_percent, 5)


def calculate_body(f_open, f_high, f_low, f_close):
    nrange = calculate_range(f_high, f_low)
    if nrange == 0:
        return 0

    if is_bull_candle(f_open, f_close):
        f_body_percent = ((f_close - f_open) / nrange) * 100
    else:
        f_body_percent = ((f_open - f_close) / nrange) * 100
    return round_number(f_body_percent, 5)


def calculate_low(f_open, f_high, f_low, f_close):
    f_low_percent = 100 - calculate_high(f_open, f_high, f_low, f_close) - calculate_body(f_open, f_high, f_low, f_close)
    return round_number(f_low_percent, 5)


def round_number(num_input, base=10):
    # base = 5 rounds the number to this nearest value, so 25, 30, 35 etc.
    return base * round(float(num_input) / base)