import pandas as pd

def _contains(haystack: str, needle: str) -> bool:
    return needle.lower() in (haystack or "").lower()

def filter_and_search(df: pd.DataFrame, query: str = "", industries=None, trl=None, has_demo=False, language=None):
    res = df.copy()
    if industries:
        res = res[res["industries"].apply(lambda lst: any(i in lst for i in industries))]
    if trl:
        res = res[res["trl"] == trl]
    if has_demo:
        res = res[res["has_live_demo"] == True]
    if language:
        res = res[res["languages"].apply(lambda lst: language in lst)]
    if query:
        res = res[
            res.apply(lambda r:
                      _contains(r["title"], query) or
                      _contains(r["one_liner"], query) or
                      any(query.lower() in t.lower() for t in r["tech_stack"]), axis=1)
        ]
    return res
