"""Helper functions and variables"""
from json import load
from typing import Optional, Union, NoReturn
from enum import Enum
from src.log import log, LogModes, LogTypes
from src.stats import NativesStats


NativeDictType = dict[str, dict[str, Optional[Union[str, list[str]]]]]
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


def format_native_function(native_dict: NativeDictType) -> str:
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


def format_native_meta_comment(
    native_hash: str,
    native_dict: NativeDictType
    ) -> str:
    """Formats a native dict to the comment above a native in nativedb"""
    return f"""// {native_hash} {native_dict["jhash"]} b{native_dict["build"]}"""


def init_file(file) -> NativeDictType:
    """Returns a better dict for parsing natives.
    just like this:
    {
        "native_name": {
            "namespace": "x",
            "hash": "x",
            ...
        }
    }
    """
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


def print_native(native_dict: NativeDictType):
    """Prints native information"""
    log(native_dict["meta_comment"])
    log(native_dict["func_call"])
    log(f"""Namespace: {native_dict["namespace"]}""")
    log(f"""Comment: {native_dict["comment"]}""")
    if len(native_dict["old_names"]) > 0:
        log(f"""Old names: {", ".join(native_dict["old_names"])}""")
    log("")


def pluralify(string: str, plural: str, num_elem: int) -> str:
    """very simple function that functions :)
    Args:
        string (str): string
        plural (str): plural of string
        num_elem (int): if > 1 returns plural else string

    Returns:
        str
    """
    return plural if num_elem > 1 else string
