# MODULE IMPORT
import sys
sys.path.append('../../lib')
import football_lib as lib

# READ *
params_before = lib.read_Params("*", "pipe_round")
print(params_before)

uri_list = []
for count in range(len(params_before)):
    # PARAMS : h2h, date, timezone
    params = {
        "h2h" : f"{params_before[count][2]}-{params_before[count][3]}",
        "date" : params_before[count][4],
        "timezone" : "Europe/London"
    }
    # MAKE URI
    # uri = lib.make_uri("fixtures/headtohead", params)
    uri = lib.make_uri(params)
    uri_list.append(uri)

# SEND CURL
for uri in uri_list:
    lib.send_curl(uri, "fixtures-headtohead")

# TEST
if __name__ == "__main__":
    print(params_before)
    print(uri_list[:5])