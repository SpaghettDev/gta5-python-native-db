"""Contains FuzzyLookup class, read its docstring for more info"""
from typing import Union, Any, Optional
from Levenshtein import ratio
from src.functions import NativeDictType, NativesStatsInstance, stop
from src.log import log, LogTypes


class FuzzyLookup:
    """Houses functions that fuzzily lookup a value in a dict, or a list"""
    def __init__(self, to_lookup: Union[dict, list]):
        self.is_dict = isinstance(to_lookup, dict)
        self.is_list = isinstance(to_lookup, list)
        if not any([self.is_dict, self.is_list]):
            log("to_lookup is neither a list nor a dict!", LogTypes.ERROR)
            stop()
        self.to_lookup = to_lookup

    # Should probably use a module like multimethod to overload fuzzy_lookup
    # but maybe it's my C++ instincts
    def lookup(self, query: Any, err_message: str) -> Optional[Union[Any, int]]:
            """Basic implementation of a fuzzy lookup of a dictionary/list"""
            formatted_err = err_message.replace("{}", query, 1)

            if self.is_list:  # how does "local" have a ratio .58 in localization but .6 in clock?!
                levs = [(itm, ratio(query, itm)) for _, itm in enumerate(self.to_lookup)]
                item, item_ratio = max(levs, key=lambda lev: lev[1])

                if item_ratio == 0.0:
                    log(formatted_err, LogTypes.ERROR)
                    return None
                return item

            levs = [(key, ratio(query, key)) for key in self.to_lookup.keys()]
            key, key_ratio = max(levs, key=lambda lev: lev[1])

            if key_ratio == 0.0:
                log(formatted_err, LogTypes.ERROR)
                return None
            return self.to_lookup.get(key)


    def refined_lookup(
        self,
        query: Any,
        namespace: str,
        get_all: bool = False
        ) -> Optional[Union[Any, list[NativeDictType]]]:
            """Basic implementation of a fuzzy lookup of a dictionary modified
            to search for a query within a namespace"""
            if self.is_list:
                log("Called 'refined_lookup()' while initialized with a list!", LogTypes.ERROR)
                stop()

            if not namespace in NativesStatsInstance.namespaces_nat_num.keys():
                log("Namespace isn't valid!", LogTypes.ERROR)
                return None

            levs = [
                (key, ratio(query, key)) for key in self.to_lookup.keys()
                if self.to_lookup[key]["namespace"] == namespace
            ]
            key, key_ratio = max(levs, key=lambda lev: lev[1])

            if get_all:
                return levs

            if key_ratio == 0.0:
                log(f"No native matches {query} in {namespace}!", LogTypes.ERROR)
                return None
            return self.to_lookup.get(key)
