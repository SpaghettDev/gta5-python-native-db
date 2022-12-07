"""Helper functions and variables"""
from json import load
from typing import NoReturn, Any, Union, List
from enum import Enum
from Levenshtein import ratio
from src.log import log, LogModes, LogTypes
from src.stats import NativesStats


NativesStatsInstance = NativesStats()


class ProgramModes(Enum):
    SEARCHING_NATIVES = 0
    SEARCHING_NATIVES_REFINED = 1
    STATS = 2
    GET_ALL_NATIVES_FROM_NAMESPACE = 3

inp_to_mode = {
    "0": ProgramModes.SEARCHING_NATIVES,
    "1": ProgramModes.SEARCHING_NATIVES_REFINED,
    "2": ProgramModes.GET_ALL_NATIVES_FROM_NAMESPACE,
    "3": ProgramModes.STATS
}


def stop() -> NoReturn:
    """Helper function that raises a SystemExit exception"""
    raise SystemExit


def format_native_function(native_dict: dict) -> str:
    """Turns native data into a declaration"""
    return_str = f"""{native_dict["return_type"]} {native_dict["name"]}("""

    # Below is one of the hackiest ways of formatting a declaration
    curr_param_idx = 0
    for i in range(len(native_dict["params"])):
        for _, val in native_dict["params"][i].items():
            return_str += f"{val} "
            curr_param_idx += 1
            if curr_param_idx == 2:
                return_str += ", "
                curr_param_idx = 0

    return_str += ")"
    return_str = return_str.replace(" ,", ",")  # void foo(t1 p1 , ...) -> void foo(t1 p1, ...)
    return_str = return_str.replace(", )", ")")  # void foo(..., ) -> void foo(...)
    return return_str


def format_native_meta_comment(native_hash, native_dict: dict) -> str:
    """Formats a native dict to the comment above a native in nativedb"""
    return f"""//{native_hash} {native_dict["jhash"]} b{native_dict["build"]}"""


def init_file(file) -> dict[str, dict[str, Union[str, None, List[str]]]]:
    """Returns a better dict for parsing natives"""
    def init_native_stats_instance(namespace: str):
        """oh my lord what the hell"""
        if not NativesStatsInstance.namespaces_nat_num.get(namespace, False):
            NativesStatsInstance.namespaces_nat_num[namespace] = 0
        if not NativesStatsInstance.namespaces_nat_known.get(namespace, False):
            NativesStatsInstance.namespaces_nat_known[namespace] = 0
        if not NativesStatsInstance.namespaces_nat_unknown.get(namespace, False):
            NativesStatsInstance.namespaces_nat_unknown[namespace] = 0

    return_dict = {}
    json_f = load(file)

    for namespace, native in json_f.items():
        init_native_stats_instance(namespace)
        NativesStatsInstance.number_of_namespaces += 1
        log(f"initing namespace {namespace}", LogTypes.NORMAL, LogModes.VERBOSE)
        for native_hash, native_dict in native.items():
            NativesStatsInstance.number_of_natives += 1
            NativesStatsInstance.namespaces_nat_num[namespace] += 1
            if native_dict["name"].startswith("_") or native_dict["name"].startswith("unk"):
                NativesStatsInstance.namespaces_nat_unknown[namespace] += 1
            else:
                NativesStatsInstance.namespaces_nat_known[namespace] += 1

            log(f"""initing native {native_dict["name"]}""", LogTypes.NORMAL, LogModes.VERBOSE)
            return_dict[native_dict["name"]] = {
                "namespace": namespace,
                "hash": native_hash,
                "jhash": native_dict["jhash"],
                "comment": native_dict["comment"],
                "return_type": native_dict["return_type"],
                "build": native_dict["build"],
                "old_names": native_dict.get("old_names", []),
                "meta_comment": format_native_meta_comment(native_hash, native_dict),
                "func_call": format_native_function(native_dict)
            }

    return return_dict


def fuzzy_lookup(dict_: dict, query: Any, err_message: str) -> Union[Any, None]:
        """Basic implementation of a fuzzy lookup of a dictionary"""
        levs = [(key, ratio(query, key)) for key in dict_.keys()]
        key, key_ratio = max(levs, key=lambda lev: lev[1])

        if key_ratio == 0.0:
            log(err_message.replace("{}", query, 1), LogTypes.ERROR)
        else:
            return dict_.get(key)


def fuzzy_lookup_refined(dict_: dict, query: Any, namespace: str) -> Union[Any, None]:
        """Basic implementation of a fuzzy lookup of a dictionary modified
        to search for a query within a namespace"""
        if not namespace in NativesStatsInstance.namespaces_nat_num.keys():
            log("Namespace isn't valid!", LogTypes.ERROR)
            return

        levs = [
            (key, ratio(query, key)) for key in dict_.keys() if dict_[key]["namespace"] == namespace
        ]
        key, key_ratio = max(levs, key=lambda lev: lev[1])

        if key_ratio == 0.0:
            log(f"No native matches {query} in {namespace}!", LogTypes.ERROR)
        else:
            return dict_.get(key)


def print_native(dict_: dict):
    """Prints native information"""
    log(dict_["meta_comment"])
    log(dict_["func_call"])
    log(f"""Namespace: {dict_["namespace"]}""")
    log(f"""Comment: {dict_["comment"]}""")
    if len(dict_["old_names"]):
        log(f"""Old names: {", ".join(dict_["old_names"])}""")
    log("")
