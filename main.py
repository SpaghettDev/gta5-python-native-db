"""when you cant visit nativedb.dottieindustries.dev :("""
from os import system
from src.functions import (
    stop, init_file, print_native,
    ProgramModes, NativesStatsInstance,
    inp_to_mode, pluralify
)
from src.log import log, LogModes, LogTypes
from src.fuzzy import FuzzyLookup


def main():
    """Main entrypoint to the script"""
    file_data = None
    mode = None
    running = True

    # Read natives file
    try:
        log("Parsing natives file...")
        with open("vendor/gta5-nativedb-data/natives.json", "r") as file:
            file_data = init_file(file)
    except FileNotFoundError:
        log(
            "Couldn't find natives.json file, try running this: 'git submodule update --init'",
            LogTypes.ERROR
        )
        stop()

    fuzzy_dict = FuzzyLookup(file_data)
    fuzzy_list = FuzzyLookup(list(NativesStatsInstance.namespaces_nat_num.keys()))

    log(
        "Enter !clear to clear the terminal, or !exit to stop running when in a mode."
    )


    log("What mode would you like to use?")
    log("[0]: Searching natives")
    log("[1]: Searching natives (within namespace)")
    log("[2]: Get all natives of a namespace")
    log("[3]: Stats")
    if (
        (mode_inp := log("your selection: ", LogTypes.NORMAL, LogModes.ON, True))
        in inp_to_mode.keys()
        ):
        mode = inp_to_mode[mode_inp]
    else:
        log("Please enter a correct mode!", LogTypes.ERROR)
        stop()

    if mode == ProgramModes.STATS:
        log(f"Number of natives: {NativesStatsInstance.number_of_natives}")
        log(f"Number of namespaces: {NativesStatsInstance.number_of_namespaces}")
        log("Namespace stats:")
        nat_num = NativesStatsInstance.namespaces_nat_num
        nat_known = NativesStatsInstance.namespaces_nat_known
        nat_unknown = NativesStatsInstance.namespaces_nat_unknown
        for namespace, nk_val, nuk_val in zip(nat_num, nat_known.values(), nat_unknown.values()):
            log(
                (
                    f"""{namespace} has {nat_num[namespace]} """
                    f"""{pluralify("native", "natives", nat_num[namespace])}, """
                    f"""of which {nk_val} {pluralify("is", "are", nk_val)} known and """
                    f"""{nuk_val} {pluralify("is", "are", nuk_val)} unknown."""
                )
            )
        mode = ProgramModes.SEARCHING_NATIVES

    # Main loop
    while running:
        if mode == ProgramModes.GET_ALL_NATIVES_FROM_NAMESPACE:
            namespace_inp = log("namespace name: ", LogTypes.NORMAL, LogModes.ON, True).upper()
            namespace_fuzzied = fuzzy_list.lookup(namespace_inp, "No namespaces matches {}!")
            namespace_lookedup = fuzzy_dict.refined_lookup("", namespace_fuzzied, True)
            for _, tup in enumerate(namespace_lookedup):
                log(
                    f"""{file_data[tup[0]]["meta_comment"]}\n{file_data[tup[0]]["func_call"]}""",
                )
            continue

        if mode == ProgramModes.SEARCHING_NATIVES_REFINED:
            namespace_inp = log("namespace name: ", LogTypes.NORMAL, LogModes.ON, True).upper()
            namespace_fuzzied = fuzzy_list.lookup(namespace_inp, "No namespaces matches {}!")

        inp = log("native name: ", LogTypes.NORMAL, LogModes.ON, True)

        if inp.startswith("!c"):
            system("clear")
            continue
        if inp.startswith("!q") or inp.startswith("!e"):
            stop()

        if mode == ProgramModes.SEARCHING_NATIVES:
            native_gotten = fuzzy_dict.lookup(inp.upper(), "No native matches {}!")
        elif mode == ProgramModes.SEARCHING_NATIVES_REFINED:
            native_gotten = fuzzy_dict.refined_lookup(inp.upper(), namespace_fuzzied)

        if native_gotten:
            print_native(native_gotten)


if __name__ == "__main__":
    main()
