"""when you cant visit nativedb.dottieindustries.dev :("""
from os import system
from src.functions import (
    stop, init_file, fuzzy_lookup,
    fuzzy_lookup_refined, print_native,
    ProgramModes, NativesStatsInstance
)
from src.log import log, LogModes


def main():
    """Main entrypoint to the script"""
    file_data = None
    running = True
    mode = None

    # Read natives file
    with open("vendor/gta5-nativedb-data/natives.json", "r") as file:
        file_data = init_file(file)

    print(
        "Enter a native name to get its info, !clear to clear the terminal, or !exit to stop running."
    )


    print("What mode would you like to do?")
    print("[0]: Searching natives")
    print("[1]: Searching natives (within namespace)")
    print("[2]: Stats")
    print("[3]: Get all natives of a namespace")
    mode_inp = input("Your slection: ")
    if mode_inp == "0":
        mode = ProgramModes.SEARCHING_NATIVES
    elif mode_inp == "1":
        mode = ProgramModes.SEARCHING_NATIVES_REFINED
    elif mode_inp == "2":
        mode = ProgramModes.STATS
    elif mode_inp == "3":
        mode = ProgramModes.GET_ALL_NATIVES_FROM_NAMESPACE
    else:
        log("Please enter a correct mode!", LogModes.ERROR)
        stop()

    if mode == ProgramModes.STATS:
        print(f"Number of natives: {NativesStatsInstance.number_of_natives}")
        print(f"Number of namespaces: {NativesStatsInstance.number_of_namespaces}")
        print("Namespace stats:")
        nat_num = NativesStatsInstance.namespaces_nat_num
        nat_known = NativesStatsInstance.namespaces_nat_known
        nat_unknown = NativesStatsInstance.namespaces_nat_unknown
        for namespace, _, _ in zip(nat_num, nat_known, nat_unknown):
            print(
                (
                    f"""{namespace} has {nat_num[namespace]} natives, """
                    f"""of which {nat_known[namespace]} are known and """
                    f"""{nat_unknown[namespace]} are unknown."""
                )
            )
        mode = ProgramModes.SEARCHING_NATIVES

    # Main loop
    while running:
        if mode == ProgramModes.GET_ALL_NATIVES_FROM_NAMESPACE:
            namespace_inp = input("namespace name: ").upper()
            if not namespace_inp in NativesStatsInstance.namespaces_nat_num.keys():
                print("Namespace isn't valid!")
                stop()
            [
                print(native_dict["meta_comment"], "\n", native_dict["func_call"])
                for _, native_dict in file_data.items() if native_dict["namespace"] == namespace_inp
            ]
            continue

        if mode == ProgramModes.SEARCHING_NATIVES_REFINED:
            namespace = input("namespace name: ")
        inp = input("native name: ")

        if inp.startswith("!c"):
            system("clear")
            continue
        if inp.startswith("!q") or inp.startswith("!e"):
            stop()

        if mode == ProgramModes.SEARCHING_NATIVES:
            native_gotten = fuzzy_lookup(file_data, inp.upper())
        elif mode == ProgramModes.SEARCHING_NATIVES_REFINED:
            native_gotten = fuzzy_lookup_refined(file_data, inp.upper(), namespace.upper())

        print_native(native_gotten)


if __name__ == "__main__":
    main()
