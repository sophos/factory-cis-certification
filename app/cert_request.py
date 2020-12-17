#!/usr/local/bin/python3

import sys
import os
import json
import jsonmerge


def usage():
    print('Usage: {scriptname} vresultfile rresultfile'.format(
        scriptname=os.path.basename(sys.argv[0])))
    print("")
    sys.exit()


def getjsoncontent(fname: str, dtype: str):
    try:
        with open(fname, "r") as f:
            j = f.read()
            r = json.loads(
                j.replace("result", "{type}-result".format(type=dtype.lower())))
    except FileNotFoundError:
        print("{type} result file not found: {path}".format(
            type=dtype, path=fname))
        exit(2)
    except json.JSONDecodeError:
        print("{type} result file is not valid JSON: {path}".format(
            type=dtype, path=fname))
    return r


vresult = getjsoncontent(sys.argv[1], 'Vendor')
rresult = getjsoncontent(sys.argv[2], 'Reference')

try:
    outputfile = open(sys.argv[3], "w") if len(sys.argv) == 4 else sys.stdout
except FileExistsError:
    print("Cannot open output file: \"{path}\"".format(path=sys.argv[3]))
    exit(2)

mergeschema = {
    "properties": {
        "benchmark-id": {"mergeStrategy": "discard"},
        "benchmark-title": {
            "mergeStrategy": "discard"
        },
        "benchmark-version": {
            "mergeStrategy": "discard"
        },
        "profile-id": {
            "mergeStrategy": "discard"
        },
        "profile-title": {
            "mergeStrategy": "discard"
        },
        "score": {
            "mergeStrategy": "discard"
        },
        "vendor-name": {
            "mergeStrategy": "overwrite"
        },
        "product-name": {
            "mergeStrategy": "overwrite"
        },
        "product-version": {
            "mergeStrategy": "overwrite"
        },
        "contact-name": {
            "mergeStrategy": "overwrite"
        },
        "contact-phone": {
            "mergeStrategy": "overwrite"
        },
        "contact-email": {
            "mergeStrategy": "overwrite"
        },
        "exceptions": {
            "mergeStrategy": "overwrite"
        },
        "rules": {
            "mergeStrategy": "arrayMergeById",
            "mergeOptions": {
                "idRef": "/rule-id"
            }
        }
    }
}
merger = jsonmerge.Merger(mergeschema)

results = merger.merge(rresult, vresult)
#json.dump(results, outputfile, indent=2)

certrequest = {
    "certification-request": merger.merge(rresult, vresult)
}

json.dump(certrequest, outputfile, indent=2)
