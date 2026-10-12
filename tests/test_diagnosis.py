from src.diagnosis_engine import diagnose

def test_leak_rule():
    result = diagnose("low", "high")
    assert result[0]["conclusion"] == "Leak suspected"
    assert result[0]["certainty_factor"] == 0.80

def test_invalid_sensor_value():
    try:
        diagnose("unknown", "high")
    except ValueError:
        return
    assert False, "Expected ValueError"
