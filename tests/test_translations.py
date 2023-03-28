import sys
import os

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from src import translations


def test_normalize_responses():
    assert translations._normalize_response("") == ""
    assert translations._normalize_response("%D") == "%d"
    assert translations._normalize_response("%S") == "%s"
    assert translations._normalize_response("% 1 $ s") == "%1$s"
    assert translations._normalize_response("%1 $ s") == "%1$s"
    assert translations._normalize_response("% 1$ s") == "%1$s"
    assert translations._normalize_response("% 1 $s") == "%1$s"

    assert translations._normalize_response("% 1 $ d") == "%1$d"
    assert translations._normalize_response("%1 $ d") == "%1$d"
    assert translations._normalize_response("% 1$ d") == "%1$d"
    assert translations._normalize_response("% 1 $d") == "%1$d"

    assert translations._normalize_response("% 1 $ D") == "%1$d"
    assert translations._normalize_response("%1 $ D") == "%1$d"
    assert translations._normalize_response("% 1$ D") == "%1$d"
    assert translations._normalize_response("% 1 $D") == "%1$d"

    assert translations._normalize_response("%1 $, D") == "%1$,d"
    assert translations._normalize_response("%1 $, d") == "%1$,d"
    assert translations._normalize_response("%2 $, s") == "%2$,s"
    assert translations._normalize_response("de \"%1$s \"") == "de \"%1$s\""

    assert translations._normalize_response("%4 $ .1f") == "%4$.1f"
    # E.g. 200/300
    assert translations._normalize_response("d/ %") == "d/%"
    assert translations._normalize_response("f/ %") == "f/%"

    # percentage sign that shows up in Chinese translations
    assert translations._normalize_response("%") == "%"
    assert translations._normalize_response("...") == "…"
    assert translations._normalize_response("“") == "\""
    assert translations._normalize_response("”") == "\""
