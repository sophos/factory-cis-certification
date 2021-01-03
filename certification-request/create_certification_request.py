#!/usr/local/bin/python3

import sys
import os
import json
import jsonmerge

merge_schema_path = os.path.join(os.path.dirname(__file__),"mergeschema.json")


def usage():
    print('\nUsage:\n\t{scriptname} vendor-result-file reference-result-file'.format(
        scriptname=__file__))
    print("")
    sys.exit()


def get_scan_result(result_file: str, result_type: str):
    try:
        with open(result_file, "r") as f:
            json_object = f.read().replace("result", "{type}-result".format(type=result_type.lower()))
            result = json.loads(json_object)
    except FileNotFoundError:
        print("\n{type} result file not found: {path}".format(
            type=result_type, path=result_file))
        exit(2)
    except json.JSONDecodeError:
        print("\n{type} result file is not valid JSON: {path}".format(
            type=result_type, path=result_file))
        exit(2)
    return result

def main():
    if len(sys.argv) not in (3, 4):
        print("\n{count} parameters".format(count=("Missing" if len(sys.argv)<3 else "Excess")))
        usage()
        exit(1)

    try:
        with open(merge_schema_path) as f:
            merge_schema = json.load(f)
    except FileNotFoundError:
        print("\nMerge schema not found: {path}".format(
            path=merge_schema_path))
        exit(2)
    except json.JSONDecodeError:
        print("\nMerge schema is not valid JSON: {path}".format(
            path=merge_schema_path))
        exit(2)
    
    try:
        outputfile = open(sys.argv[3], "w") if len(sys.argv) == 4 else sys.stdout
    except FileExistsError:
        print("\nCannot open output file: \"{path}\"".format(path=sys.argv[3]))
        exit(2)

    vendor_result = get_scan_result(sys.argv[1], 'Vendor')
    reference_result = get_scan_result(sys.argv[2], 'Reference')

    merger = jsonmerge.Merger(merge_schema)

    merged_result = merger.merge(reference_result, vendor_result)

    certification_request = { "certification-request": merged_result }

    json.dump(certification_request, outputfile, indent=2)

if __name__ == "__main__":
    main()
